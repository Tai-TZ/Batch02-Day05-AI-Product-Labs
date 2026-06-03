# Toolkit — Từ Evidence Đến Build Slice (Vinpearl In-Stay Q&A + Gọi lễ tân)

Dùng sau khi nhóm đã có evidence pack. Mục tiêu: chốt build slice đủ nhỏ cho Day 06.

---

## 1. Gom evidence thành cụm

Gom theo **workflow/pain**, không gom theo tên feature.

### Cụm đã gom từ evidence pack


| Cụm pain (workflow)                                                         | Evidence hỗ trợ                                   | Liên quan demo                                                        |
| --------------------------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------- |
| **Không tìm nhanh tiện ích in-stay trên app** (bị chôn dưới booking/ưu đãi) | Self-use #1, #3; App Store mô tả                  | Entry “Concierge in-stay”                                             |
| **Không biết giờ / điểm đón shuttle–xe điện**                               | Self-use #2; review Nha Trang (chờ xe)            | Demo D1 Happy, D2 Low-confidence                                      |
| **Hỏi availability realtime (spa, slot)** — app/KB không đủ                 | Self-use #4                                       | Demo D3 Failure                                                       |
| **Không tin câu trả lời AI / cần người**                                    | Self-use #5; review tin lễ tân                    | Demo D4 Correction; escalation Gọi lễ tân                             |
| **Tình huống nhạy cảm (sức khỏe)**                                          | Red flag policy                                   | Demo D5 Escalate                                                      |
| **VinWonders: không có AI tư vấn in-park** (map + vé + hotline)             | Observation app VinWonders; analog nội bộ Track B | **Không** gộp vào slice Day 06 — đưa backlog; củng cố “gap ecosystem” |


### Cụm loại (không chọn làm slice Day 06)

- “AI gợi ý lịch trình 3 ngày Phú Quốc” — quá rộng, thiếu evidence in-stay trực tiếp.
- “Chatbot đặt phòng/đổi hủy” — rủi ro cao, không demo 1 ngày.
- “Concierge đa ngôn ngữ toàn resort” — backlog.
- **“AI concierge VinWonders”** (hỏi show, lối đi, giờ chờ) — pain thật nhưng **app/product khác**, escalation = tổng đài thay vì lễ tân; làm sau khi xong slice resort.

---

## 2. Viết insight

```text
Khách đã check-in tại Vinpearl (gia đình / lần đầu property) không chỉ cần danh sách tiện ích hay màn hình đặt thêm dịch vụ.
Họ thật ra cần câu trả lời đúng ngữ cảnh (property + khung giờ) và một lối thoát tin cậy khi thông tin không đủ hoặc không realtime,
vì self-use cho thấy MyVinpearl ưu tiên booking/check-in; review/public nhấn mạnh phụ thuộc xe điện/lễ tân/tổng đài khi thông tin vận hành không rõ hoặc cao điểm;
đồng thời VinWonders (cùng Track B) cũng không có AI tư vấn — chứng minh gap “micro-Q&A + escalation” chưa được khai thác trong hệ sinh thái hospitality/entertainment của Vingroup.
```

---

## 3. Viết opportunity

```text
Cơ hội là dùng AI để augment hành động hẹp: retrieve + trả lời Q&A tiện ích từ KB cố định (shuttle, ăn sáng, pool),
kèm confidence và trích dẫn nguồn,
giúp khách quyết định trong dưới 1 phút mà không phải lục toàn app,
trong khi vẫn kiểm soát rủi ro bằng không bịa slot spa / không tư vấn y khoa — chuyển sang Gọi lễ tân khi low-confidence, failure, correction, hoặc red flag.
```

---

## 4. Chọn build slice

### Build slice (đã chốt)

```text
Cho khách đã check-in (in-stay) tại Vinpearl Resort (demo: Phú Quốc),
đang cần thông tin tiện ích trong ngày (xe điện/shuttle, giờ ăn sáng, hồ bơi),
prototype dùng AI để retrieve KB + trả lời ngắn + hiển thị nguồn và confidence,
tạo ra answer block + CTA (map / copy),
và xử lý low-confidence / sai KB / spa realtime / red flag bằng nút Gọi lễ tân (không bịa, không thay lễ tân cho mọi câu).
```

### 5 câu hỏi — đánh giá slice


| Câu hỏi               | Đạt?   | Trả lời cho slice này                                                                                      |
| --------------------- | ------ | ---------------------------------------------------------------------------------------------------------- |
| User cụ thể chưa?     | **Có** | Khách **in-stay**, đã check-in, tại **một** property (Phú Quốc cho demo).                                  |
| Task đủ hẹp chưa?     | **Có** | 5 prompt demo (D1–D5) trong 3–5 phút; không booking, không lịch trình đa ngày.                             |
| AI decision rõ chưa?  | **Có** | Một việc: **retrieve KB → draft answer → gán confidence → route** (trả lời / clarify / Gọi lễ tân).        |
| Failure path rõ chưa? | **Có** | D3 spa slot; D2 thiếu ngữ cảnh; D5 red flag; D4 correction.                                                |
| Có evidence không?    | **Có** | Self-use 5 dòng + review/public 5 dòng + competitor 3 dòng (evidence pack). Bổ sung screenshot trước demo. |


---

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?


| Tình huống                            | Áp dụng? | Quyết định nhóm                                                                |
| ------------------------------------- | -------- | ------------------------------------------------------------------------------ |
| Evidence yếu, user mơ hồ              | Không    | Giữ slice; bổ sung 1–2 review App Store + screenshot self-use trước M1.        |
| Ý tưởng quá rộng (“AI concierge”)     | **Có**   | **Giảm scope** → chỉ Q&A tiện ích in-stay + Gọi lễ tân.                        |
| AI không cần thiết                    | Không    | Cần AI cho retrieve + paraphrase + confidence; rule-only cho red flag message. |
| Rủi ro cao (sai giờ shuttle, bịa spa) | **Có**   | **Augmentation + conditional escalation**; human = lễ tân qua điện thoại.      |
| Không demo được trong 1 ngày          | Một phần | **Giữ** chat UI + KB JSON mock + 5 demo paths; backlog tích hợp API thật.      |


**Quyết định cuối:** **Giữ** hướng slice; **không** đổi sang Sun World hay pre-arrival trong Day 06.

---

## 6. Câu chốt cuối

```text
Dựa trên self-use MyVinpearl (tiện ích in-stay khó tìm), review Vinpearl (chờ xe điện/tổng đài), và analog Marriott/Accor (handoff human),
nhóm sẽ build prototype Concierge Q&A tiện ích in-stay có cite KB + confidence,
cho khách đã check-in tại Vinpearl Resort & Spa Phú Quốc,
để giải quyết pain tìm nhanh giờ/địa điểm tiện ích mà không sai thông tin,
bằng cách AI augment retrieve-and-answer,
và sẽ test failure path hỏi slot spa 8h tối → không bịa + Gọi lễ tân, và red flag sốt trẻ em → Gọi lễ tân ngay.
```

---

## 7. Backlog (không build Day 06)

- Gợi ý lịch trình đa ngày / AI itinerary planner  
- Đặt spa/phòng/đổi booking qua chat  
- Tích hợp API MyVinpearl / PMS realtime  
- Đa property trong một session (chọn resort trước khi chat — có thể chỉ chọn 1 lần mock)  
- Đa ngôn ngữ đầy đủ (chỉ tiếng Việt cho demo)  
- Chat Zalo thay vì Gọi lễ tân (escalation đã chốt: **call**)  
- **VinWonders in-park Q&A AI** (giờ show, đường đi, hàng chờ) — escalation **gọi tổng đài** 1900…; product/app riêng, học pattern từ slice resort

