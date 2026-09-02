# 修改离线唤醒词

[English](./WAKE_WORD_EN.md)

小智内置 `sherpa-onnx-kws-zipformer-zh-en-3M-2025-12-20` 中英双语开放词汇模型。修改中英文唤醒词只需更新关键词文件，不需要重新训练模型、重新编译 K230 程序或在设备上下载模型。

## 语言与文件

| 配置/文件 | 作用 |
| --- | --- |
| `config.json` 的 `locale` | 界面和 MCP 描述语言：`auto`、`zh-CN`、`en-US` |
| `config.json` 的 `wake_word_locale` | 选择本地识别使用的关键词文件；`auto` 通常跟随界面 |
| `config.json` 的 `wake_word` | 待机提示和协议文字；留空时使用对应语言默认值 |
| `wake/keywords.zh-CN.txt` | 中文识别 token，默认“你好小智”，兼容“小智小智” |
| `wake/keywords.en-US.txt` | 英文识别 token，默认“Hello Xiaozhi” |
| `wake/manifest.sha256` | 部署脚本使用的资源完整性清单 |

`wake_word` 本身不会生成识别 token。因此修改它时，必须同步修改所选语言的关键词文件。为兼容旧设备，`wake_word_locale` 为 `auto` 且 `wake_word` 明确是内置中英文默认词时，会自动选择匹配的关键词文件。

## 关键词格式

中文默认项：

```text
n ǐ h ǎo x iǎo zh ì :3.5 #0.10 @你好小智
```

英文默认项（“Hello” 使用英语音素，“小智”使用拼音音素）：

```text
HH AH0 L OW1 x iǎo zh ì :3.5 #0.10 @HELLO_XIAOZHI
```

格式为：

```text
音素 token :增益 #触发阈值 @识别结果
```

- `:3.5` 是 boosting score，越大越容易触发，也更容易误唤醒。
- `#0.10` 是 trigger threshold，范围 0 到 1，越小越容易触发。
- `@...` 是返回结果。`phone+ppinyin` 模型要求提供它，空格应替换为下划线。
- 行内的 `:` 和 `#` 会覆盖 `config.json` 中的全局 `wake_word_score`、`wake_word_threshold`。

## 切换中英文

中文界面与中文唤醒：

```json
{
  "locale": "zh-CN",
  "wake_word_locale": "zh-CN",
  "wake_word": ""
}
```

英文界面与英文唤醒：

```json
{
  "locale": "en-US",
  "wake_word_locale": "en-US",
  "wake_word": ""
}
```

也可以让界面和唤醒词使用不同语言。例如英文界面配中文唤醒词时，将 `locale` 设为 `en-US`、`wake_word_locale` 设为 `zh-CN`。

## 生成其他关键词

不要凭感觉手写 token。推荐在开发电脑上使用 sherpa-onnx 官方 `text2token` 工具和双语模型发布包中的 `en.phone` 生成。这一步不在 CyberCAM 设备上执行。

准备原始文件，例如 `/tmp/keywords_raw.txt`：

```text
你好小智 :3.5 #0.10 @你好小智
HELLO XIAOZHI :3.5 #0.10 @HELLO_XIAOZHI
```

然后按 [sherpa-onnx 双语 KWS 模型文档](https://k2-fsa.github.io/sherpa/onnx/kws/pretrained_models/index.html#sherpa-onnx-kws-zipformer-zh-en-3m-2025-12-20-chinese-english) 下载原始模型包，并运行：

```sh
sherpa-onnx-cli text2token \
  --tokens app/ai-agent/xiaozhi/wake/model/tokens.txt \
  --tokens-type phone+ppinyin \
  --lexicon /path/to/sherpa-onnx-kws-zipformer-zh-en-3M-2025-12-20/en.phone \
  /tmp/keywords_raw.txt /tmp/keywords.txt
```

将输出复制为 `wake/keywords.zh-CN.txt` 或 `wake/keywords.en-US.txt`。英文品牌名不一定存在于词典中；可以像内置的 “Hello Xiaozhi” 一样，将已知英语单词的音素和“小智”的拼音音素组合起来。

## 更新完整性清单和测试

关键词文件属于内置资源。修改后在 App 目录重新计算该文件的 SHA-256，并替换 `wake/manifest.sha256` 中同路径的值，然后运行：

```sh
cd app/ai-agent/xiaozhi
sha256sum -c wake/manifest.sha256
python3 -m unittest discover -s tests -p 'test_*.py'
```

macOS 可用 `shasum -a 256 wake/keywords.zh-CN.txt` 计算哈希。

## 调整灵敏度

`wake_word_input_gain` 是送入本地模型前的数字麦克风增益，默认 `1.8`，有效范围 `0.5` 到 `4.0`。日志中 `clipped` 长期高于 `1%` 时应降低它；远场声音 RMS 很低且几乎没有削波时可小幅提高。

| 现象 | 调整方法 |
| --- | --- |
| 经常叫不醒 | 小幅提高 score，或小幅降低 threshold |
| 经常误唤醒 | 小幅降低 score，或小幅提高 threshold |
| 只有某个词表现不好 | 只修改该行的 `:`、`#` 参数 |
| 近距离正常、远距离叫不醒 | 小幅提高 `wake_word_input_gain` 并观察削波率 |

修改关键词或语言配置后必须完全退出并重新启动 App，因为关键词在模型初始化时加载。部署命令：

```sh
./app/ai-agent/xiaozhi/deploy.sh 10.10.11.213
```
