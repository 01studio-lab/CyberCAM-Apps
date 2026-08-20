# Xiaozhi for CyberCAM K230

[中文](./README.md)

Xiaozhi is a voice assistant for the WalnutPi CyberCAM. It implements the official Xiaozhi WebSocket protocol and streams 16 kHz mono audio in 60 ms Opus frames.

## Features

- Chinese and English UI, status text, controls, and MCP tool descriptions
- Offline bilingual wake-up: “你好小智” in Chinese or “Hello Xiaozhi” in English
- OTA endpoint discovery and device activation
- Live Opus input/output without temporary audio files
- STT captions, answer captions, emotion, and connection state
- Tap and physical KEY controls, interruption, and safe exit
- Six-second no-speech timeout and response/playback recovery
- Warm WebSocket sessions and a persistent local wake model between turns
- MCP controls for status, volume, brightness, camera vision, status LED, and system information
- TLS verification by default and support for private Xiaozhi servers

## Controls

- Say the wake phrase while idle, then ask the question directly.
- Tap the bottom button or press KEY to start and stop manual recording.
- Tap while Xiaozhi is replying to interrupt and ask a new question.
- Tap `×` or hold KEY for two seconds to exit safely.

For the official service, add the device at [xiaozhi.me](https://xiaozhi.me/) when the six-digit activation code appears.

## Localization

Create `/data/app/xiaozhi/config.json` only when you need to override defaults:

```json
{
  "locale": "en-US",
  "wake_word_locale": "auto",
  "wake_word": ""
}
```

- `locale`: `auto`, `zh-CN`, or `en-US`. Auto reads `LC_ALL`, `LC_MESSAGES`, then `LANG`; unsupported values fall back to Chinese.
- `wake_word_locale`: `auto`, `zh-CN`, or `en-US`. Auto follows the UI locale; a legacy explicit “你好小智” or “Hello Xiaozhi” value keeps its matching wake language.
- `wake_word`: optional display/protocol override. Leave it empty to use “你好小智” or “Hello Xiaozhi” automatically.

The wake phrase is recognized locally. Changing the recognized phrase also requires updating its locale-specific keyword file; see [Customizing the offline wake phrase](./WAKE_WORD_EN.md).

## Deploy

The K230 riscv64 daemon, runtime libraries, bilingual KWS model, and keyword files are bundled. No compilation, package installation, or model download is needed on the device.

Exit the running app, then run from the repository root:

```sh
./app/ai-agent/xiaozhi/deploy.sh 10.10.11.213
```

The deployment verifies bundled resources and preserves the existing `config.json` and `device.json`.

## Privacy

Idle microphone audio is processed only by the on-device keyword model and is neither stored nor uploaded. Question audio is sent to the configured Xiaozhi service only after the UI enters the listening state. Set `wake_word_enabled` to `false` to disable idle microphone capture.
