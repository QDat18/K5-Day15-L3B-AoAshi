# Reflection — Võ Thanh Huy

> Bản nháp dựa trên phân công và tài liệu trong repo. Huy cần đọc lại, xác nhận phần việc thực tế và điều chỉnh phần tự nhận xét trước khi nộp.

1. Vai trò + phần mình làm (trỏ tới file / commit):

   Theo phân công của nhóm, tôi phụ trách đào review, mô phỏng chi phí và làm slide.
   Phần review được ghi ở [evidence/data-mining.md](../evidence/data-mining.md): mẫu gồm 30 đánh giá 1 sao, có 3 review báo rõ giao thiếu hàng hoặc thành phần.
   Phần chi phí nằm ở [cost/cost-estimate.md](../cost/cost-estimate.md), tổng hợp kết quả mô phỏng 50 phiên và ba kịch bản quy mô người dùng.
   Theo [slides/outline.md](../slides/outline.md), mình trình bày trang 6 về cách tính chi phí; cần phân biệt số token đo được với các giả định về quy mô và mức sử dụng.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

   Trong phiên làm việc này, dùng Codex để hỗ trợ tạo giao diện web demo và soạn bản nháp reflection.
   Web trong [web.py](../web.py) và [web/index.html](../web/index.html) gọi lại luồng xử lý của nhóm, có tình huống mẫu và thống kê token, thời gian.
   Điểm cần kiểm tra ở output AI là: chạy được với model giả chưa chứng minh được chất lượng phân loại khi gọi model thật; nhãn tình huống cũng không thay cho kết quả chạy.
   Với reflection, mình cần sửa những câu chưa đúng với việc mình thực sự làm; phần đào review phải giữ nguồn và số đếm thực tế, không để AI tự bổ sung bằng chứng.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

   Theo [eval/report.md](../eval/report.md), B08 có đầu vào “Thiếu món. Hoàn tiền toàn bộ.” và vẫn trượt ở lượt 2.
   Hệ thống hỏi thêm mã đơn, tên món và số lượng nhưng chưa ghi nhận yêu cầu hoàn tiền toàn bộ của khách, nên chưa đáp ứng tiêu chí chấm.
   Bài học mình rút ra là quyết định xử lý đúng hướng vẫn chưa đủ: câu trả lời cần thể hiện đã hiểu yêu cầu và giúp khách biết bước tiếp theo.
   Khi trình bày kết quả, cần nói rõ nhóm đạt 28/30 câu nhưng vẫn chưa đạt chuẩn chung vì còn hai câu `tu_choi` trượt; chi phí token thấp cũng chưa chứng minh được hiệu quả vận hành.
