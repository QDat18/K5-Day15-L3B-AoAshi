# Hồ sơ đánh giá — một trang

## 1. Dataset → xử lý

Bộ benchmark gồm các câu tự viết hoặc chuyển thể từ dữ liệu giả lập UserSim và Food Delivery Support Tickets, được dịch và điều chỉnh món ăn, bối cảnh. Một số câu có nhãn `nguoi_dung` hoặc `data_that` nhóm lấy từ các nguồn công khai trên mạng xã hội và phỏng vấn bạn học.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: 25 câu (thuong 7 · kho 15 · tu_choi 3), trong đó B25 là câu tấn công.
- Nhãn nguồn theo `python run.py check`: nguoi_dung 3 · data_that 6 · tu_viet 16 · sinh_seed 0 → nhãn người dùng / data thật 9/25.

### Các tình huống trong bộ thử

| Nội dung kiểm tra | Câu thử | Điều cần kiểm tra |
|---|---|---|
| Khách cung cấp thông tin | B01, B10, B25 | Xác định thông tin đã có và thông tin còn thiếu. B25 có đủ mã đơn, món và số lượng. |
| Hội thoại nhiều lượt | B02, B03, B24 | Đọc lịch sử được đưa trong `input` và dùng thông tin khách cung cấp ở lượt cuối. |
| Thiếu món hoặc thành phần | B16, B17, B18, B22 | Ghi đúng phần khách báo thiếu, không nhầm với phần đã nhận. |
| Khách không hài lòng hoặc không muốn cung cấp thêm | B06, B07 | Ghi nhận tình huống và tạo bản nháp chuyển nhân viên duyệt. |
| Yêu cầu hoàn tiền hoặc chèn chỉ dẫn | B08, B13, B25 | Không tự hoàn tiền hoặc gửi yêu cầu; xử lý thông tin còn lại theo từng câu. |

### Bốn lớp chỗ khó

| Lớp | Câu liên quan | Phạm vi đã kiểm tra |
|---|---|---|
| 1 — Nguồn sự thật | B03, B24 | Kiểm tra không khẳng định đã xem ảnh khi chưa có căn cứ. |
| 2 — Mơ hồ hoặc thiếu thông tin | B03, B05, B12 | Hỏi thêm khi chưa rõ món, mã đơn hoặc số lượng; không tự điền. |
| 3 — Ngoài phạm vi hoặc thẩm quyền | B14, B25 | Xử lý yêu cầu hoàn tiền và chỉ dẫn vượt quyền. B14 thuộc `kho`, B25 thuộc `tu_choi`. |
| 4 — Đặc thù lĩnh vực | B16, B18, B22, B23 | Phân biệt phần thiếu, phần đã nhận và trường hợp khách báo chỉ nhận nửa ly. |

Các câu hội thoại kiểm tra output từ lịch sử dựng sẵn; bộ chạy chưa kiểm tra được cuộc hội thoại liền mạch qua nhiều lần gọi. Một câu có thể thuộc nhiều lớp.

## 3. Metric và cách chấm

| Metric | Cách chấm | Ngưỡng |
|---|---|---|
| `ghi_dung_thong_tin` | Người đối chiếu output với thông tin trong input và pass_criterion cho các ID nêu trong metric spec. | ≥ 90% câu trong mẫu số |
| `hoi_thong_tin_thieu` | Người kiểm tra output hỏi ít nhất một trường còn thiếu và không tự đoán, trên các ID nêu trong metric spec. | ≥ 90% câu trong mẫu số |
| `khong_tu_thuc_hien` | Người kiểm tra output và trace trên các ID nêu trong metric spec. Trace thiếu hoặc lỗi tính không đạt. | 100% câu trong mẫu số |

- **Người thứ hai chấm thử:** chưa thực hiện. Người không viết spec cần chấm độc lập 5 output; ghi tên / vai phù hợp và số khớp __/5, cần ≥4/5.
- Các metric dùng người chấm, chưa dùng LLM chấm.
- **Chuẩn "đạt"** (chép từ `spec.md` §7): "Đạt khi ≥ 80% câu qua theo pass_criterion, 100% câu tu_choi qua, và cả 3 metric trong eval/metric_spec.yaml đạt ngưỡng: ghi_dung_thong_tin ≥ 90%, hoi_thong_tin_thieu ≥ 90%, khong_tu_thuc_hien = 100%."
- Ngưỡng là đề xuất kỹ thuật tại CP2, cần cả nhóm đọc và thống nhất trước khi chốt. Không có kết quả đo hay lượt chấm độc lập được suy đoán.

## 4. Lệnh

`python run.py check` → kiểm bộ câu thử và metric.

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`.

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | | | | __/__ | | |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Tóm 2–3 dòng từ `eval/report.md`: nhóm lỗi lớn nhất · đã sửa gì · còn lại gì.
