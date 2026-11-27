"""Luật chặn rủi ro — code thuần, không gọi AI.

Nguyên tắc: code chỉ HẠ quyết định của model (đề xuất hoàn → hỏi thêm / chuyển nhân viên), không bao giờ nâng.
Số tiền do code tính từ đơn. Câu gửi khách lấy từ mẫu ở đây. Chữ duy nhất được chèn vào mẫu là tên món
đã lọc qua loc_mon_khach_neu: phải có sẵn trong tin của khách.
"""
import json
import re
import unicodedata

DECISIONS = ("de_xuat_hoan", "hoi_them", "chuyen_nhan_vien")

_ORDER_ID = re.compile(r"\bDH\s?(\d{3})\b", re.IGNORECASE)
_FENCE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL | re.IGNORECASE)


def tim_ma_don(text: str) -> list:
    """Các mã đơn trong tin, chuẩn hoá dạng DH001, bỏ trùng, giữ thứ tự."""
    return list(dict.fromkeys("DH" + number for number in _ORDER_ID.findall(text)))


def _valid_item(item) -> bool:
    if not isinstance(item, dict) or not isinstance(item.get("ma"), str):
        return False
    qty = item.get("so_luong")
    return isinstance(qty, int) and not isinstance(qty, bool) and qty >= 1


def parse_model_json(text: str):
    """JSON của model (trần hoặc bọc ```json). Sai định dạng → None."""
    body = (text or "").strip()
    fenced = _FENCE.match(body)
    if fenced:
        body = fenced.group(1)
    try:
        data = json.loads(body)
    except ValueError:
        return None
    if not isinstance(data, dict) or data.get("quyet_dinh") not in DECISIONS:
        return None
    items = data.get("mon_thieu")
    if not isinstance(items, list) or not all(_valid_item(i) for i in items):
        return None
    return data


# Tên "món" chứa các từ này đọc lên như lời xác nhận (đã hoàn, đã gửi, được duyệt) → không nhắc lại
_PROMISE_WORDS = {"đã", "hoàn", "tiền", "bồi", "duyệt", "gửi"}
_NUMBER_WORDS = ("một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười")
_MAX_ITEMS, _MAX_NAME = 5, 60


def _normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def _has_phrase(text: str, phrase: str) -> bool:
    return re.search(r"(?<!\w)%s(?!\w)" % re.escape(phrase), text) is not None


def _stated_quantity(qty, text: str):
    """Giữ số lượng chỉ khi khách có viết số đó (chữ số, hoặc chữ từ một đến mười)."""
    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
        return None
    words = [str(qty)] + ([_NUMBER_WORDS[qty - 1]] if qty <= len(_NUMBER_WORDS) else [])
    return qty if any(_has_phrase(text, word) for word in words) else None


def loc_mon_khach_neu(model, text: str) -> list:
    """Món khách nêu là thiếu, theo model, đã lọc: tên phải có trong tin. → [{"ten", "so_luong" | None}]."""
    raw = model.get("mon_khach_neu") if model else None
    if not isinstance(raw, list):
        return []
    message = _normalize(text)
    noted = {}
    for item in raw:
        name = item.get("ten") if isinstance(item, dict) else None
        if not isinstance(name, str):
            continue
        name = " ".join(name.split())
        key = _normalize(name)
        if (not key or len(name) > _MAX_NAME or key in noted or not _has_phrase(message, key)
                or _PROMISE_WORDS & set(re.findall(r"\w+", key))):
            continue
        noted[key] = {"ten": name, "so_luong": _stated_quantity(item.get("so_luong"), message)}
    return list(noted.values())[:_MAX_ITEMS]


def _result(decision: str, reason: str, amount: int = 0, items=None) -> dict:
    return {"quyet_dinh": decision, "so_tien": amount, "ly_do": reason, "mon": items or []}


def decide(model, order, so_ma_don: int, policy: dict) -> dict:
    """Quyết định cuối cùng. Khớp luật đầu tiên thì dừng."""
    if model is None:
        return _result("chuyen_nhan_vien", "khong_doc_duoc_model")
    if model["quyet_dinh"] == "chuyen_nhan_vien":
        return _result("chuyen_nhan_vien", "model_chuyen")
    if so_ma_don > 1:
        return _result("hoi_them", "nhieu_ma_don")
    if order is None:
        return _result("hoi_them", "khong_thay_don")
    if model["quyet_dinh"] == "hoi_them":
        return _result("hoi_them", "model_hoi_them")
    if order["da_hoan"]:
        return _result("chuyen_nhan_vien", "da_hoan")
    if order["trang_thai"] != "da_giao":
        return _result("chuyen_nhan_vien", "chua_giao")
    if not model["mon_thieu"]:
        return _result("hoi_them", "chua_ro_mon")

    missing = {}
    for item in model["mon_thieu"]:  # cộng dồn để model không lặp mã món mà vượt số đã đặt
        missing[item["ma"]] = missing.get(item["ma"], 0) + item["so_luong"]
    ordered = {item["ma"]: item for item in order["mon"]}
    if any(code not in ordered or qty > ordered[code]["so_luong"] for code, qty in missing.items()):
        return _result("chuyen_nhan_vien", "mon_khong_khop")

    amount = sum(ordered[code]["don_gia"] * qty for code, qty in missing.items())
    if amount > policy["han_muc_hoan_toi_da"]:
        return _result("chuyen_nhan_vien", "vuot_han_muc")
    items = [{"ten": ordered[code]["ten"], "so_luong": qty} for code, qty in missing.items()]
    return _result("de_xuat_hoan", "hop_le", amount, items)


def _list_items(noted) -> str:
    return ", ".join("%d %s" % (i["so_luong"], i["ten"]) if i["so_luong"] else i["ten"] for i in noted)


def _ask_message(result: dict, noted) -> str:
    if result["ly_do"] == "nhieu_ma_don":
        return "Bạn gửi lại một tin chỉ có một mã đơn và nói rõ món bị thiếu nhé."
    missing = []
    if result["ly_do"] == "khong_thay_don":
        missing.append("mã đơn (dạng DH001)")
    if any(not item["so_luong"] for item in noted):
        missing.append("số lượng")
    if not noted or not missing:
        return "Bạn gửi lại một tin có mã đơn (dạng DH001), tên món bị thiếu và số lượng nhé."
    # Không lưu hội thoại nên phải xin lại đủ trong một tin
    return ("Mình còn cần: %s. Bạn gửi lại một tin có đủ món bị thiếu và thông tin này nhé."
            % ", ".join(missing))


def _message(result: dict, noted) -> str:
    if result["quyet_dinh"] == "de_xuat_hoan":
        items = ", ".join("%d %s" % (i["so_luong"], i["ten"]) for i in result["mon"])
        money = format(result["so_tien"], ",").replace(",", ".")
        return ("Mình đề xuất hoàn %sđ cho %s. Đề xuất đang chờ nhân viên duyệt, tiền chưa được hoàn."
                % (money, items))
    if result["ly_do"] == "nhieu_ma_don":
        noted = ()
    heard = "Mình hiểu bạn báo thiếu: %s. " % _list_items(noted) if noted else ""
    if result["quyet_dinh"] == "hoi_them":
        return heard + _ask_message(result, noted)
    return heard + "Trường hợp này cần nhân viên xem. Hiện chưa có khoản hoàn hay mức bồi thường nào được xác nhận."


def render(result: dict, noted=()) -> str:
    """3 dòng đầu để chấm bằng code, sau đó là câu gửi khách. noted: kết quả của loc_mon_khach_neu."""
    return "QUYET_DINH: %s\nSO_TIEN: %d\nLY_DO: %s\n%s" % (
        result["quyet_dinh"], result["so_tien"], result["ly_do"], _message(result, noted))
