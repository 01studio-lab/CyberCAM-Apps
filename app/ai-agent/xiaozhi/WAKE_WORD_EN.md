# Customizing the offline wake phrase

[中文](./WAKE_WORD.md)

The app bundles the bilingual open-vocabulary `sherpa-onnx-kws-zipformer-zh-en-3M-2025-12-20` model. Chinese and English wake phrases can be changed without retraining the model, recompiling the K230 daemon, or downloading anything on the device.

## Files and settings

- `wake_word_locale` selects `wake/keywords.zh-CN.txt` or `wake/keywords.en-US.txt`; `auto` follows the UI locale.
- `wake_word` controls the idle prompt and protocol text. Leave it empty for the localized default.
- The selected keyword file contains the tokens that are actually recognized.
- `wake/manifest.sha256` protects all bundled runtime and model assets during deployment.

The default English entry is:

```text
HH AH0 L OW1 x iǎo zh ì :3.5 #0.10 @HELLO_XIAOZHI
```

The fields are phoneme tokens, boosting score, trigger threshold, and returned keyword. A larger score or smaller threshold increases sensitivity and false-wake risk. The alias after `@` must not contain spaces.

To generate another phrase, use the official `sherpa-onnx-cli text2token` tool with `--tokens-type phone+ppinyin`, the bundled `wake/model/tokens.txt`, and `en.phone` from the [official bilingual model archive](https://k2-fsa.github.io/sherpa/onnx/kws/pretrained_models/index.html#sherpa-onnx-kws-zipformer-zh-en-3m-2025-12-20-chinese-english). Copy the result into the appropriate locale keyword file.

After editing a keyword file, update its SHA-256 entry and run:

```sh
cd app/ai-agent/xiaozhi
sha256sum -c wake/manifest.sha256
python3 -m unittest discover -s tests -p 'test_*.py'
```

Fully exit and restart the app after changing a phrase or wake locale because keyword tokens are loaded when the model starts.
