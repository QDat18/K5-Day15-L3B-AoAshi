# Data Card — dữ liệu bản chạy thử D1 của AoAshi

## Dataset 1 · Đơn hàng giao đồ ăn giả lập

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | `data/orders.json` là nguồn của `get_order(order_id)` trong `codebase/tools.py`. Bản chạy thử tra trạng thái đơn, trạng thái đã hoàn, danh sách món, số lượng và đơn giá để xử lý khiếu nại thiếu món. |
| Từ đâu | Hoàng Quang Đạt phụ trách. Claude Code hỗ trợ soạn thủ công các đơn mẫu bằng script. Dữ liệu được khai báo trong `docs/ai-usage.md`. |
| Xử lý những bước gì | Mỗi đơn có mã `DH001`–`DH010`, trạng thái giao, cờ `da_hoan` và danh sách món. Mỗi món có mã, tên, số lượng đặt và đơn giá bằng VND. Chương trình đọc JSON UTF-8 và tra theo mã đơn. Dữ liệu được dựng từ đầu nên các bước lọc, ẩn danh và chia tập không áp dụng. |
| Số dòng / số đoạn | 10 bản ghi đơn hàng, gồm 16 dòng món. Có 9 đơn đã giao, trong đó 1 đơn đã hoàn, và 1 đơn đang giao. |
| Phiên bản / ngày lấy | Bản CP2 tại commit `6eca5ac`, ngày 27/11/2026. |
| Nhãn | `synthetic`. |
| Giới hạn | Mẫu nhỏ với các tình huống do nhóm chọn để chạy thử. Dữ liệu mô tả món đã đặt và trạng thái đơn. Thông tin món bị thiếu đến từ lời khách trong từng ca thử. |

**Cách sinh và kiểm tra:** Soạn thủ công với Claude Code, không sinh ngẫu nhiên nên seed không áp dụng. Khi soạn Data Card, đã kiểm tra bằng Python toàn bộ 10 đơn và 16 dòng món về cấu trúc, mã món trong từng đơn, số lượng và đơn giá. Commit chưa ghi nhận thành viên kiểm tay hay số dòng đã kiểm tay.

## Dataset 2 · Chính sách xử lý thiếu món giả lập

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | `data/policy.json` là nguồn của `get_policy()` trong `codebase/tools.py`. `codebase/rules.py` dùng hạn mức từ file này để kiểm tra số tiền đề xuất hoàn. |
| Từ đâu | Hoàng Quang Đạt phụ trách. Nhóm tự đặt chính sách mẫu với sự hỗ trợ của Claude Code, ghi trong `docs/ai-usage.md`. |
| Xử lý những bước gì | Chương trình đọc JSON UTF-8. Code tính số tiền từ đơn giá nhân số lượng thiếu, rồi so với hạn mức 100.000 VND. Nếu vượt hạn mức, hệ thống tạo phiếu nháp chuyển nhân viên. Nếu đủ điều kiện, hệ thống tạo đề xuất hoàn chờ duyệt. |
| Số dòng / số đoạn | 1 bản ghi cấu hình gồm 3 trường: `han_muc_hoan_toi_da`, `ap_dung_cho` và `nguon`. |
| Phiên bản / ngày lấy | Bản CP2 tại commit `6eca5ac`, ngày 27/11/2026. |
| Nhãn | `synthetic`. |
| Giới hạn | Cấu hình chỉ áp dụng cho tình huống thiếu món trong demo. Mức 100.000 VND do nhóm đặt. Các kiểm tra về món, số lượng và trạng thái đơn nằm trong `codebase/rules.py`. |

**Cách sinh và kiểm tra:** Soạn thủ công, seed không áp dụng. Khi soạn Data Card, đã kiểm tra 1 bản ghi cấu hình và đối chiếu hạn mức với cách code sử dụng. Commit chưa ghi nhận thành viên kiểm tay nội dung chính sách.

Bằng chứng về khó khăn khi khách báo giao thiếu được ghi riêng trong `evidence/data-mining.md`.