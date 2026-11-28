# Reflection — Hoàng Quang Đạt

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
Mình phụ trách phần kỹ thuật của bản chạy thử: nối model thật (`deepseek-flash`), giữ các chốt chặn rủi ro bằng code, chạy đánh giá hai lượt và chạy mô phỏng chi phí. Các file mình làm và trực tiếp kiểm gồm `codebase/agent.py`, `codebase/rules.py`, `codebase/tools.py`, `codebase/ai.py`, dữ liệu giả ở `data/orders.json`, `data/policy.json`, bộ test `tests/`, cùng các mục thiết kế và an toàn ở `spec.md` (§4–§6, §9). Ngoài ra mình chạy `eval/run-1.csv` (commit `0480e34`), `eval/run-2.csv` (commit `d84df48`) và `cost/simulate-1.csv` (commit `cc5323b`), đồng thời dựng thêm giao diện web nhỏ `demo_ui.py` để nhóm demo trực quan hơn.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
Mình dùng Claude Code để lên thiết kế, viết khung code, bộ test và sửa prompt trước lượt 2; dùng Antigravity để kiểm tra nối API thật, điền phần §5–§6, §9 của `spec.md`, đối chiếu chấm chéo 5 câu và làm `demo_ui.py`. Tuy nhiên AI không tự chạy hết được: mình phải tự cấu hình `.env`, test lỗi HTTP 401 khi mới nối DeepSeek và quyết định giữ nguyên luật cho hai câu `B08`, `B13` trước lượt 1 thay vì sửa vội. Lúc sửa prompt trước lượt 2, khi test thử 9 câu thì thấy câu `B23` (ly nước chỉ còn một nửa) bị đẩy nhầm sang hỏi thêm, nên phải thêm ngoại lệ riêng để giữ `B23` ở nhánh chuyển nhân viên.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
Mình nhớ nhất nhóm lỗi ở `B16`, `B18`, `B22` trong lượt 1 (ví dụ `B16`: khách báo bún chả thiếu nước chấm nhưng chưa đưa mã đơn). Vì prompt có dòng bảo chuyển nhân viên khi thiếu thành phần của một món, model áp dụng luôn kể cả lúc chưa tìm thấy đơn, làm khách chưa kịp đưa mã đơn đã bị đẩy đi. Bài học là viết prompt không chỉ ghi điều kiện cần kích hoạt, mà phải nói rõ điều kiện nào chưa đủ thì khoan hãy chuyển; nhờ sửa đúng chỗ này mà lượt 2 tăng từ 24/30 lên 28/30, còn hai câu `B08`, `B13` vẫn trượt thì giữ nguyên để ghi nhận trung thực và rút kinh nghiệm về việc câu mẫu cố định cần có thêm ý ghi nhận yêu cầu.

