# AI SPEC — Khiếu nại đơn đồ ăn giao thiếu món · Nhóm AoAshi · Phòng D304 · Zone 1

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [ ] A · [ ] B · [ ] C · [x] D · [ ] E — bài toán: người đặt đồ ăn qua app nhận đơn bị thiếu món, muốn khiếu nại để lấy lại tiền món đó nhưng không rõ bước tiếp theo, phải chờ lâu hoặc bỏ cuộc.
Data BTC cấp đã dùng (nếu có — không commit nguyên file): Không dùng.

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại trên app giao đồ ăn (ShopeeFood, GrabFood…), tổng hợp từ `evidence/interviews/P1.md`–`P3.md`:
  1. Mở túi đồ ăn, phát hiện thiếu món (P1: thiếu topping, hộp canh · P2: thiếu khoai tây chiên trong combo · P3: đơn nhóm 5–6 món, quán hay đóng thiếu).
  2. Chụp ảnh túi và hoá đơn dán trên túi, nếu còn. P2 đã vứt bill nên không có bằng chứng để nộp.
  3. Tìm mục Trợ giúp / form khiếu nại trên app, hoặc gọi tài xế / quán (P2). P3 không biết bấm vào đâu: "giao diện khiếu nại giấu kỹ quá, tìm mãi mới ra".
  4. Tự gõ lại mã đơn và tên món thiếu, nhắn CSKH. P1 qua bot trước rồi mới gặp nhân viên. P3 phải lật lại lịch sử đơn để dò món thiếu rồi gõ tay từng chữ, gửi qua mục Trợ giúp và nhắn thêm CSKH.
  5. Chờ phản hồi rồi nhận kết quả: P1 chờ ~20 phút, được voucher thấp hơn giá món · P3 hơn 30 phút (tính cả chờ duyệt) mới được hoàn đúng giá trị món thiếu về ví · P2 loay hoay ~10 phút rồi bỏ cuộc, mất ~25.000đ.
- Ảnh chụp từ tài khoản của nhóm (đã che thông tin):  ![Mục trợ giúp trên app](assets/p1-tro-giup.png) hình ảnh của p1
- Công cụ / AI đang được dùng: gemini dùng tạo google doc, deekseek dùng cho llm

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): người đặt đồ ăn qua app, vừa nhận đơn và thấy thiếu món.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): đòi lại tiền món bị thiếu ngay sau khi nhận đơn đồ ăn giao qua app.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: nhắn qua mục Trợ giúp / CSKH của app, hoặc gọi tài xế / quán. Hỏng ở chỗ: khó tìm form khiếu nại (P3), phải chờ nhân viên lâu và không biết bước tiếp theo (P1), app đòi ảnh hoá đơn đã vứt (P2), phải tự nhớ và gõ lại tên món, mã đơn (P1, P3), được hoàn thấp hơn giá món (P1). Chưa bỏ vì vẫn muốn lấy lại tiền món đã trả; khi món rẻ thì nhiều người bỏ luôn (P2).
- Pain (KHÔNG chữ AI): người đặt đồ ăn qua app mở đơn ra thấy thiếu món, muốn khiếu nại nhưng khó tìm chỗ khiếu nại, phải tự gõ lại thông tin và chờ 10 đến hơn 30 phút không rõ bước tiếp theo, nên hoặc bỏ cuộc mất tiền món đó, hoặc chỉ nhận voucher thấp hơn giá món.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`):
  - Phỏng vấn: 3/3 người bị thiếu món trong 1 tháng qua (P1 2 lần, P2 1 lần, P3 2 lần). Lần gần nhất mất ~10 phút (bỏ cuộc) đến hơn 30 phút. 2/3 người không lấy lại đủ tiền (P1 voucher thấp hơn giá món, P2 bỏ cuộc); P3 được hoàn đủ nhưng mất hơn 30 phút.
  - Khảo sát (`evidence/survey/results.csv`, n = 21): 9/21 người bị thiếu món ≥1 lần trong 1 tháng qua, tổng 14 lần. Lần gần nhất xử lý: 9/16 người mất ≥15 phút (6 người 15–30 phút, 3 người trên 30 phút) · 7/15 người khiếu nại chỉ được giải quyết một phần.
  - Kết luận: giả thuyết "khách khó khiếu nại và phải chờ lâu" được ủng hộ ở cả phỏng vấn và khảo sát. Số review giao đồ ăn của Huy (`evidence/data-mining.md`) bổ sung sau.
  - Giới hạn: 2/21 người chưa từng đặt đồ ăn vẫn nằm trong mẫu số 21.

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| Khiếu nại đơn giao **thiếu món** | 9/21 người khảo sát · 3/3 người phỏng vấn (trong 1 tháng qua) | 14 lần / 9 người (TB 1,56) | ~17 phút *(tự ước tính, giữa các khoảng câu 6)* + tiền món thiếu không lấy lại được (P2 ~25.000đ) | ≈ 238 phút ≈ 4 giờ trong 21 người | Kịp — bản chạy thử đã có, đơn và món kiểm được bằng dữ liệu đơn | ✅ |
| Khiếu nại **sai món** | chưa đo | chưa đo | chưa đo | chưa đo | Khó — phải đối chiếu ảnh món nhận được, §4 đã ghi không đọc ảnh | ❌ |
| Khiếu nại **giao trễ** | chưa đo | chưa đo | chưa đo | chưa đo | Khó — cần dữ liệu thời gian giao thật của app, nhóm không có | ❌ |

- **Impact / tháng** của hướng chọn = 9 người × 1,56 lần × ~17 phút ≈ 238 phút (≈ 4 giờ) / tháng trong mẫu 21 người — nguồn từng thừa số: 9 người và 14 lần từ câu 4 khảo sát · 17 phút là trung bình giữa các khoảng của câu 6 (dưới 5 → 2,5 · 5–15 → 10 · 15–30 → 22,5 · trên 30 → 30) trên 16 người có xử lý *(tự ước tính)*. Chưa tính tiền món bị mất. Quy mô người dùng thật để ở §8.
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá): **sai món** — phải xác minh món nhận được qua ảnh, ngoài phạm vi lát cắt (§4 "không đọc ảnh"). **Giao trễ** — cần dữ liệu thời gian giao thật mà nhóm không có, và lỗi nằm ở vận hành giao hàng hơn là ở bước khiếu nại. Cả hai chưa có số đo; khi gặp trong tin khách thì bản chạy thử chuyển nhân viên. *(nháp — nhóm chốt ở họp 08:00)*
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8) — số lần **bị thiếu món** / tháng (câu 4) theo tần suất đặt (câu 2), khảo sát n = 21:

  | Kiểu người dùng (câu 2) | n | Số lần thiếu món / tháng (TB) |
  |---|---|---|
  | Hầu như ngày nào cũng đặt | 3 | 2,0 (0 · 1 · 5) |
  | Vài lần mỗi tuần | 7 | 0,86 |
  | Vài lần mỗi tháng | 3 | 0 |
  | Hiếm khi đặt (vài tháng 1 lần) | 6 | 0,33 |
  | Chưa bao giờ đặt | 2 | 0 — không phải người dùng, bỏ khỏi persona |

  n nhỏ, mỗi nhóm chỉ 3–7 người. Phỏng vấn khớp chiều này: P1 (ngày nào cũng đặt) 2 lần / tháng · P2 (3–4 đơn / tuần) 1 lần · P3 (vài lần / tuần, đặt đơn nhóm) 2 lần.

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả): Một khách nhận đơn thiếu món gửi khiếu nại, AI quyết định đề xuất hoàn tiền món thiếu, hỏi thêm hay chuyển cho nhân viên, để khách biết bước tiếp theo.
- Không làm (≥3 điều): không xử lý sai món, giao trễ, chất lượng món, ngộ độc (chỉ chuyển nhân viên) · không đọc ảnh · không lưu lịch sử hội thoại · không hoàn tiền thật, không nối app thật.
- **Sơ đồ** (sơ đồ hoạt động UML; các luật liền nhau cùng kết quả được gộp vào một nút quyết định):

![Sơ đồ hoạt động](assets/so_do_kien_truc.svg)

- **Hình dạng:** [x] workflow cố định · [ ] một agent · [ ] nhiều agent — Mọi tin đi cùng một đường: đọc đơn, AI quyết định, code kiểm. AI không cần tự chọn công cụ, nên agent chỉ thêm lượt gọi model và khó đo hơn.
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | get_order | mã đơn | đơn giả lập, hoặc không có | Không (chỉ đọc) |
  | get_policy | không | hạn mức hoàn giả lập | Không (chỉ đọc) |
  | draft_refund | mã đơn, món, số tiền | bản nháp chờ nhân viên duyệt | Không |
  | escalate_to_staff | mã lý do, mã đơn khách nêu, món khách nêu, tin của khách | phiếu nháp, giữ nguyên văn tin (tối đa 1000 ký tự) | Không |

- **Mức tự động:** [x] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — Hoàn sai thì quán mất tiền, từ chối sai thì khách chịu thiệt. Bản chạy thử chỉ tạo bản nháp.
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì): đề xuất hoàn tiền sai bị chặn bằng code trong `codebase/rules.py`. Code chỉ hạ quyết định của AI, không nâng. Số tiền do code tính từ đơn. Chặn món không có trong đơn, vượt số lượng đã đặt, vượt hạn mức 100.000đ, đơn đã hoàn hoặc chưa giao. Nhiều mã đơn thì hỏi lại. AI trả sai định dạng thì chuyển nhân viên. Câu gửi khách lấy từ mẫu; chữ duy nhất chèn thêm là tên món có sẵn trong tin của khách, và cụm có từ "đã, hoàn, tiền, bồi, duyệt, gửi" bị bỏ.
- **Chỗ người duyệt** (việc AI không được tự làm): AI không được tự hoàn tiền hay tự gửi phiếu. Mọi đề xuất hoàn tiền phải chờ nhân viên duyệt.
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | Chưa rõ đơn hoặc món thì `hoi_them`; ngoài phạm vi hoặc không khớp đơn thì `chuyen_nhan_vien` |
  | G1 — nói rõ làm được gì | Câu đề xuất ghi tiền chưa được hoàn, đang chờ nhân viên duyệt |
  | G11 — giải thích vì sao | Câu đề xuất nêu món, số lượng và số tiền làm căn cứ |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật: model đang ở chế độ giả (đã viết phần nối DeepSeek, chưa gọi thật) · đơn hàng và hạn mức 100.000đ là giả lập · bản nháp và phiếu không được lưu thành hàng đợi, không gửi cho ai · bước nhân viên duyệt chưa được xây · không hoàn tiền.

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — 30 câu (thuong 9 · kho 17 · tu_choi 4) · metric: `eval/metric_spec.yaml` (4 metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ 80% câu qua theo pass_criterion, 100% câu tu_choi qua, và cả 4 metric trong eval/metric_spec.yaml đạt ngưỡng: ghi_dung_thong_tin ≥ 90%, hoi_thong_tin_thieu ≥ 90%, khong_tu_thuc_hien = 100%, dung_quyet_dinh_va_so_tien = 100%."
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): __
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
