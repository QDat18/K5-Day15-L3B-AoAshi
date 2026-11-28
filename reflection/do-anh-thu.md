# Reflection — Đỗ Anh Thư

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
   - Đội trưởng nhóm AoAshi: điều phối tiến độ, nộp các checkpoint, rà soát chéo tài liệu trước khi nộp và thuyết trình phần bằng chứng, bài toán & kết luận (trang 1–2, 7 trong `demo-slides.pdf` và `slides/outline.md`).
   - Phỏng vấn 3 người ngoài nhóm (`evidence/interviews/P1.md`–`P3.md`), gửi và tổng hợp khảo sát 21 phiếu (`evidence/survey/questions.md`, `evidence/survey/results.csv` — commit `e93e55c`), cập nhật `evidence/hypothesis.md`, `evidence/summary.md`, `canvas.md` dòng 4, `assets/p1-tro-giup.png` và `spec.md` §0–§2 cùng bảng impact (commit `17fb5a2`, `5029db1`, `1c2f9f4`).
   - Chấm thử độc lập 5 output ngẫu nhiên của `run-1` (khớp `5/5`), rà phần ẩn danh dữ liệu người trả lời ở `spec.md` §9, điền `spec.md` §10 (commit `77dcbde`), cập nhật `AGENTS.md` và `README.md` trước CP4 (commit `20f44ca`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   - Dùng Claude Code hỗ trợ gợi ý khung câu hỏi phỏng vấn/khảo sát ban đầu; sau đó tự chỉnh câu chữ cho sát ngữ cảnh đặt đồ ăn qua app và tự đi phỏng vấn, thu phiếu khảo sát thật.
   - Dùng Antigravity (Gemini) hỗ trợ đối chiếu `eval/metric_spec.yaml` và `traces/run-1.jsonl` khi chấm thử 5 output, kiểm tra xung đột merge ở `spec.md` §10, rà soát đồng bộ `README.md` và chuẩn bị ý trả lời cho buổi demo.
   - Chỗ phải tự kiểm và chỉnh lại: tự lọc lại các phiếu khảo sát mâu thuẫn trong `evidence/summary.md` và `canvas.md` (bỏ trích dẫn từ phiếu 21, bổ sung số đã lọc 7/12), đối chiếu giờ thật từ lịch sử git cho dòng changelog §10, và sửa câu chữ trong `README.md` cho khớp thực tế nhóm đã rà soát.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   - Câu `B08` (`"Thiếu món. Hoàn tiền toàn bộ."`, nhóm `tu_choi`) bị trượt ở cả `run-1` và `run-2`: AI chọn đúng hướng `hoi_them` để xin mã đơn, tên món và số lượng, nhưng câu trả lời mẫu chỉ hỏi thông tin mà không nhắc lại là đã ghi nhận yêu cầu hoàn tiền toàn bộ của khách nên không đạt `pass_criterion`.
   - Bài học rút ra là một câu trả lời AI tốt không chỉ cần đúng logic phân loại, mà phải thể hiện rõ cho người dùng biết hệ thống đã hiểu đúng yêu cầu của họ ở lượt đó. Ngoài ra, khi chưa sửa xong một nhóm lỗi thì cần giữ nguyên kết quả thực tế (28/30) và khai báo trung thực phần chưa đạt thay vì cố tối ưu cho đẹp số.
