# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/agent.py`, `tools.py`, `rules.py`, phần gọi model trong `ai.py` (theo `docs/connect-model.md`; DeepSeek theo tài liệu chính thức) và test trong `tests/`. Sau khi đối chiếu với benchmark: thêm trường `mon_khach_neu` và bộ lọc tên món, câu trả lời nhắc lại món khách nêu, phiếu chuyển nhân viên giữ tin của khách. Trước CP2 chạy chế độ giả; từ tối 27/11 gọi thật `deepseek-flash` (`eval/run-1.csv`) | Đạt duyệt thiết kế; code chưa ghi nhận người kiểm | Hoàng Quang Đạt |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn thiết kế workflow, luật chặn rủi ro và `SYSTEM`. Đã chạy với model thật ở `run-1`. Sau `run-1`: sửa hai dòng luật trong `SYSTEM` cho nhóm lỗi chuyển nhân viên quá tay | Đạt duyệt thiết kế; chưa ghi nhận người kiểm nội dung `SYSTEM` | Hoàng Quang Đạt |
| Sơ đồ kiến trúc (`assets/so_do_kien_truc.svg`) | Claude Code | Vẽ sơ đồ hoạt động theo `codebase/agent.py`, `rules.py` bằng script tạm; so điều kiện gộp trên sơ đồ với `rules.decide` ở 154 tổ hợp đầu vào (chỉ so quyết định cuối, không so `LY_DO`) | Đạt xem hình, yêu cầu vẽ lại và chốt bản này | Hoàng Quang Đạt |
| `spec.md` §4 (thiết kế) | Claude Code | Soạn nội dung §4 theo code trong `codebase/` và thiết kế đã duyệt | Chưa ghi nhận người kiểm | Hoàng Quang Đạt |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code (gợi ý ban đầu) | Gợi ý nguồn review và cách đếm. Review trong `evidence/data-mining.md` do Huy tự tìm trên Shopee. Việc có dùng AI để tóm tắt hay viết file này: chưa xác nhận | Chưa ghi nhận người kiểm lại số đếm | Võ Thanh Huy |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Gợi ý câu hỏi nháp khi bàn phạm vi. Bộ câu hỏi đã gửi nằm ở `evidence/survey/questions.md`; bản đó có dùng gợi ý của AI hay không: chưa xác nhận | Chưa ghi nhận người rà | Đỗ Anh Thư |
| Viết câu thử (benchmark) | Codex, Claude Code | Codex soạn và Việt hóa câu thử theo dữ liệu giả lập; Claude Code đề xuất B26–B30 từ dữ liệu đơn và chính sách giả lập | Phụ trách rà input, expected, pass_criterion và nguồn trước khi chốt | Vương Trường Giang |
| Sinh data `synthetic` (nếu có) | Claude Code | Tự đặt 18 đơn giả và chính sách hoàn trong `data/orders.json`, `data/policy.json` (viết tay trong script, không sinh ngẫu nhiên, không có seed). DH011–DH018 được thêm sau, đặt tên món theo các câu trong bộ benchmark của nhóm; giá tự đặt | Chưa ghi nhận người kiểm | Hoàng Quang Đạt |
| Data card (`data/DATA_CARD.md`) | Codex | Theo `DATA_CARD.md`: kiểm tự động 18 đơn, 34 dòng món và 1 cấu hình chính sách. Việc Codex có soạn nội dung file hay không: chưa xác nhận | Chưa ghi nhận người kiểm tay | Võ Thanh Huy |
| Video demo CP3 | Claude Code | Cắt đoạn đầu, phóng to vùng terminal và dòng kết quả, thêm tiêu đề và chú thích từ bản quay màn hình của Đạt; không tua nhanh, không dựng kết quả giả. Bản dựng không có tiếng | Chưa ghi nhận người xem lại toàn bộ | Hoàng Quang Đạt |
| Nối model thật và thử tay | Antigravity | Theo README: hỗ trợ kiểm tra nối `deepseek-flash`, chạy thử câu mẫu, cập nhật `spec.md` §4–§6 và `README.md` | Đạt chạy kiểm tra và chốt giữ luật trước `run-1` | Hoàng Quang Đạt |
| Tạo Google Doc | Gemini | Bản `spec.md` §0 trước đó ghi dùng Gemini để tạo Google Doc; nội dung cụ thể: chưa xác nhận | Chưa ghi nhận | Chưa xác nhận |
| Chấm cột `pass` bằng LLM (nếu có) | Antigravity (Gemini) | Đọc `eval/run-1.csv` và `traces/run-1.jsonl` để đối chiếu `pass_criterion` và tính 4 metric trong `eval/metric_spec.yaml` | Giang tự kiểm tra lại các ca biên (`B08`, `B13`) và chốt điểm `pass` cuối cùng | Vương Trường Giang |
| Slide, văn bản | Claude Code | Viết nháp `canvas.md` (bài toán, lát cắt, giả thuyết, mức tự động), chia phần việc trong `TEAMS.md`, điền mục khai báo này; soạn phần cập nhật CP2 trong `canvas.md` (dòng 4 và "Đã đổi gì so với CP1"). Chưa làm slide | Nhóm chọn track D, lát cắt và cung cấp thông tin thành viên; câu chữ và phần chia việc cần cả nhóm rà lại | Cả nhóm |
| Chuẩn bị đề bài và repo | Claude Code | Đọc, tóm tắt bộ đề; hướng dẫn mốc CP1; chép starter-repo, điền tên nhóm / lớp / link, xoá mục 0 trong README, commit và push | Chưa ghi nhận người kiểm | Hoàng Quang Đạt |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
