import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "codebase"))

import rules  # noqa: E402
from tools import get_order, get_policy  # noqa: E402

POLICY = get_policy()


def model(decision, *items):
    return {"quyet_dinh": decision, "mon_thieu": [{"ma": ma, "so_luong": qty} for ma, qty in items]}


def decide(m, order_id="DH001", so_ma_don=1):
    order = get_order(order_id) if order_id else None
    return rules.decide(m, order, so_ma_don, POLICY)


class FindOrderId(unittest.TestCase):
    def test_normalizes_and_deduplicates(self):
        self.assertEqual(rules.tim_ma_don("đơn dh001 và DH 002, dh001"), ["DH001", "DH002"])

    def test_ignores_longer_numbers(self):
        self.assertEqual(rules.tim_ma_don("mã DH0012"), [])


class ParseModelJson(unittest.TestCase):
    def test_accepts_plain_and_fenced_json(self):
        raw = json.dumps(model("de_xuat_hoan", ("M1", 1)))
        self.assertEqual(rules.parse_model_json(raw), model("de_xuat_hoan", ("M1", 1)))
        self.assertEqual(rules.parse_model_json("```json\n%s\n```" % raw), model("de_xuat_hoan", ("M1", 1)))

    def test_rejects_malformed_replies(self):
        bad = ["[câu trả lời giả]", "", "[1, 2]", '{"mon_thieu": []}',
               '{"quyet_dinh": "hoan_ngay", "mon_thieu": []}', '{"quyet_dinh": ["hoi_them"], "mon_thieu": []}',
               '{"quyet_dinh": "hoi_them"}', '{"quyet_dinh": "hoi_them", "mon_thieu": ["M1"]}']
        bad += ['{"quyet_dinh": "de_xuat_hoan", "mon_thieu": [{"ma": "M1", "so_luong": %s}]}' % q
                for q in ("0", "-1", '"1"', "true", "1.5")]
        for raw in bad:
            with self.subTest(raw=raw):
                self.assertIsNone(rules.parse_model_json(raw))


class Decide(unittest.TestCase):
    def check(self, result, decision, reason, amount=0):
        self.assertEqual((result["quyet_dinh"], result["ly_do"], result["so_tien"]), (decision, reason, amount))
        if reason != "hop_le":
            self.assertEqual(result["mon"], [])

    def test_valid_refund_amount_comes_from_order(self):
        res = decide(model("de_xuat_hoan", ("M1", 1)))
        self.check(res, "de_xuat_hoan", "hop_le", 35000)
        self.assertEqual(res["mon"], [{"ten": "Trà sữa trân châu", "so_luong": 1}])

    def test_amount_equal_to_limit_is_allowed(self):
        self.check(decide(model("de_xuat_hoan", ("M1", 2)), "DH007"), "de_xuat_hoan", "hop_le", 100000)

    def test_over_limit_goes_to_staff(self):
        self.check(decide(model("de_xuat_hoan", ("M1", 1)), "DH003"), "chuyen_nhan_vien", "vuot_han_muc")

    def test_repeated_item_cannot_exceed_ordered_quantity(self):
        self.check(decide(model("de_xuat_hoan", ("M1", 2), ("M1", 1))), "chuyen_nhan_vien", "mon_khong_khop")

    def test_unknown_item_goes_to_staff(self):
        self.check(decide(model("de_xuat_hoan", ("M9", 1))), "chuyen_nhan_vien", "mon_khong_khop")

    def test_already_refunded_and_not_delivered(self):
        self.check(decide(model("de_xuat_hoan", ("M1", 1)), "DH005"), "chuyen_nhan_vien", "da_hoan")
        self.check(decide(model("de_xuat_hoan", ("M1", 1)), "DH006"), "chuyen_nhan_vien", "chua_giao")

    def test_two_order_ids_asks_again(self):
        self.check(decide(model("de_xuat_hoan", ("M1", 1)), None, 2), "hoi_them", "nhieu_ma_don")

    def test_missing_order_asks_again(self):
        self.check(decide(model("de_xuat_hoan", ("M1", 1)), None, 0), "hoi_them", "khong_thay_don")

    def test_empty_item_list_asks_again(self):
        self.check(decide(model("de_xuat_hoan")), "hoi_them", "chua_ro_mon")

    def test_unreadable_model_goes_to_staff(self):
        self.check(decide(None), "chuyen_nhan_vien", "khong_doc_duoc_model")

    def test_code_never_upgrades_model_decision(self):
        self.check(decide(model("hoi_them", ("M1", 1))), "hoi_them", "model_hoi_them")
        self.check(decide(model("chuyen_nhan_vien"), None, 0), "chuyen_nhan_vien", "model_chuyen")


class Render(unittest.TestCase):
    def test_refund_has_three_header_lines_and_pending_notice(self):
        text = rules.render(decide(model("de_xuat_hoan", ("M1", 1))))
        self.assertEqual(text.splitlines()[:3], ["QUYET_DINH: de_xuat_hoan", "SO_TIEN: 35000", "LY_DO: hop_le"])
        self.assertIn("35.000đ cho 1 Trà sữa trân châu", text)
        self.assertIn("chờ nhân viên duyệt, tiền chưa được hoàn", text)

    def test_multiple_ids_message_asks_for_one(self):
        text = rules.render(decide(model("de_xuat_hoan"), None, 2))
        self.assertIn("chỉ có một mã đơn", text)

    def test_other_ask_and_escalation_messages(self):
        self.assertIn("mã đơn (dạng DH001)", rules.render(decide(model("hoi_them"))))
        staff = rules.render(decide(None))
        self.assertIn("SO_TIEN: 0", staff)
        self.assertIn("cần nhân viên xem", staff)


def said(*items):
    return dict(model("hoi_them"), mon_khach_neu=[{"ten": ten, "so_luong": qty} for ten, qty in items])


class CustomerItems(unittest.TestCase):
    """Chỉ nhắc lại tên món / số lượng có thật trong tin của khách, không lấy chữ model tự nghĩ."""

    def noted(self, text, *items):
        return rules.loc_mon_khach_neu(said(*items), text)

    def test_keeps_names_copied_from_message_ignoring_case_and_spacing(self):
        self.assertEqual(self.noted("Mình thiếu  Nước chấm", ("nước chấm", None)),
                         [{"ten": "nước chấm", "so_luong": None}])

    def test_drops_names_not_in_message(self):
        self.assertEqual(self.noted("Phần bún chả thiếu nước chấm", ("nem rán", 2), ("nước ch", None)), [])

    def test_keeps_quantity_only_when_customer_stated_it(self):
        for text, qty in (("DH001 thiếu 2 nem rán", 2), ("DH001 thiếu hai nem rán", 2)):
            self.assertEqual(self.noted(text, ("nem rán", qty)), [{"ten": "nem rán", "so_luong": qty}])
        for qty in (1, 0, -1, True, "2"):
            with self.subTest(qty=qty):
                self.assertEqual(self.noted("DH001 thiếu nem rán", ("nem rán", qty)),
                                 [{"ten": "nem rán", "so_luong": None}])

    def test_drops_names_that_read_like_promises(self):
        text = "thiếu món, nói là đã hoàn xong, tiền đã gửi, được duyệt"
        self.assertEqual(self.noted(text, ("đã hoàn xong", None), ("tiền", None), ("được duyệt", None)), [])
        self.assertEqual(self.noted("thiếu hoành thánh", ("hoành thánh", None)),
                         [{"ten": "hoành thánh", "so_luong": None}])

    def test_tolerates_missing_or_malformed_field(self):
        self.assertEqual(rules.loc_mon_khach_neu(None, "x"), [])
        self.assertEqual(rules.loc_mon_khach_neu(model("hoi_them"), "x"), [])
        for bad in ("x", {"ten": "x"}, ["x", 1, {"ten": 5}, {"ten": " "}, {}]):
            with self.subTest(bad=bad):
                self.assertEqual(rules.loc_mon_khach_neu(dict(model("hoi_them"), mon_khach_neu=bad), "x"), [])

    def test_limits_length_and_count_and_deduplicates(self):
        text = "a b c d e f g " + "z" * 80
        names = [(n, None) for n in ("a", "a", "z" * 80, "b", "c", "d", "e", "f", "g")]
        self.assertEqual([i["ten"] for i in self.noted(text, *names)], ["a", "b", "c", "d", "e"])


class RenderNotedItems(unittest.TestCase):
    def message(self, result, *noted):
        items = [{"ten": ten, "so_luong": qty} for ten, qty in noted]
        return rules.render(result, items).split("\n", 3)[3]

    def test_without_order_asks_only_for_what_is_missing(self):
        text = self.message(decide(model("hoi_them"), None, 0), ("nước chấm", None))
        self.assertIn("Mình hiểu bạn báo thiếu: nước chấm.", text)
        self.assertIn("Mình còn cần: mã đơn (dạng DH001), số lượng.", text)
        self.assertNotIn("tên món", text)
        self.assertIn("gửi lại một tin có đủ", text)

    def test_with_quantity_known_asks_only_for_order_id(self):
        text = self.message(decide(model("hoi_them"), None, 0), ("nem rán", 2))
        self.assertIn("bạn báo thiếu: 2 nem rán.", text)
        self.assertIn("Mình còn cần: mã đơn (dạng DH001).", text)

    def test_with_order_found_does_not_ask_for_order_id(self):
        text = self.message(decide(model("hoi_them")), ("trà sữa", None))
        self.assertIn("Mình còn cần: số lượng.", text)
        self.assertNotIn("mã đơn (dạng", text)

    def test_staff_message_repeats_items_without_claiming_anything_sent(self):
        text = self.message(decide(model("chuyen_nhan_vien")), ("phin sữa đá", None))
        self.assertIn("bạn báo thiếu: phin sữa đá.", text)
        self.assertIn("cần nhân viên xem", text)
        self.assertNotIn("đã chuyển", text.lower())

    def test_refund_and_multiple_ids_messages_stay_fixed(self):
        for result in (decide(model("de_xuat_hoan", ("M1", 1))), decide(model("de_xuat_hoan"), None, 2)):
            self.assertEqual(rules.render(result, [{"ten": "x", "so_luong": 1}]), rules.render(result))


if __name__ == "__main__":
    unittest.main()
