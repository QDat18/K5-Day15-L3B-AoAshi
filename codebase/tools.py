"""Công cụ của bài toán — NHÓM VIẾT. Điền ở guide bước 2.2 (thiết kế) và 3.2 (code).

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace (tên, input, output rút gọn, thời gian, lỗi).

Số công cụ, kiểu công cụ do thiết kế của nhóm quyết định — có bài chỉ cần một công cụ tra cứu.
Công cụ có tác động ra ngoài: KHÔNG tự làm. Trả về bản nháp chờ người duyệt (guide bước 2.2, "chỗ người duyệt").
Dữ liệu công cụ đọc (bài mẫu, thông báo mẫu, lịch…): để trong data/ và mô tả ở data/DATA_CARD.md.
"""
import json
import os

from tracing import tool, TOOLS  # noqa: F401  (TOOLS: danh sách công cụ đã đăng ký, dùng khi viết vòng lặp agent)

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load(name: str) -> dict:
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


@tool
def get_order(order_id: str):
    """Tên: get_order. Input: mã đơn (str, vd DH001). Output: đơn giả lập {"trang_thai", "da_hoan", "mon"},
    hoặc None nếu không có. Tác động ra ngoài: không (chỉ đọc)."""
    return _load("orders.json").get(order_id)


@tool
def get_policy() -> dict:
    """Tên: get_policy. Input: không. Output: chính sách giả lập có "han_muc_hoan_toi_da" (đồng).
    Tác động ra ngoài: không (chỉ đọc)."""
    return _load("policy.json")


@tool
def draft_refund(order_id: str, items: list, amount: int) -> dict:
    """Tên: draft_refund. Input: mã đơn, danh sách món thiếu, số tiền. Output: bản nháp chờ nhân viên duyệt.
    Tác động ra ngoài: không (không hoàn tiền, không ghi file, không gửi gì)."""
    return {"loai": "nhap_hoan_tien", "trang_thai": "cho_nhan_vien_duyet",
            "order_id": order_id, "items": items, "amount": amount}


@tool
def escalate_to_staff(reason: str) -> dict:
    """Tên: escalate_to_staff. Input: mã lý do. Output: phiếu nháp chuyển nhân viên.
    Tác động ra ngoài: không (chưa gửi cho ai)."""
    return {"loai": "phieu_chuyen_nhan_vien", "trang_thai": "nhap", "reason": reason}
