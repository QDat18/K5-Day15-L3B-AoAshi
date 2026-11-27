# Data card — dữ liệu bản chạy thử D1 của AoAshi

## Dataset 1 · Đơn hàng giao đồ ăn giả lập

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | `data/orders.json` là nguồn của `get_order(order_id)`. Bản chạy thử tra đơn theo mã, dùng danh sách món để đối chiếu khiếu nại, rồi kiểm tra trạng thái giao và hoàn trước khi đề xuất xử lý. |
| Từ đâu | Hoàng Quang Đạt phụ trách. Claude Code hỗ trợ soạn dữ liệu cố định bằng script. Theo [`docs/ai-usage.md`](../docs/ai-usage.md), 8 đơn bổ sung `DH011`–`DH018` lấy tên món theo benchmark của nhóm. Nhóm tự đặt đơn giá. |
| Xử lý những bước gì | Lưu JSON UTF-8 theo mã đơn. Mỗi đơn có `trang_thai`, `da_hoan` và `mon`. Mỗi dòng món có mã, tên, số lượng đặt và đơn giá nguyên bằng VND. Các bước lọc, ẩn danh và chia tập không áp dụng cho dữ liệu được dựng từ đầu. |
| Số bản ghi | **18 đơn** (`DH001`–`DH018`), gồm **34 dòng món**. Có 17 đơn đã giao, trong đó 1 đơn đã hoàn, và 1 đơn đang giao. Nhóm 8 đơn bổ sung có 18 dòng món. |
| Phiên bản / ngày lấy | Nhánh `hoangquangdat`, commit `51fc1ea`, ngày 27/11/2026. |
| Nhãn | `synthetic`. Soạn thủ công với Claude Code. Seed không áp dụng. |
| Giới hạn | Dữ liệu phục vụ lát cắt khiếu nại thiếu món và có 8 đơn được dựng theo câu thử. Kết quả trên các đơn này phản ánh hiệu năng trong tình huống mô phỏng đã thiết kế. Thông tin món thực tế bị thiếu đến từ lời khách trong mỗi ca. |
| Kiểm tra | Codex đã kiểm tra tự động 18 đơn và 34 dòng món về cấu trúc, mã món duy nhất trong từng đơn, số lượng và đơn giá hợp lệ. Chưa ghi nhận người kiểm tay hoặc số dòng đã kiểm tay. |

## Dataset 2 · Cấu hình chính sách hoàn tiền giả lập

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | `data/policy.json` là nguồn của `get_policy()`. `codebase/rules.py` tính số tiền từ đơn giá và số lượng thiếu rồi so với hạn mức **100.000 VND**. Ca vượt hạn mức tạo phiếu nháp chuyển nhân viên. Đề xuất hoàn đủ điều kiện tạo bản nháp chờ nhân viên duyệt. |
| Từ đâu | Chính sách mẫu do nhóm tự đặt với Claude Code hỗ trợ, theo `docs/ai-usage.md`. Hoàng Quang Đạt phụ trách. |
| Xử lý những bước gì | Lưu một cấu hình JSON UTF-8 với các trường `han_muc_hoan_toi_da`, `ap_dung_cho` và `nguon`. Các bước lọc, ẩn danh và chia tập không áp dụng. |
| Số bản ghi | **1 cấu hình**, gồm **3 trường**. |
| Phiên bản / ngày lấy | Thêm tại commit `6eca5ac` ngày 27/11/2026 và có trong bản dữ liệu `51fc1ea`. |
| Nhãn | `synthetic`. Soạn thủ công với Claude Code. Seed không áp dụng. |
| Giới hạn | Hạn mức do nhóm đặt cho tình huống thiếu món trong demo. Các điều kiện kiểm tra trạng thái đơn, mã món và số lượng nằm trong `codebase/rules.py`. |
| Kiểm tra | Codex đã kiểm tra 1 cấu hình và đối chiếu hạn mức với cách code sử dụng. Chưa ghi nhận người kiểm tay. |

## Dataset 3 · UserSim (nguồn câu thử)

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Làm nguồn để soạn câu thử cho `eval/benchmark.csv`. |
| Từ đâu | [UserSim2026/UserSim trên Hugging Face](https://huggingface.co/datasets/UserSim2026/UserSim). Mã ca gốc được ghi trong cột `source`. |
| Xử lý những bước gì | Nhóm chọn tình huống, Việt hóa và điều chỉnh món hoặc bối cảnh khi cần, theo `eval/README.md`. |
| Số câu sử dụng | **12/30** câu ở commit `2e6547a` nhánh `vuongtruonggiang`. Các câu là B01, B03, B04, B06, B07, B08, B10, B11, B13, B14, B15 và B24. |
| Phiên bản / ngày lấy | Đối chiếu benchmark tại commit `2e6547a` ngày 27/11/2026. Phiên bản và ngày lấy dữ liệu gốc chưa được ghi nhận. |
| Nhãn / seed | `synthetic`. Benchmark ghi `tu_viet` cho các câu chuyển thể. Seed của nguồn gốc chưa kiểm. |
| Giới hạn / kiểm tra | Đã kiểm số câu theo cột `source`. Chưa kiểm từng câu với bản ghi gốc. Các câu phản ánh tình huống mô phỏng đã được điều chỉnh cho D1. |