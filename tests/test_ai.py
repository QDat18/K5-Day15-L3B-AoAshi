import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "codebase"))

import ai  # noqa: E402


class CallModel(unittest.TestCase):
    """Không gọi mạng: chỉ thay hàm gửi HTTP, phản hồi theo đúng dạng ở docs/connect-model.md."""

    def call(self, provider, response):
        post = mock.Mock(return_value=response)
        with mock.patch.object(ai, "MODEL_PROVIDER", provider), mock.patch.object(ai, "MODEL_NAME", "m-test"), \
                mock.patch.object(ai, "API_KEY", "khoa-gia-de-test"), mock.patch.object(ai, "post_json", post, create=True):
            return ai.call_model("he thong", "nguoi dung"), post

    def check(self, result):
        self.assertEqual(result, {"text": "xin chao", "model": "m-test", "tokens_in": 11, "tokens_out": 7})

    def test_openai_reads_text_and_usage(self):
        result, post = self.call("openai", {"choices": [{"message": {"content": "xin chao"}}],
                                            "usage": {"prompt_tokens": 11, "completion_tokens": 7}})
        self.check(result)
        url, headers, body = post.call_args.args[:3]
        self.assertEqual(url, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(headers, {"Authorization": "Bearer khoa-gia-de-test"})
        self.assertEqual([m["role"] for m in body["messages"]], ["system", "user"])

    def test_deepseek_uses_json_mode_without_thinking(self):
        result, post = self.call("deepseek", {"choices": [{"message": {"content": "xin chao"}}],
                                              "usage": {"prompt_tokens": 11, "completion_tokens": 7}})
        self.check(result)
        url, headers, body = post.call_args.args[:3]
        self.assertEqual(url, "https://api.deepseek.com/chat/completions")
        self.assertEqual(headers, {"Authorization": "Bearer khoa-gia-de-test"})
        self.assertEqual(body["model"], "m-test")
        self.assertEqual(body["thinking"], {"type": "disabled"})
        self.assertEqual(body["response_format"], {"type": "json_object"})
        self.assertEqual(body["max_tokens"], 1024)

    def test_anthropic_reads_text_and_usage(self):
        result, post = self.call("anthropic", {"content": [{"type": "text", "text": "xin chao"}],
                                               "usage": {"input_tokens": 11, "output_tokens": 7}})
        self.check(result)
        self.assertEqual(post.call_args.args[1]["x-api-key"], "khoa-gia-de-test")
        self.assertEqual(post.call_args.args[2]["system"], "he thong")

    def test_ollama_reads_text_and_usage(self):
        result, _ = self.call("ollama", {"message": {"content": "xin chao"},
                                         "prompt_eval_count": 11, "eval_count": 7})
        self.check(result)

    def test_unsupported_provider_says_so(self):
        with self.assertRaisesRegex(NotImplementedError, "gemini"):
            self.call("gemini", {})

    def test_fake_mode_makes_no_request(self):
        result, post = self.call("fake", {})
        self.assertEqual((result["model"], result["tokens_in"], result["tokens_out"]), ("fake", 0, 0))
        post.assert_not_called()


class HttpErrors(unittest.TestCase):
    def test_error_message_never_contains_the_key(self):
        """Lỗi được ghi vào cột error của eval/run-N.csv, file này được commit."""
        import io
        import urllib.error
        failure = urllib.error.HTTPError("u", 401, "no", {}, io.BytesIO(b"bad key khoa-gia-de-test"))
        with mock.patch.object(ai, "API_KEY", "khoa-gia-de-test"), \
                mock.patch("urllib.request.urlopen", side_effect=failure):
            with self.assertRaises(RuntimeError) as caught:
                ai.post_json("https://example.invalid", {}, {})
        self.assertIn("HTTP 401", str(caught.exception))
        self.assertNotIn("khoa-gia-de-test", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
