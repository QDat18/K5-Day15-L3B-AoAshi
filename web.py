"""Web demo trên máy: python web.py [--port 8000]. Chỉ dùng thư viện chuẩn."""
import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))
sys.dont_write_bytecode = True

import ai
import tracing
from agent import answer


class Handler(BaseHTTPRequestHandler):
    def send_body(self, status, body, content_type="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_body(200, (ROOT / "web" / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/status":
            self.send_body(200, {"provider": ai.MODEL_PROVIDER, "model": ai.MODEL_NAME,
                                 "fake": ai.MODEL_PROVIDER == "fake"})
        elif self.path == "/favicon.ico":
            self.send_body(204, b"", "image/x-icon")
        else:
            self.send_body(404, {"error": "Không tìm thấy trang."})

    def do_POST(self):
        if self.path != "/api/answer":
            self.send_body(404, {"error": "Không tìm thấy API."})
            return
        # Không cho một website khác gọi API trên máy để tiêu tốn lượt model.
        origin = self.headers.get("Origin")
        expected_origin = "http://127.0.0.1:%d" % self.server.server_port
        if origin and origin != expected_origin:
            self.send_body(403, {"error": "Hãy mở demo bằng địa chỉ được in trong terminal."})
            return
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            self.send_body(415, {"error": "Yêu cầu cần có định dạng JSON."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 24000:
                raise ValueError("Kích thước yêu cầu không hợp lệ.")
            payload = json.loads(self.rfile.read(size))
            text = payload.get("text") if isinstance(payload, dict) else None
            if not isinstance(text, str) or not text.strip() or len(text) > 4000:
                raise ValueError("Nhập khiếu nại từ 1 đến 4.000 ký tự.")
        except (ValueError, UnicodeError) as exc:
            self.send_body(400, {"error": str(exc)})
            return
        started = time.perf_counter()
        tracing.begin("web-demo")
        try:
            result = answer(text.strip())
        except Exception:
            # Không trả nội dung lỗi API thô hoặc thông tin cấu hình ra trình duyệt.
            self.send_body(502, {"error": "Chưa gọi được model. Kiểm tra mạng, API key, tên model và hạn mức trong .env rồi thử lại."})
            return
        finally:
            summary, _ = tracing.end()
        self.send_body(200, {"output": result["output"], "stats": summary,
                             "elapsed": round(time.perf_counter() - started, 2),
                             "fake": ai.MODEL_PROVIDER == "fake"})

    def log_message(self, format, *args):
        # Chỉ ghi đường dẫn và mã HTTP, không ghi khiếu nại hay API key.
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    # Một luồng xử lý để bộ đếm trace toàn cục không bị trộn giữa các yêu cầu.
    try:
        server = HTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as exc:
        parser.exit(1, "Không mở được cổng: %s. Thử python web.py --port 8001\n" % exc)
    print("AoAshi: http://127.0.0.1:%d\nDung server: Ctrl+C" % args.port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
