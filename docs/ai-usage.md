# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Chưa dùng | Chưa viết code. Repo mới có khung starter-repo của BTC | | Hoàng Quang Đạt |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Mới gợi ý hướng thiết kế khi bàn phạm vi (AI chọn đề xuất / hỏi thêm / chuyển nhân viên, code kiểm hạn mức). Chưa viết prompt | Nhóm chọn lát cắt đơn giao thiếu món; thiết kế chi tiết chưa chốt | Hoàng Quang Đạt |
| Đào data (viết script đếm, gợi ý nhãn) | Chưa dùng cho bằng chứng | Mới gợi ý nguồn review và cách đếm, chưa lấy review nào | Chưa có dòng nào để kiểm | Võ Thanh Huy |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Gợi ý câu hỏi nháp khi bàn phạm vi. Chưa gửi bộ câu hỏi nào | Chưa rà | Đỗ Anh Thư |
| Viết câu thử (benchmark) | Codex, Claude Code | Codex soạn và Việt hóa câu thử theo dữ liệu giả lập; Claude Code đề xuất B26–B30 từ dữ liệu đơn và chính sách giả lập | Phụ trách rà input, expected, pass_criterion và nguồn trước khi chốt | Vương Trường Giang |
| Sinh data `synthetic` (nếu có) | Chưa dùng | Chưa sinh data | | |
| Chấm cột `pass` bằng LLM (nếu có) | Chưa dùng | Chưa chạy lượt đánh giá nào | | Vương Trường Giang |
| Slide, văn bản | Claude Code | Viết nháp `canvas.md` (bài toán, lát cắt, giả thuyết, mức tự động), chia phần việc trong `TEAMS.md`, điền mục khai báo này. Chưa làm slide | Nhóm chọn track D, lát cắt và cung cấp thông tin thành viên; câu chữ và phần chia việc cần cả nhóm rà lại | Cả nhóm |
| Chuẩn bị đề bài và repo | Claude Code | Đọc, tóm tắt bộ đề; hướng dẫn mốc CP1; chép starter-repo, điền tên nhóm / lớp / link, xoá mục 0 trong README, commit và push | Chưa ghi nhận người kiểm | Hoàng Quang Đạt |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
