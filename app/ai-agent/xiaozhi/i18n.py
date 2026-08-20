"""Small, dependency-free localization layer for the Xiaozhi app."""

import os


DEFAULT_LOCALE = "zh-CN"
SUPPORTED_LOCALES = ("zh-CN", "en-US")


_MESSAGES = {
    "zh-CN": {
        "app_name": "小智",
        "app_subtitle": "K230 智能语音助手",
        "starting_title": "正在启动",
        "starting_detail": "正在准备音频与网络",
        "idle_title": "你好，我是小智",
        "tap_to_talk": "按一下开始说话",
        "thinking_title": "正在思考",
        "thinking_detail": "小智正在组织回答",
        "speaking_title": "小智正在说",
        "tap_to_interrupt": "轻触可打断",
        "continue_title": "可以继续问我",
        "alert_title": "提示",
        "alert_detail": "收到服务端提示",
        "button_done": "说完了",
        "button_interrupt": "打断并提问",
        "button_activation": "等待激活",
        "button_connecting": "正在连接",
        "button_retry": "重试",
        "button_talk": "开始说话",
        "status_starting": "启动中",
        "status_arming": "准备唤醒",
        "status_connecting": "连接中",
        "status_activating": "待绑定",
        "status_idle": "已就绪",
        "status_listening": "聆听中",
        "status_thinking": "思考中",
        "status_speaking": "回答中",
        "status_error": "需重试",
        "status_running": "运行中",
        "hardware_hint": "短按实体键操作 · 长按 2 秒退出",
        "wake_prompt": "叫我“{phrase}”",
        "wake_prompt_detail": "唤醒后直接说出问题 · 也可以点击按钮",
        "wake_button_fallback": "按钮对话仍可使用",
        "wake_success": "唤醒成功",
        "say_question": "请直接说出你的问题",
        "connecting_xiaozhi": "正在连接小智",
        "fetching_device_config": "正在获取设备配置",
        "activation_required": "需要绑定设备",
        "activation_detail": "登录 xiaozhi.me 添加设备",
        "activation_timeout": "等待激活超时，请重新进入 App",
        "ota_missing_websocket": "OTA 未返回 WebSocket 地址",
        "wake_resuming": "正在恢复语音唤醒",
        "wake_preparing": "正在准备语音唤醒",
        "opening_microphone": "正在打开麦克风",
        "wake_first_load": "首次加载大约需要 5 秒",
        "connecting": "正在连接",
        "secure_channel": "正在建立安全语音通道",
        "server_hello_timeout": "等待服务端 hello 超时",
        "voice_channel_disconnected": "语音连接已断开，请重试",
        "voice_channel_not_connected": "语音通道未连接",
        "audio_not_initialized": "音频设备未初始化",
        "listening_title": "我在听",
        "manual_listening_detail": "说完后再按一下",
        "recognizing_title": "正在识别",
        "please_wait": "请稍候",
        "unavailable_title": "暂时无法使用",
        "wake_service_stopped": "唤醒服务意外退出",
        "wake_engine_stopped": "唤醒引擎已停止",
        "wake_engine_exit": "唤醒引擎退出: {status}",
        "wake_model_load_failed": "无法加载唤醒模型",
        "wake_microphone_unavailable": "麦克风暂时不可用",
        "wake_microphone_read_failed": "麦克风读取失败",
        "mcp_device_status": "获取设备当前状态",
        "mcp_set_volume": "设置扬声器音量，范围 0 到 100",
        "mcp_set_brightness": "设置屏幕亮度，范围 0 到 100",
        "mcp_take_photo": "拍摄当前画面并回答关于画面的问题",
        "mcp_photo_question": "需要根据照片回答的问题",
        "mcp_set_led": "打开或关闭设备绿色状态灯",
        "mcp_system_info": "获取设备系统与硬件信息",
        "mcp_screen_info": "获取屏幕尺寸和背光信息",
        "params_object": "params 必须是对象",
        "user_tools_boolean": "withUserTools 必须是布尔值",
        "cursor_string": "cursor 必须是字符串",
        "unknown_cursor": "未知 cursor: {cursor}",
        "tool_too_large": "工具描述超过 MCP 列表大小限制: {name}",
        "arguments_object": "arguments 必须是对象",
        "missing_argument": "缺少参数: {name}",
        "argument_integer": "{name} 必须是整数",
        "argument_boolean": "{name} 必须是布尔值",
        "argument_string": "{name} 必须是字符串",
        "argument_below_min": "{name} 小于允许的最小值",
        "argument_above_max": "{name} 超出允许的最大值",
        "speaker_volume_read_failed": "无法读取扬声器音量",
        "device_operation_cancelled": "设备操作已取消",
        "volume_range": "volume 必须在 0 到 100 之间",
        "brightness_range": "brightness 必须在 0 到 100 之间",
        "brightness_unsupported": "设备不支持屏幕亮度控制",
        "status_led_unsupported": "设备不支持状态灯控制",
        "camera_open_failed": "无法打开摄像头",
        "camera_no_frame": "摄像头未返回画面",
        "camera_encode_failed": "摄像头画面编码失败",
        "photo_default_question": "请描述这张照片",
        "vision_endpoint_missing": "服务端未下发有效的视觉分析地址",
        "vision_http_error": "视觉服务返回 HTTP {status}: {detail}",
        "vision_response_too_large": "视觉服务响应过大",
        "identity_corrupt": "设备身份文件损坏，请从备份恢复 device.json",
        "identity_not_object": "设备身份文件必须是 JSON 对象",
        "identity_permissions": "无法保护设备身份文件权限",
        "activation_version_unsupported": "不支持的激活协议版本: {version}",
        "activation_v2_credentials": "激活 v2 需要预置 serial_number 和 hmac_key",
        "ota_response_too_large": "OTA 服务响应过大",
        "ota_http_error": "OTA 服务返回 HTTP {status}",
        "activation_challenge_missing": "激活响应缺少 challenge/code",
        "activation_http_error": "激活服务返回 HTTP {status}",
    },
    "en-US": {
        "app_name": "Xiaozhi",
        "app_subtitle": "K230 Voice Assistant",
        "starting_title": "Starting",
        "starting_detail": "Preparing audio and network",
        "idle_title": "Hi, I'm Xiaozhi",
        "tap_to_talk": "Tap to start talking",
        "thinking_title": "Thinking",
        "thinking_detail": "Xiaozhi is preparing a response",
        "speaking_title": "Xiaozhi is speaking",
        "tap_to_interrupt": "Tap to interrupt",
        "continue_title": "Ask me another question",
        "alert_title": "Notice",
        "alert_detail": "A server notice was received",
        "button_done": "I'm done",
        "button_interrupt": "Interrupt and ask",
        "button_activation": "Awaiting activation",
        "button_connecting": "Connecting",
        "button_retry": "Retry",
        "button_talk": "Start talking",
        "status_starting": "Starting",
        "status_arming": "Wake readying",
        "status_connecting": "Connecting",
        "status_activating": "Link device",
        "status_idle": "Ready",
        "status_listening": "Listening",
        "status_thinking": "Thinking",
        "status_speaking": "Speaking",
        "status_error": "Retry needed",
        "status_running": "Running",
        "hardware_hint": "Press KEY to act · Hold 2 sec to exit",
        "wake_prompt": "Say “{phrase}”",
        "wake_prompt_detail": "Ask your question after waking · Or tap below",
        "wake_button_fallback": "Tap-to-talk is still available",
        "wake_success": "I'm awake",
        "say_question": "Go ahead and ask your question",
        "connecting_xiaozhi": "Connecting to Xiaozhi",
        "fetching_device_config": "Fetching device configuration",
        "activation_required": "Device activation required",
        "activation_detail": "Add this device at xiaozhi.me",
        "activation_timeout": "Activation timed out. Reopen the app to retry",
        "ota_missing_websocket": "OTA did not return a WebSocket endpoint",
        "wake_resuming": "Resuming voice wake-up",
        "wake_preparing": "Preparing voice wake-up",
        "opening_microphone": "Opening microphone",
        "wake_first_load": "First load takes about 5 seconds",
        "connecting": "Connecting",
        "secure_channel": "Establishing a secure voice channel",
        "server_hello_timeout": "Timed out waiting for the server hello",
        "voice_channel_disconnected": "Voice connection lost. Please retry",
        "voice_channel_not_connected": "Voice channel is not connected",
        "audio_not_initialized": "Audio device is not initialized",
        "listening_title": "I'm listening",
        "manual_listening_detail": "Tap again when you're done",
        "recognizing_title": "Recognizing",
        "please_wait": "Please wait",
        "unavailable_title": "Temporarily unavailable",
        "wake_service_stopped": "Wake service exited unexpectedly",
        "wake_engine_stopped": "Wake engine stopped",
        "wake_engine_exit": "Wake engine exited: {status}",
        "wake_model_load_failed": "Unable to load the wake model",
        "wake_microphone_unavailable": "Microphone is temporarily unavailable",
        "wake_microphone_read_failed": "Microphone read failed",
        "mcp_device_status": "Get the current device status",
        "mcp_set_volume": "Set speaker volume from 0 to 100",
        "mcp_set_brightness": "Set screen brightness from 0 to 100",
        "mcp_take_photo": "Take a photo and answer a question about it",
        "mcp_photo_question": "Question to answer from the photo",
        "mcp_set_led": "Turn the green device status LED on or off",
        "mcp_system_info": "Get device system and hardware information",
        "mcp_screen_info": "Get screen dimensions and backlight information",
        "params_object": "params must be an object",
        "user_tools_boolean": "withUserTools must be a boolean",
        "cursor_string": "cursor must be a string",
        "unknown_cursor": "Unknown cursor: {cursor}",
        "tool_too_large": "Tool description exceeds the MCP list limit: {name}",
        "arguments_object": "arguments must be an object",
        "missing_argument": "Missing argument: {name}",
        "argument_integer": "{name} must be an integer",
        "argument_boolean": "{name} must be a boolean",
        "argument_string": "{name} must be a string",
        "argument_below_min": "{name} is below the allowed minimum",
        "argument_above_max": "{name} exceeds the allowed maximum",
        "speaker_volume_read_failed": "Unable to read speaker volume",
        "device_operation_cancelled": "Device operation was cancelled",
        "volume_range": "volume must be between 0 and 100",
        "brightness_range": "brightness must be between 0 and 100",
        "brightness_unsupported": "Screen brightness control is not supported",
        "status_led_unsupported": "Status LED control is not supported",
        "camera_open_failed": "Unable to open the camera",
        "camera_no_frame": "The camera did not return an image",
        "camera_encode_failed": "Unable to encode the camera image",
        "photo_default_question": "Describe this photo",
        "vision_endpoint_missing": "The server did not provide a valid vision endpoint",
        "vision_http_error": "Vision service returned HTTP {status}: {detail}",
        "vision_response_too_large": "Vision service response is too large",
        "identity_corrupt": "The device identity file is corrupt; restore device.json from backup",
        "identity_not_object": "The device identity file must contain a JSON object",
        "identity_permissions": "Unable to secure device identity file permissions",
        "activation_version_unsupported": "Unsupported activation protocol version: {version}",
        "activation_v2_credentials": "Activation v2 requires provisioned serial_number and hmac_key",
        "ota_response_too_large": "OTA service response is too large",
        "ota_http_error": "OTA service returned HTTP {status}",
        "activation_challenge_missing": "Activation response is missing challenge/code",
        "activation_http_error": "Activation service returned HTTP {status}",
    },
}


def normalize_locale(value, fallback=DEFAULT_LOCALE):
    """Normalize a configured/POSIX locale to one supported by the app."""
    fallback = fallback if fallback in SUPPORTED_LOCALES else DEFAULT_LOCALE
    candidate = str(value or "").strip()
    if not candidate or candidate.lower() in ("auto", "system"):
        return fallback
    candidate = candidate.split(".", 1)[0].split("@", 1)[0].replace("_", "-").lower()
    # CyberCAM's system ``set-language en`` command intentionally stores
    # English as C.UTF-8.  Treating the POSIX locale as unknown would make an
    # explicitly selected English desktop fall back to Chinese.
    if candidate == "c" or candidate == "posix":
        return "en-US"
    if candidate.startswith("zh"):
        return "zh-CN"
    if candidate.startswith("en"):
        return "en-US"
    return fallback


def resolve_locale(value="auto", environ=None):
    """Resolve ``auto`` from standard locale variables, defaulting to Chinese."""
    candidate = str(value or "auto").strip()
    if candidate.lower() not in ("", "auto", "system"):
        return normalize_locale(candidate)
    environ = os.environ if environ is None else environ
    for name in ("LC_ALL", "LC_MESSAGES", "LANG"):
        raw = str(environ.get(name) or "").strip()
        if raw:
            return normalize_locale(raw)
    return DEFAULT_LOCALE


def default_wake_word(locale):
    return "Hello Xiaozhi" if normalize_locale(locale) == "en-US" else "你好小智"


def resolve_wake_locale(value, ui_locale, wake_word=""):
    """Resolve wake language while keeping legacy explicit phrases aligned."""
    candidate = str(value or "auto").strip()
    if candidate.lower() not in ("", "auto", "system"):
        return normalize_locale(candidate, fallback=ui_locale)
    phrase = " ".join(str(wake_word or "").strip().lower().split())
    if phrase in ("你好小智", "小智小智"):
        return "zh-CN"
    if phrase == "hello xiaozhi":
        return "en-US"
    return normalize_locale(ui_locale)


class Localizer:
    def __init__(self, locale=DEFAULT_LOCALE):
        self.locale = normalize_locale(locale)

    def text(self, key, **values):
        template = _MESSAGES[self.locale].get(key, _MESSAGES[DEFAULT_LOCALE].get(key, key))
        return template.format(**values) if values else template

    __call__ = text
