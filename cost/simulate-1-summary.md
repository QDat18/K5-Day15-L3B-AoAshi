# Tóm tắt mô phỏng simulate-1@20261128-110015

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| bao_thieu_it | 37 | 1 | 987 | 45 | 1.0 | 1.4 |
| bao_thieu_vua | 8 | 2 | 1980 | 98 | 2.0 | 2.9 |
| bao_thieu_nhieu | 5 | 3 | 2937 | 134 | 3.0 | 3.6 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-2@20261128-103935

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (10 người) | Chi phí / tháng — cơ sở (50 người) | Chi phí / tháng — cao (100 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash (vào 0.3 · ra 1.2 $/1M) | $0.00048 | $0.00051 | $0.00038 | $0.0101 | $0.0504 | $0.1009 | $0.0010 |
| deepseek-v4-pro (vào 1.32 · ra 3.96 $/1M) | $0.0020 | $0.0022 | $0.0016 | $0.0427 | $0.2133 | $0.4266 | $0.0043 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: deepseek-flash. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
