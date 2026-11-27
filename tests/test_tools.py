import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "codebase"))

import tools  # noqa: E402


class ReadTools(unittest.TestCase):
    def test_get_order_returns_items_with_price(self):
        self.assertEqual(tools.get_order("DH001")["mon"][0]["don_gia"], 35000)

    def test_get_order_unknown_id_returns_none(self):
        self.assertIsNone(tools.get_order("DH999"))

    def test_get_policy_has_refund_limit(self):
        self.assertEqual(tools.get_policy()["han_muc_hoan_toi_da"], 100000)


class DraftTools(unittest.TestCase):
    def test_draft_refund_waits_for_staff_approval(self):
        draft = tools.draft_refund("DH001", [], 35000)
        self.assertEqual(draft["trang_thai"], "cho_nhan_vien_duyet")
        self.assertEqual(draft["amount"], 35000)

    def test_escalate_keeps_reason_as_draft(self):
        ticket = tools.escalate_to_staff("vuot_han_muc")
        self.assertEqual((ticket["reason"], ticket["trang_thai"]), ("vuot_han_muc", "nhap"))


if __name__ == "__main__":
    unittest.main()
