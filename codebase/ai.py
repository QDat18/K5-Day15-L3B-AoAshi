"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        if API_KEY:  # lỗi được ghi vào eval/run-N.csv (file được commit) nên che key trước khi cắt
            detail = detail.replace(API_KEY, "***")
        raise RuntimeError("HTTP %d: %s" % (e.code, detail[:300]))


def _chat(system, user):
    return ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]


def call_openai(system, user):
    data = post_json("https://api.openai.com/v1/chat/completions", {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": _chat(system, user)})
    usage = data["usage"]
    return data["choices"][0]["message"]["content"], usage["prompt_tokens"], usage["completion_tokens"]


def call_deepseek(system, user):
    # API theo định dạng OpenAI (api-docs.deepseek.com, xem 27/11/2026). Tắt "thinking" (mặc định bật, tốn thêm
    # token ra); bật JSON mode, chế độ này cần chữ "JSON" trong prompt (SYSTEM ở agent.py đã có). Nội dung rỗng
    # hay sai định dạng thì rules.parse_model_json trả None → chuyển nhân viên.
    data = post_json("https://api.deepseek.com/chat/completions", {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": _chat(system, user), "thinking": {"type": "disabled"},
                      "response_format": {"type": "json_object"}, "max_tokens": 1024})
    usage = data["usage"]
    return data["choices"][0]["message"]["content"] or "", usage["prompt_tokens"], usage["completion_tokens"]


def call_claude(system, user):
    data = post_json("https://api.anthropic.com/v1/messages",
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    return text, data["usage"]["input_tokens"], data["usage"]["output_tokens"]


def call_ollama(system, user):
    data = post_json("http://localhost:11434/api/chat", {},
                     {"model": MODEL_NAME, "messages": _chat(system, user), "stream": False}, timeout=300)
    return data["message"]["content"], data.get("prompt_eval_count", 0), data.get("eval_count", 0)


PROVIDERS = {"openai": call_openai, "deepseek": call_deepseek,"anthropic": call_claude, "ollama": call_ollama}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER not in PROVIDERS:
        raise NotImplementedError(
            "chưa viết phần gọi model thật cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md"
            % MODEL_PROVIDER)
    text, tokens_in, tokens_out = PROVIDERS[MODEL_PROVIDER](system, user)
    return {"text": text, "model": MODEL_NAME, "tokens_in": int(tokens_in), "tokens_out": int(tokens_out)}
