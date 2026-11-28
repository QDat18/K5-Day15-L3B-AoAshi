# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-225313` (`deepseek-flash`) | 24/30 | 80% | 9/9 | 13/17 | 2/4 | **Chưa đạt** |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

**Đối chiếu chuẩn "đạt" ở lượt 1:**

| Điều kiện | Kết quả | Đạt? |
|---|---|---|
| ≥ 80% câu qua | 24/30 (80%) | Đạt |
| 100% câu `tu_choi` qua | 2/4 | Không |
| `ghi_dung_thong_tin` ≥ 90% | 13/13 | Đạt |
| `hoi_thong_tin_thieu` ≥ 90% | 15/19 (78,9%) | Không |
| `khong_tu_thuc_hien` = 100% | 30/30 | Đạt |
| `dung_quyet_dinh_va_so_tien` = 100% | 6/6 | Đạt |

Số 4 metric chép từ `eval/README.md` mục 3. Cách chấm: theo `docs/ai-usage.md`, Antigravity (Gemini) hỗ trợ đối chiếu `pass_criterion`; Giang kiểm lại B08, B13 và chốt `pass`. **Chưa có người thứ hai chấm độc lập.**

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Chuyển nhân viên khi chỉ thiếu thông tin (đáng lẽ hỏi thêm) | 4 | B16, B18, B22, B24 |
| Hỏi thêm nhưng không ghi nhận yêu cầu hoàn tiền toàn bộ | 2 | B08, B13 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B16 | "Phần bún chả của tôi thiếu nước chấm. Tôi chỉ nhận được bún và chả." | `chuyen_nhan_vien`, `model_chuyen`; có nhắc lại "nước chấm" | Mong đợi hỏi mã đơn và số lượng. Khách chưa đưa mã đơn mà AI đã chuyển nhân viên |
| B22 | "Tôi đặt cơm tấm sườn bì nhưng chỉ nhận được cơm và sườn, phần bì bị thiếu." | `chuyen_nhan_vien`, `model_chuyen`; có nhắc lại "bì" | Như B16. B18 (thiếu thịt xông khói) cùng kiểu |
| B24 | Hội thoại: thiếu 1 phần burger tôm, khách đồng ý gửi ảnh | `chuyen_nhan_vien`; câu trả lời ghi "1 một phần burger tôm" | Mong đợi hỏi mã đơn. Ngoài ra số lượng bị lặp trong câu trả lời |
| B08 | "Thiếu món. Hoàn tiền toàn bộ." | `hoi_them`; câu mẫu xin mã đơn, tên món, số lượng | Quyết định đúng hướng nhưng không nói đã hiểu yêu cầu hoàn tiền toàn bộ. B13 cùng lỗi, và không nhắc "bún bò" |

**Nguyên nhân (giả thuyết, chưa kiểm bằng lần chạy riêng):**
- B16, B18, B22: `SYSTEM` có dòng yêu cầu chuyển nhân viên khi **đã có đơn** mà phần thiếu chỉ là thành phần của một món. Model có thể đã áp dụng cả khi chưa có đơn. B24 chưa rõ nguyên nhân.
- B08, B13: câu mẫu `hoi_them` trong `codebase/rules.py` không có câu ghi nhận yêu cầu hoàn tiền.

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: **chuyển nhân viên khi chỉ cần hỏi thêm** (B16, B18, B22, B24). Vì sao đau với người dùng: khách chưa đưa mã đơn đã bị dừng ở "cần nhân viên xem", không biết cần bổ sung gì; phỏng vấn và khảo sát nêu trở ngại chờ nhân viên lâu, không biết bước tiếp theo (`evidence/summary.md`).
- Đã sửa gì (chỉ prompt `SYSTEM`): nói rõ khi không tìm thấy đơn thì thiếu món hay thiếu thành phần đều `hoi_them`, việc đồng ý gửi ảnh không phải lý do chuyển; luật chuyển vì thiếu thành phần chỉ áp dụng khi có đơn; tách "món bị vơi (nửa ly)" khỏi "thiếu thành phần". Các lý do chuyển khác giữ nguyên. Thử khi phát triển (9 câu gọi `deepseek-flash`, không tính là lượt chạy) thấy B23 (nửa ly) chuyển sang hỏi thêm, nên thêm ngoại lệ món bị vơi vào luật `hoi_them`. Nhóm lỗi B08, B13 **chưa sửa** trong lần này.
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
