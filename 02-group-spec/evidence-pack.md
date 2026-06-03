# Evidence Pack — Vinpearl In-Stay Concierge (Q&A tiện ích + gọi lễ tân)

Nộp kèm thin SPEC cuối Day 05.

## 1. Nhóm và track

**Tên nhóm:** · **Số thành viên:** 3  
**Track:** B · Travel & Hospitality  
**Product/app đã chọn:** MyVinpearl (iOS/Android) — hành trình **in-stay** tại Vinpearl Resort (ví dụ property demo: **Vinpearl Resort & Spa Phú Quốc**)  
**Build slice đã chốt:** Q&A tiện ích in-stay (shuttle/xe điện, F&B, pool) — AI retrieve KB + cite nguồn + confidence; escalation **gọi lễ tân** khi low-confidence / red flag / user báo sai  

## 2. Self-use evidence

Nhóm tự dùng MyVinpearl / trải nghiệm in-stay (hoặc mô phỏng sau check-in) và ghi điểm gãy.  
*Screenshot: nhóm chụp/bổ sung trước demo Day 06 — ghi đường dẫn file trong repo.*


| Observation                                                                                                                                                                                        | Screenshot/link                                                                                               | Path liên quan   | Điều học được                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Sau check-in, mở app thấy ưu tiên **đặt thêm dịch vụ / Pearl Club / ưu đãi**, khó tìm ngay block “**hôm nay ở resort cần gì**” (shuttle, giờ ăn sáng, pool). Phải lục nhiều mục hoặc hỏi tại sảnh. | `[assets/self-use-01-home-instay.png]`                                                                        | Failure          | Pain = **task in-stay bị chôn** dưới journey booking; không phải thiếu tiện ích mà thiếu **entry point theo ngữ cảnh đang ở**. |
| Tìm thông tin **xe điện / di chuyển nội khu**: có nhắc trên web resort (sảnh, VinBus) nhưng trong app **không có một câu trả lời gom** (giờ, điểm đón, có cần thẻ phòng không).                    | `[assets/self-use-02-shuttle-search.png]`                                                                     | Low-confidence   | User hỏi “hôm nay còn xe không?” — app không trả lời trực tiếp → cần **clarify property + khung giờ** hoặc escalate.           |
| Mục **Quản lý lịch trình** trên store mô tả sắp xếp dịch vụ, nhưng self-use không thấy luồng “**hỏi nhanh 1 tiện ích**” (FAQ 1-turn). Cảm giác phải tự ghép thông tin.                             | [MyVinpearl — Google Play](https://play.google.com/store/apps/details?hl=vi&id=net.cloudhms.booking.vinpearl) | Happy (một phần) | App mạnh **booking + check-in online**; slice in-stay Q&A là **khoảng trống** so với promise “trọn vẹn kỳ nghỉ”.               |
| Thử câu hỏi kiểu “**Spa còn slot tối nay không?**” — không có kênh trong app trả **realtime availability**; kết quả thực tế = gọi spa/lễ tân.                                                      | `[assets/self-use-03-spa-no-slot.png]`                                                                        | Failure          | **Không được để AI bịa slot**; failure path bắt buộc: nói giới hạn KB + **Gọi lễ tân**.                                        |
| Khi thông tin mơ hồ, quyết định thực tế: **gọi số lễ tân / nhờ nhân viên sảnh** (đúng pattern escalation đã chọn).                                                                                 | `[assets/self-use-04-call-frontdesk.png]`                                                                     | Correction       | Human rescuer đã có sẵn tại resort; prototype chỉ cần **một nút Gọi lễ tân** + tóm tắt câu hỏi cho người nhận máy.             |


## 3. User / review / social evidence


| Quote / review / observation                                                                                                        | Nguồn                                                                                                                            | User là ai?                 | Pain/failure mode                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------- |
| “Vào giờ cao điểm **phải đợi xe điện lâu hơn**…” — cần biết trước lịch/alternative, không chỉ “có xe”.                              | [Review tổng hợp — Vinpearl Nha Trang](https://vinpearlresortvietnam.com/review-dich-vu-khach-hang-tai-vinpearl-nha-trang/)      | Gia đình in-stay            | Failure / low-confidence — thông tin vận hành **theo thời gian thực** khó có trong FAQ tĩnh. |
| “**Một số trường hợp phải chờ lâu khi gọi tổng đài**, đặc biệt ban đêm.”                                                            | Cùng nguồn trên                                                                                                                  | Khách in-stay ban đêm       | Escalation qua call vẫn cần; AI phải **giảm cuộc gọi thừa** (chỉ escalate khi cần).          |
| “Nhân viên… **cung cấp thông tin về các dịch vụ**… gọi xe điện…” — kênh con người hoạt động tốt nhưng **không scale** lúc cao điểm. | Cùng nguồn trên                                                                                                                  | Mọi segment in-stay         | Opportunity: AI trả lời **FAQ cố định**; human cho exception.                                |
| “**Lễ tân nhanh nhẹn**, hỗ trợ check-in…” — điểm cộng dịch vụ người; khách **tin** lễ tân khi app không rõ.                         | [Dịch vụ khách hàng — Vinpearl Phú Quốc](https://vinpearlresortvietnam.com/dich-vu-khach-hang-tai-vinpearl-resort-spa-phu-quoc/) | Khách lần đầu               | Escalation **Gọi lễ tân** khớp hành vi hiện có; prototype không thay thế toàn bộ lễ tân.     |
| App MyVinpearl: mô tả **check-in online, đặt dịch vụ, quản lý lịch trình** — ít nhấn mạnh **Q&A tiện ích tức thời in-stay**.        | [App Store — MyVinpearl](https://apps.apple.com/us/app/myvinpearl/id1484921109?l=vi)                                             | User đã book, đang ở resort | Mismatch promise vs in-stay task → justify build slice hẹp.                                  |


*Nếu nhóm bổ sung thêm review App Store/Play (1–2 sao, keyword “thông tin”, “app”), paste quote vào hàng trống dưới đây trước M1.*

## 4. Competitor / analog evidence


| App / mô hình tham khảo                                  | Họ xử lý task này thế nào?                                                                                                                                                                   | Pattern học được                                                                                                                                         | Có áp dụng trong 1 ngày không?                                                           |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Marriott Bonvoy — chat / request                         | Chat có template yêu cầu; phức tạp chuyển **nhân viên**; không cam kết realtime mọi dịch vụ.                                                                                                 | **Handoff human** + không bịa availability                                                                                                               | Có — nút Gọi lễ tân + tóm tắt context                                                    |
| Accor ALL — messaging                                    | FAQ + messaging property; một số câu trả lời chận từ knowledge base.                                                                                                                         | Cite / template theo property                                                                                                                            | Có — KB mock theo 1 resort                                                               |
| Klook / travel app in-trip                               | Thông tin điểm đến; booking tách khỏi “đang ở đó hỏi giờ mở cửa”.                                                                                                                            | Tách **in-trip micro-Q&A** khỏi booking                                                                                                                  | Có — 1 màn Concierge in-stay                                                             |
| **VinWonders app** (cùng hệ sinh thái Vingroup, Track B) | Đặt vé, bản đồ số, lịch show, My Plan, hàng chờ ảo — **không có** chatbot / AI tư vấn khách in-park. Hỗ trợ qua [contact / tổng đài](https://vinwonders.com/vi/contact/) (vd 1900 23 23 89). | **Khoảng trống:** khách vẫn tự tra map + gọi người khi cần tư vấn; prototype resort có thể là **mảng đầu** của pattern “Q&A + escalate” cho cả ecosystem | Không build VinWonders Day 06 — ghi **backlog**; slice Day 06 giữ **MyVinpearl in-stay** |


**Observation nhóm (VinWonders):** Self-use / quan sát app VinWonders — không thấy luồng hỏi đáp AI (giờ show, đường đi, tiện ích trong ngày); chỉ công cụ tự phục vụ + hotline. Củng cố cơ hội product: **AI concierge chưa có** ở kênh công viên, trong khi resort (MyVinpearl) cũng thiếu Q&A in-stay — pain tương tự, user khác (in-park vs in-stay).

## 5. Evidence -> Insight

```text
Evidence nổi bật nhất:
- Self-use: app mạnh booking/check-in; thông tin tiện ích in-stay (shuttle, giờ ăn, pool) khó lấy trong 1 luồng.
- Review/public: khách phụ thuộc lễ tân/xe điện khi thông tin vận hành không rõ hoặc cao điểm; tổng đài đôi khi chậm → cần giảm gọi thừa.
- Competitor: pattern handoff human + không hứa realtime ngoài KB.
- VinWonders (analog nội bộ): app công viên **chưa có AI tư vấn** — khách dựa map + lịch + gọi tổng đài; cùng pattern “thiếu micro-Q&A có escalation” với resort.

Insight:
Khách đã check-in tại Vinpearl không chỉ cần “danh sách tiện ích resort”.
Họ cần câu trả lời đúng ngữ cảnh (property + khung giờ) và lối thoát tin cậy khi không chắc,
vì evidence cho thấy app chưa phục vụ tốt micro-task in-stay, trong khi khách vẫn tin lễ tân nhưng muốn giải quyết nhanh trước khi gọi.

Opportunity:
AI augment — retrieve câu trả lời từ KB tiện ích cố định, hiện confidence + nguồn;
giúp khách quyết định trong <1 phút;
escalation “Gọi lễ tân” khi low-confidence, red flag, hoặc user báo sai — không tự đặt spa/đổi phòng.
```

## 6. Evidence đổi SPEC như thế nào?

- Đổi user chính.
- Đổi pain statement.
- Đổi build slice.
- Đổi Auto/Aug decision.
- Đổi 4 paths.
- Đổi failure mode.
- Đổi owner/test plan.

