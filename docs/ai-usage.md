# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/agent.py`, `tools.py`, `rules.py`, phần gọi model trong `ai.py` (theo `docs/connect-model.md`; DeepSeek theo tài liệu chính thức) và test trong `tests/`. Sau khi đối chiếu với benchmark: thêm trường `mon_khach_neu` và bộ lọc tên món, câu trả lời nhắc lại món khách nêu, phiếu chuyển nhân viên giữ tin của khách. Model vẫn ở chế độ giả, chưa gọi model thật | Đạt duyệt thiết kế; code chưa ghi nhận người kiểm | Hoàng Quang Đạt |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn thiết kế workflow, luật chặn rủi ro và bản đầu của `SYSTEM`. Chưa thử với model thật | Đạt duyệt thiết kế; chưa ghi nhận người kiểm nội dung `SYSTEM` | Hoàng Quang Đạt |
| Sơ đồ kiến trúc (`assets/so_do_kien_truc.svg`) | Claude Code | Vẽ sơ đồ hoạt động theo `codebase/agent.py`, `rules.py` bằng script tạm; so điều kiện gộp trên sơ đồ với `rules.decide` ở 154 tổ hợp đầu vào (chỉ so quyết định cuối, không so `LY_DO`) | Đạt xem hình, yêu cầu vẽ lại và chốt bản này | Hoàng Quang Đạt |
| Đào data (viết script đếm, gợi ý nhãn) | Chưa dùng cho bằng chứng | Mới gợi ý nguồn review và cách đếm, chưa lấy review nào | Chưa có dòng nào để kiểm | Võ Thanh Huy |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Gợi ý câu hỏi nháp khi bàn phạm vi. Chưa gửi bộ câu hỏi nào | Chưa rà | Đỗ Anh Thư |
| Viết câu thử (benchmark) | Chưa dùng | Chưa viết câu thử của nhóm (file còn dòng mẫu của khung) | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | Vương Trường Giang |
| Sinh data `synthetic` (nếu có) | Claude Code | Tự đặt 18 đơn giả và chính sách hoàn trong `data/orders.json`, `data/policy.json` (viết tay trong script, không sinh ngẫu nhiên, không có seed). DH011–DH018 được thêm sau, đặt tên món theo các câu trong bộ benchmark của nhóm; giá tự đặt | Chưa ghi nhận người kiểm | Hoàng Quang Đạt |
| Chấm cột `pass` bằng LLM (nếu có) | Chưa dùng | Chưa chạy lượt đánh giá nào | | Vương Trường Giang |
| Slide, văn bản | Claude Code | Viết nháp `canvas.md` (bài toán, lát cắt, giả thuyết, mức tự động), chia phần việc trong `TEAMS.md`, điền mục khai báo này. Chưa làm slide | Nhóm chọn track D, lát cắt và cung cấp thông tin thành viên; câu chữ và phần chia việc cần cả nhóm rà lại | Cả nhóm |
| Chuẩn bị đề bài và repo | Claude Code | Đọc, tóm tắt bộ đề; hướng dẫn mốc CP1; chép starter-repo, điền tên nhóm / lớp / link, xoá mục 0 trong README, commit và push | Chưa ghi nhận người kiểm | Hoàng Quang Đạt |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
