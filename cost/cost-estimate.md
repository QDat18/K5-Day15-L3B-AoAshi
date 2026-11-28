# Chi phí khi dùng thật

## 1. Đầu vào

- `cost/personas.yaml` dùng ba nhóm báo thiếu món theo câu 4 trong `evidence/survey/results.csv`. Trong 9 người báo thiếu món, 7 người báo 1 lần, 1 người báo 2 lần và 1 người báo 5 lần trong tháng. Mỗi lần báo thiếu được tính thành một phiên. Giả định số lượt hỏi tương ứng là 1, 2 và 3 lượt/phiên.
- Quy mô thấp, cơ sở và cao lần lượt là 10, 50 và 100 người dùng/tháng. Nhóm tự ước tính quy mô.
- Giá theo cấu hình dùng cho lần chạy, tính bằng USD trên 1 triệu token. `deepseek-flash` có giá đầu vào 0,30 và đầu ra 1,20. `deepseek-v4-pro` có giá đầu vào 1,32 và đầu ra 3,96. Cấu hình ghi giá cao điểm, đầu vào cache miss, xem ngày 27/11/2026. [DeepSeek API Docs](https://api-docs.deepseek.com/quick_start/pricing/)
- Tỷ lệ đạt dùng để tính là **28/30 (93,3%)** từ [lượt 2 đã chấm](../eval/run-2.csv), run ID `run-2@20261128-103935`.
- Đo token trên `deepseek-flash` và áp hai bảng giá để so sánh. Dòng Pro là ước tính theo token đo trên Flash.

## 2. Kết quả mô phỏng

[CSV 50 phiên](simulate-1.csv) · run ID `simulate-1@20261128-110015` · seed 42 · **0/50 phiên lỗi**. Số liệu lấy từ [tóm tắt mô phỏng](simulate-1-summary.md) và [trace](../traces/simulate-1.jsonl).

| Model | USD/phiên | USD/task thành công | USD/tháng, 10 người | USD/tháng, 50 người | USD/tháng, 100 người | USD/người/tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| deepseek-flash (vào 0.3 · ra 1.2 /1M) | 0.00048 | 0.00051 | 0.0101 | 0.0504 | 0.1009 | 0.0010 |
| deepseek-v4-pro (vào 1.32 · ra 3.96 /1M) | 0.0020 | 0.0022 | 0.0427 | 0.2133 | 0.4266 | 0.0043 |

Chi phí mỗi task thành công bằng chi phí trung bình mỗi phiên chia cho 28/30. Tỷ lệ này đo theo câu thử và được dùng để ước tính chi phí mỗi task thành công. Bảng dựa trên chi phí token. Chi phí vận hành và thời gian nhân viên duyệt còn cần đo.

Chi phí mỗi tháng là tổng chi phí của ba nhóm người dùng. Với mỗi nhóm, lấy số người dùng trong kịch bản nhân với tỷ trọng nhóm, số phiên mỗi người dùng trong tháng và chi phí trung bình mỗi phiên của nhóm đó.

## 3. So với impact

`spec.md` §2 ước tính khoảng **26,4 phút xử lý/người gặp sự cố/tháng** trong mẫu khảo sát (238 phút ÷ 9 người). Ở kịch bản cơ sở, chi phí model ước tính là **0,0010 USD/người/tháng** với Flash và **0,0043 USD/người/tháng** nếu áp giá Pro trên token Flash. Phút xử lý hiện tại là căn cứ để thiết kế thử nghiệm đo thời gian tiết kiệm.

**Đề xuất tiếp tục cải tiến.** Chi phí token thấp trong các kịch bản đã mô phỏng. Cần đo thời gian tiết kiệm và công duyệt của nhân viên trước khi kết luận hiệu quả kinh tế.
