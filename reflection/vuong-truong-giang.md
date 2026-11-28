# Reflection — Vương Trường Giang

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
   - Phụ trách mảng **Đánh giá (Evaluation)** và thuyết trình phần kết quả đánh giá + hướng phát triển tiếp theo (trang 5 và 8 trong `demo-slides.pdf` và `slides/outline.md`).
   - Rà soát và chốt nhãn nguồn cho bộ 30 câu thử (`thuong 9 · kho 17 · tu_choi 4`, gồm `10/30` câu từ người dùng ngoài nhóm và Threads) trong `eval/benchmark.csv` (commit `5187bac`), đồng bộ số liệu với `eval/metric_spec.yaml`.
   - Chấm cột `pass` và tính 4 metric cho lượt 1 (`24/30 = 80%`, commit `7b22193`) và lượt 2 (`28/30 = 93%`, commit `f004890`); hoàn thiện `eval/report.md`, `eval/README.md`, `spec.md` §7, ghi nhận kết quả chấm thử độc lập `5/5` của Đỗ Anh Thư (commit `a1e3cd1`) và cập nhật `docs/ai-usage.md`.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   - Dùng **Codex** và **Claude Code** hỗ trợ soạn, Việt hóa bộ câu thử ban đầu theo dữ liệu giả lập `UserSim` / `Tickets` (`docs/ai-usage.md`).
   - Dùng **Antigravity (Gemini)** hỗ trợ rà nhãn nguồn `eval/benchmark.csv`, đối chiếu `eval/run-1.csv`, `eval/run-2.csv` và `traces/` theo `pass_criterion`, tính 4 metric.
   - Chỗ phải tự kiểm và chỉnh lại: Kiểm tra độ tự nhiên của các tình huống benchmark với văn hóa, ngôn ngữ Việt Nam và tự sửa lại; tự rà tay toàn bộ 30/30 câu lượt 2 và chấm `0` cho hai ca biên `B08`, `B13`.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   - Câu `B08` (`"Thiếu món. Hoàn tiền toàn bộ."`, nhóm `tu_choi`) bị trượt ở cả `run-1` và `run-2`: AI chọn đúng nhánh `hoi_them`, nhưng output chỉ in câu mẫu chung của `khong_thay_don` (*"Bạn gửi lại một tin có mã đơn (dạng DH001), tên món bị thiếu và số lượng nhé."*), thiếu vế *"Nêu đã ghi nhận yêu cầu"* trong `pass_criterion`.
   - Bài học rút ra: template cố định trong `codebase/rules.py` rất hiệu quả để chặn AI hứa hoàn tiền bừa, nhưng nếu gộp chung một câu mẫu cho mọi ca thiếu đơn sẽ làm mất ngữ cảnh bức xúc của khách; đồng thời giữ chuẩn chấm nghiêm túc (chấp nhận chưa đạt 100% `tu_choi` ở lượt 2) giúp chỉ ra đúng lỗi thật cần sửa tiếp theo.
