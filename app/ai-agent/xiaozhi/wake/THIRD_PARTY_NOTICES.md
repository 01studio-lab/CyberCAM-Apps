# 第三方唤醒资源

本目录内置的 sherpa-onnx 运行库和关键词模型仅用于小智的本地离线唤醒。

以下资源随 App 再分发：

- sherpa-onnx v1.13.2 `linux-riscv64-spacemit-shared`：来源于 [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)，按 [Apache License 2.0](./APACHE-2.0.txt) 使用。原始发布包 SHA-256：`4c2c101da444dcca72274653ada16edf2c4b009e55a57bc0e5ef6337f4dbfc60`。
- ONNX Runtime 1.24.2 SpaceMi 构建：`libonnxruntime.so.1` 和 `libonnxruntime_providers_shared.so` 按 [MIT License](./ONNXRUNTIME-MIT.txt) 使用，依赖组件声明见 [ONNX Runtime Third Party Notices](./ONNXRUNTIME-THIRD-PARTY-NOTICES.txt)。
- `sherpa-onnx-kws-zipformer-zh-en-3M-2025-12-20`：来源于 [sherpa-onnx 官方 KWS 模型发布包](https://github.com/k2-fsa/sherpa-onnx/releases/tag/kws-models)。原始发布包 SHA-256：`68447f4fbc67e70eee3a93961f36e81e98f47aef73ce7e7ca00885c6cd3616a6`。发布包未附带模型权重专属许可证；sherpa-onnx 仓库的 Apache-2.0 明确覆盖软件源码，但上游目前没有单独明确这些模型权重及词表的授权范围。公开或商业再分发前应向模型发布者确认适用条款。

仓库只保留运行小智所需的最小文件集合。`native/wakeword-daemon` 由同目录下的 `wakeword_daemon.cpp` 在 CyberCAM K230 上编译，使用内置的 sherpa-onnx C API；官方 `sherpa-onnx-keyword-spotter-alsa` 仅作为常驻服务不可用时的降级路径。
