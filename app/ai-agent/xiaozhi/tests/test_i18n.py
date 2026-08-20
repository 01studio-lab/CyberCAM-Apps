import unittest

from i18n import (
    Localizer,
    default_wake_word,
    normalize_locale,
    resolve_locale,
    resolve_wake_locale,
)


class LocalizationTests(unittest.TestCase):
    def test_locale_aliases_are_normalized(self):
        self.assertEqual(normalize_locale("zh_CN.UTF-8"), "zh-CN")
        self.assertEqual(normalize_locale("en_GB.UTF-8"), "en-US")

    def test_auto_locale_follows_posix_environment(self):
        self.assertEqual(resolve_locale("auto", {"LANG": "en_US.UTF-8"}), "en-US")
        self.assertEqual(resolve_locale("auto", {"LANG": "C.UTF-8"}), "zh-CN")

    def test_unknown_locale_falls_back_to_chinese(self):
        self.assertEqual(resolve_locale("fr-FR", {}), "zh-CN")

    def test_wake_word_and_ui_follow_locale(self):
        english = Localizer("en-US")
        self.assertEqual(default_wake_word(english.locale), "Hello Xiaozhi")
        self.assertEqual(
            english.text("wake_prompt", phrase="Hello Xiaozhi"),
            "Say “Hello Xiaozhi”",
        )

    def test_legacy_explicit_wake_word_keeps_matching_model_locale(self):
        self.assertEqual(resolve_wake_locale("auto", "en-US", "你好小智"), "zh-CN")
        self.assertEqual(
            resolve_wake_locale("auto", "zh-CN", "Hello Xiaozhi"), "en-US"
        )
        self.assertEqual(resolve_wake_locale("en-US", "zh-CN", "你好小智"), "en-US")


if __name__ == "__main__":
    unittest.main()
