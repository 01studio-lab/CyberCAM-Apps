"""Xiaozhi MCP-over-WebSocket JSON-RPC server."""

import json
import queue
import threading

from i18n import Localizer


MCP_PROTOCOL_VERSION = "2024-11-05"
MAX_LIST_PAYLOAD = 8000


def _schema(properties=None, required=None):
    value = {"type": "object", "properties": properties or {}}
    if required:
        value["required"] = required
    return value


class MCPServer:
    def __init__(
        self,
        devices,
        server_name="cybercam-xiaozhi",
        version="2.1.0",
        locale="zh-CN",
    ):
        self.devices = devices
        self.localizer = Localizer(locale)
        tr = self.localizer.text
        self.server_name = server_name
        self.version = version
        self._jobs = queue.Queue(maxsize=16)
        self._closed = threading.Event()
        self._worker = threading.Thread(
            target=self._run,
            name="xiaozhi-mcp",
            daemon=True,
        )
        self._worker.start()
        self._tools = [
            self._tool("self.get_device_status", tr("mcp_device_status"), _schema(), lambda _: devices.get_device_status()),
            self._tool(
                "self.audio_speaker.set_volume",
                tr("mcp_set_volume"),
                _schema({"volume": {"type": "integer", "minimum": 0, "maximum": 100}}, ["volume"]),
                lambda args: devices.set_volume(args["volume"]),
            ),
            self._tool(
                "self.screen.set_brightness",
                tr("mcp_set_brightness"),
                _schema({"brightness": {"type": "integer", "minimum": 0, "maximum": 100}}, ["brightness"]),
                lambda args: devices.set_brightness(args["brightness"]),
            ),
            self._tool(
                "self.camera.take_photo",
                tr("mcp_take_photo"),
                _schema({"question": {"type": "string", "description": tr("mcp_photo_question")}}, ["question"]),
                lambda args: devices.take_photo(args["question"]),
            ),
            self._tool(
                "self.status_led.set_enabled",
                tr("mcp_set_led"),
                _schema({"enabled": {"type": "boolean"}}, ["enabled"]),
                lambda args: devices.set_status_led(args["enabled"]),
            ),
            self._tool("self.get_system_info", tr("mcp_system_info"), _schema(), lambda _: devices.get_system_info(), True),
            self._tool("self.screen.get_info", tr("mcp_screen_info"), _schema(), lambda _: devices.get_screen_info(), True),
        ]

    @staticmethod
    def _tool(name, description, input_schema, handler, user_only=False):
        return {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "handler": handler,
            "user_only": user_only,
        }

    @staticmethod
    def _response(request_id, result):
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id, code, message):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }

    @staticmethod
    def _public_tool(tool):
        return {key: tool[key] for key in ("name", "description", "inputSchema")}

    def _list_tools(self, params):
        tr = self.localizer.text
        if not isinstance(params, dict):
            raise ValueError(tr("params_object"))
        include_user = params.get("withUserTools", False)
        if not isinstance(include_user, bool):
            raise ValueError(tr("user_tools_boolean"))
        available = [tool for tool in self._tools if include_user or not tool["user_only"]]
        cursor = params.get("cursor") or ""
        if not isinstance(cursor, str):
            raise ValueError(tr("cursor_string"))
        start = 0
        if cursor:
            start = next(
                (index for index, tool in enumerate(available) if tool["name"] == cursor),
                -1,
            )
            if start < 0:
                raise ValueError(tr("unknown_cursor", cursor=cursor))
        selected = []
        index = start
        while index < len(available):
            candidate = selected + [self._public_tool(available[index])]
            probe = {"tools": candidate}
            if index + 1 < len(available):
                probe["nextCursor"] = available[index + 1]["name"]
            if len(json.dumps(probe, ensure_ascii=False).encode("utf-8")) > MAX_LIST_PAYLOAD:
                if not selected:
                    raise ValueError(tr("tool_too_large", name=available[index]["name"]))
                break
            selected = candidate
            index += 1
        result = {"tools": selected}
        if index < len(available):
            result["nextCursor"] = available[index]["name"]
        return result

    def _validate_arguments(self, tool, arguments):
        tr = self.localizer.text
        if not isinstance(arguments, dict):
            raise ValueError(tr("arguments_object"))
        schema = tool["inputSchema"]
        for name in schema.get("required", []):
            if name not in arguments:
                raise ValueError(tr("missing_argument", name=name))
        for name, value in arguments.items():
            rule = schema.get("properties", {}).get(name)
            if rule is None:
                continue
            expected = rule.get("type")
            if expected == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
                raise ValueError(tr("argument_integer", name=name))
            if expected == "boolean" and not isinstance(value, bool):
                raise ValueError(tr("argument_boolean", name=name))
            if expected == "string" and not isinstance(value, str):
                raise ValueError(tr("argument_string", name=name))
            if "minimum" in rule and value < rule["minimum"]:
                raise ValueError(tr("argument_below_min", name=name))
            if "maximum" in rule and value > rule["maximum"]:
                raise ValueError(tr("argument_above_max", name=name))

    def handle(self, payload):
        if not isinstance(payload, dict):
            return self._error(None, -32600, "Invalid Request")
        request_id = payload.get("id")
        if payload.get("jsonrpc") != "2.0" or not isinstance(payload.get("method"), str):
            return self._error(request_id, -32600, "Invalid Request")
        method = payload["method"]
        # A JSON-RPC notification is defined by the absence of an id. Its
        # method name is unrestricted and it must never receive a response.
        if "id" not in payload:
            return None
        params = payload.get("params", {})
        if params is None:
            params = {}
        if not isinstance(params, dict):
            return self._error(request_id, -32602, self.localizer.text("params_object"))
        try:
            if method == "initialize":
                capabilities = params.get("capabilities") if isinstance(params, dict) else {}
                capabilities = capabilities if isinstance(capabilities, dict) else {}
                vision = capabilities.get("vision")
                vision = vision if isinstance(vision, dict) else {}
                self.devices.configure_vision(vision)
                print("[mcp] initialized (vision=%s)" % bool(vision and vision.get("url")))
                return self._response(
                    request_id,
                    {
                        "protocolVersion": MCP_PROTOCOL_VERSION,
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": self.server_name, "version": self.version},
                    },
                )
            if method == "tools/list":
                result = self._list_tools(params)
                print("[mcp] listed %d tools" % len(result["tools"]))
                return self._response(request_id, result)
            if method == "tools/call":
                if not isinstance(params, dict):
                    raise ValueError(self.localizer.text("params_object"))
                name = params.get("name")
                tool = next((item for item in self._tools if item["name"] == name), None)
                if tool is None:
                    return self._error(request_id, -32601, "Unknown tool: %s" % name)
                print("[mcp] calling %s" % name)
                arguments = params.get("arguments", {})
                if arguments is None:
                    arguments = {}
                self._validate_arguments(tool, arguments)
                try:
                    value = tool["handler"](arguments)
                    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
                    return self._response(
                        request_id,
                        {"content": [{"type": "text", "text": text}], "isError": False},
                    )
                except Exception as exc:
                    return self._response(
                        request_id,
                        {
                            "content": [{"type": "text", "text": str(exc) or type(exc).__name__}],
                            "isError": True,
                        },
                    )
            return self._error(request_id, -32601, "Method not found")
        except (KeyError, TypeError, ValueError) as exc:
            return self._error(request_id, -32602, str(exc) or "Invalid params")

    def _run(self):
        while not self._closed.is_set():
            try:
                job = self._jobs.get(timeout=0.2)
            except queue.Empty:
                continue
            if job is None:
                return
            payload, send_response = job
            try:
                response = self.handle(payload)
                if response is not None and not self._closed.is_set():
                    send_response(response)
            except Exception as exc:
                print("[mcp]", type(exc).__name__, exc)

    def submit(self, payload, send_response):
        if self._closed.is_set():
            return False
        try:
            self._jobs.put_nowait((payload, send_response))
            return True
        except queue.Full:
            if isinstance(payload, dict) and "id" in payload:
                send_response(
                    self._error(payload.get("id"), -32000, "MCP request queue is full")
                )
            return False

    def close(self):
        if self._closed.is_set():
            return
        self._closed.set()
        cancel = getattr(self.devices, "cancel_operations", None)
        if callable(cancel):
            cancel()
        try:
            while True:
                self._jobs.get_nowait()
        except queue.Empty:
            pass
        try:
            self._jobs.put_nowait(None)
        except queue.Full:
            pass
        if self._worker is not threading.current_thread():
            self._worker.join(timeout=1.0)
