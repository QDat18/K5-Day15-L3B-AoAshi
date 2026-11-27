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


if __name__ == "__main__":
    unittest.main()
