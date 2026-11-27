# Đào data — cách đếm và kết quả

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Nguồn:** [Đánh giá sản phẩm Combo bánh tráng – Tiệm Bánh Tráng Cute trên Shopee](https://shopee.vn/product/635858058/24093715534).
- **Ngày xem:** 27/11/2026. Ngày đăng của các review trong mẫu từ 23/04/2025 đến 18/11/2026.
- **Cách lấy mẫu:** Chọn bộ lọc 1 sao, đọc 5 trang đầu theo thứ tự Shopee hiển thị, mỗi trang 6 review. Khoảng ngày đăng là phạm vi quan sát được của mẫu.
- **Đếm gì:** Đếm review kể rõ đơn bị giao thiếu hàng hoặc thành phần. Trong các review đó, đếm riêng những ca khách kể gặp khó khăn khi liên hệ xử lý phần thiếu, như không được trả lời, phản hồi chậm hoặc chờ gửi bù. Giao sai thành phần và nghi thiếu khối lượng được gắn nhãn riêng.
- **Mẫu số:** `N = 40`, gồm toàn bộ review đã đọc trong 5 trang, kể cả review về vấn đề khác. Khi tính tỷ lệ gặp khó khăn trong nhóm giao thiếu, dùng số ca giao thiếu làm mẫu số.
- **Công thức:** `Tỷ lệ giao thiếu = số review báo rõ giao thiếu / 30 × 100%`. `Tỷ lệ gặp khó khăn trong nhóm giao thiếu = số review báo giao thiếu và gặp khó khăn khi liên hệ / số review báo rõ giao thiếu × 100%`. Mỗi review được đếm một lần cho mỗi chỉ số.

## 2. Đọc trước, đếm sau

Đã đọc 30 review và ghi nhận ngày đăng, trang hiển thị và nội dung người mua kể. Các tình huống quan sát được:

- Khách báo giao thiếu rồi nhắn shop. Có người kể không được trả lời, có người chờ hai ngày, có người nhận phản hồi nhưng vẫn chờ gửi bù.
- Khách nhận thành phần khác với phân loại đã đặt.
- Khách nghi sản phẩm thiếu khối lượng. Các review khác nói về bao bì hoặc chất lượng sản phẩm.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---:|---:|---|
| Review báo rõ giao thiếu hàng hoặc thành phần | 3/30 | 10% | R01, R02, R03 |
| Review vừa báo giao thiếu vừa kể gặp khó khăn khi liên hệ xử lý | 3/30 | 10% | R01, R02, R03 |
| Trong nhóm báo giao thiếu, số review kể gặp khó khăn khi liên hệ xử lý | 3/3 | 100% | Mẫu số của dòng này là 3 ca giao thiếu. |

## 4. Năm ví dụ cụ thể đã ẩn danh

Các nội dung dưới đây được tóm tắt từ review. Số trang là vị trí trong bộ lọc 1 sao tại ngày xem.

| Mã | Ngày đăng | Trang | Nội dung người mua kể | Nhãn |
|---|---|---:|---|---|
| R01 | 18/06/2025 | 2 | Đơn giao thiếu hàng. Khách nhắn cho shop nhưng không được trả lời. | Giao thiếu, khó liên hệ |
| R02 | 18/11/2026 | 3 | Đơn giao thiếu. Khách kể đã nhắn hỏi và chờ hai ngày mới nhận được phản hồi. | Giao thiếu, phản hồi chậm |
| R03 | 30/08/2025 | 5 | Đơn giao thiếu. Khách kể shop phản hồi qua loa và sau khi chờ vẫn chưa nhận được phần bù. | Giao thiếu, chờ xử lý |
| R04 | 19/08/2025 | 4 | Khách đặt một hũ ớt và một hũ tắc nhưng nhận hai hũ tắc. | Giao sai thành phần |
| R05 | 16/07/2025 | 3 | Khách nhận một bịch và nghi chưa đủ 1 kg. | Nghi thiếu khối lượng |

## 5. Giới hạn của data

Mẫu gồm 30 đánh giá 1 sao của một sản phẩm đóng gói trên Shopee. Tỷ lệ trên mô tả mẫu review đã đọc. Bộ lọc 1 sao khiến mẫu nghiêng về trải nghiệm tiêu cực, và thứ tự hiển thị có thể thay đổi sau ngày thu thập. Review phản ánh lời kể của khách về việc liên hệ và chờ xử lý. Bối cảnh mua bánh tráng đóng gói cũng khác với đặt món giao tận nơi trong lát cắt D1.

**Cách kiểm lại:** Phỏng vấn người ngoài nhóm từng nhận đơn đồ ăn giao thiếu món. Hỏi họ đã báo sự cố qua đâu, đã phải nhắn lại bao nhiêu lần và chờ bao lâu để nhận phản hồi hoặc phương án xử lý.