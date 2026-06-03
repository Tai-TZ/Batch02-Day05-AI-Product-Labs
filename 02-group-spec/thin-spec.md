# Thin SPEC Cuối Day 05 — Vinpearl In-Stay Concierge (Q&A tiện ích + Gọi lễ tân)

Thin SPEC không phải PRD đầy đủ. Đây là bản cam kết đủ rõ để sáng Day 06 nhóm build ngay.

*Nộp kèm: `evidence-pack.md`, `synthesis-decide-toolkit.md`*

---

## 1. Track, product/app và user

**Track:** B · Travel & Hospitality  

**Product/app thật:** **MyVinpearl** (iOS / Android) — màn **Concierge in-stay** (prototype tách module, không refactor toàn app Day 06). Property demo: **Vinpearl Resort & Spa Phú Quốc** (`property_id = phu-quoc-vrp`).  

**User cụ thể:** Khách **đã check-in (in-stay)**, lần đầu hoặc không quen property, **tiếng Việt**, đi cùng gia đình (có trẻ em). Đang cần thông tin **trong ngày tại resort**: xe điện/shuttle, giờ ăn sáng, hồ bơi — không phải khách chỉ đặt vé hay chưa nhận phòng.  

**Nhóm có phải user thật không? Nếu không, khác ở đâu?**  
Một phần. Nhóm đã **self-use MyVinpearl** (booking/check-in journey); **chưa** in-stay thực tế tại Phú Quốc trong tuần lab. Khác biệt: prototype dùng **KB mock** theo FAQ public resort; escalation **Gọi lễ tân** dùng `tel:` mock (số thật / số trên thẻ phòng khi test tại chỗ). Bổ sung screenshot self-use + 1–2 review App Store trước M1.

---

## 2. Evidence summary


| Evidence                                                                         | Nguồn                                                                                                            | User/pain nói lên điều gì?                                | SPEC phải đổi gì?                                  |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------- |
| Sau check-in, app ưu tiên đặt dịch vụ/ưu đãi; khó thấy “hôm nay ở resort cần gì” | Self-use #1                                                                                                      | In-stay task **bị chôn**; cần entry **Concierge** riêng   | Thêm màn chat in-stay, không nhét vào booking flow |
| Không gom được giờ/điểm đón xe điện trong một câu trả lời                        | Self-use #2                                                                                                      | Pain **shuttle**; cần clarify hoặc escalate               | KB chunk `KB-shuttle-beach`; path low-confidence   |
| App mạnh check-in/booking; thiếu Q&A 1-turn tiện ích                             | [MyVinpearl — Google Play](https://play.google.com/store/apps/details?hl=vi&id=net.cloudhms.booking.vinpearl)    | Gap so với promise “trọn vẹn kỳ nghỉ”                     | Scope chỉ Q&A hẹp, không làm full PMS              |
| “Chờ xe điện lâu” giờ cao điểm; tổng đài đôi khi chậm ban đêm                    | [Review Vinpearl Nha Trang](https://vinpearlresortvietnam.com/review-dich-vu-khach-hang-tai-vinpearl-nha-trang/) | Cần FAQ tĩnh + **giảm gọi thừa**; escalate khi không chắc | Confidence threshold; không bịa realtime           |
| Spa slot tối — app không trả availability                                        | Self-use #4                                                                                                      | **Failure**: không bịa slot                               | D3 + Gọi lễ tân bắt buộc                           |
| VinWonders: map + vé + hotline, **không AI tư vấn**                              | [VinWonders App Store](https://apps.apple.com/us/app/vinwonders/id1590471592), observation nhóm                  | Gap ecosystem; **không** gộp VinWonders Day 06            | Giữ slice resort; VinWonders → backlog             |
| Marriott/Accor: handoff human, không hứa mọi realtime                            | Competitor analog                                                                                                | Pattern cite KB + **rescuer**                             | Nút **Gọi lễ tân** + copy context                  |


---

## 3. Pain statement

```text
Khách đã check-in tại Vinpearl Resort đang gặp khó ở bước “tìm nhanh thông tin tiện ích trong ngày” (xe điện, giờ ăn, pool),
vì MyVinpearl ưu tiên booking/check-in/ưu đãi và không có luồng hỏi–đáp in-stay một lần chạm,
dẫn tới phải lục nhiều mục, hỏi tại sảnh, hoặc gọi lễ tân/tổng đài — đặc biệt khi thông tin vận hành không rõ hoặc cần realtime (spa).
Bằng chứng chính là self-use #1–#4 (evidence pack) và review công khai về chờ xe điện / tổng đài (Vinpearl Nha Trang).
```

---

## 4. Build slice

```text
Cho khách đã check-in (in-stay) tại Vinpearl Resort & Spa Phú Quốc,
đang cần thông tin tiện ích trong ngày (xe điện/shuttle, giờ ăn sáng, hồ bơi),
prototype sẽ dùng AI để augment: retrieve KB cố định theo property → trả lời ngắn + nguồn + confidence,
tạo ra answer block + CTA (xem sơ đồ / copy),
và xử lý low-confidence / spa realtime / red flag / user báo sai
bằng không bịa thông tin + nút Gọi lễ tân (kèm tóm tắt câu hỏi tùy chọn).
```

**Out of scope Day 06:** đặt spa/phòng, lịch trình đa ngày, VinWonders in-park, tích hợp API MyVinpearl thật.

---

## 5. Auto/Aug decision

Chọn một:

- **Augmentation:** AI retrieve + draft trả lời; user đọc, bấm Đúng/Không đúng, hoặc chủ động Gọi lễ tân.
- **Conditional automation:** AI **chỉ** tự trả lời khi retrieve được chunk KB và confidence ≥ ngưỡng; ngược lại → clarify 1 câu hoặc **Gọi lễ tân** (không đoán).
- **Automation:** AI tự quyết và tự hành động.

*Ghi chú: Chọn **Augmentation làm chính**, kèm **conditional escalation** — không phải automation end-to-end.*

**Lý do chọn:** Sai giờ shuttle hoặc bịa slot spa có hậu quả thực (đến trễ, mất tin app). Khách đã **tin lễ tân** (review); AI chỉ thay phần FAQ tĩt, human giữ exception và rủi ro.  

**Human role:**  

- **Decider** — khách quyết “Đúng / Không đúng”, có thể bỏ qua AI và gọi thẳng.  
- **Rescuer** — lễ tân qua điện thoại khi confidence thấp, failure, correction, red flag.

---

## 6. Four paths

*Map với kịch bản demo Day 06 (D1–D5). Chi tiết prompt: evidence pack / README nhóm.*


| Path                         | Prototype phải thể hiện gì?                                                                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Happy** (D1)               | Prompt: *“Xe điện đi bãi biển chạy mấy giờ? Đón ở đâu?”* → Trả lời ngắn + cite `KB-shuttle-beach` + confidence cao + CTA [Xem sơ đồ sảnh].                                     |
| **Low-confidence** (D2)      | Prompt: *“Hôm nay còn xe điện không?”* (thiếu tuyến) → Clarify 1 câu: bãi biển / nhà hàng chính / lobby — **hoặc** confidence thấp → **[Gọi lễ tân]** (không nhắc VinWonders). |
| **Failure** (D3)             | Prompt: *“Spa còn chỗ 8h tối nay không?”* → Thông báo KB không có slot realtime; **không bịa** + **[Gọi lễ tân]**.                                                             |
| **Correction** (D4)          | Sau D1, user bấm **Không đúng** → Ghi nhận + hiện handoff + **[Gọi lễ tân]** + optional copy context cho người nhận máy.                                                       |
| **Escalate / red flag** (D5) | Prompt: *“Con tôi sốt 38.5°C”* → Message cố định (không tư vấn y khoa) + **[Gọi lễ tân ngay]** — rule-based, không qua LLM tự do.                                              |


**Escalation UI — Gọi lễ tân:**  

- Nút `tel:` mock Day 06: extension property hoặc hotline resort (nhóm xác nhận số FAQ).  
- Optional: copy clipboard `Câu hỏi | Property: Phú Quốc | Confidence: thấp`.  
- User luôn thấy rõ đang chuyển sang **người**, không chat ẩn danh.

---

## 7. Failure mode nguy hiểm nhất

```text
Nếu user hỏi giờ vận hành tiện ích (xe điện, pool, ăn sáng) hoặc câu cần dữ liệu realtime (spa slot),
AI có thể trả lời sai giờ/địa điểm hoặc hallucination khi không retrieve được chunk phù hợp,
hậu quả là khách đến trễ, bỏ lỡ dịch vụ, hoặc mất niềm tin vào app/in-stay digital.
Prototype sẽ xử lý bằng:
- chỉ trả lời khi có chunk KB + confidence ≥ ngưỡng (vd 0.75);
- luôn hiện source snippet;
- dưới ngưỡng → clarify 1 lần hoặc Gọi lễ tân;
- spa/realtime → failure message cố định + Gọi lễ tân;
- nút “Không đúng” → correction path;
- red flag sức khỏe → không Q&A, Gọi lễ tân ngay.
Owner kiểm thử path này là [Thành viên 3 — Test + D3 + D5].
```

**Ngưỡng confidence (mock Day 06):** `≥ 0.75` → answer; `0.50–0.74` → clarify; `< 0.50` hoặc no retrieval → Gọi lễ tân.

---

## 8. Owner plan cho sáng Day 06

**Nhóm 3 thành viên** — mỗi người một vai chính; hỗ trợ chéo khi kẹt (đặc biệt prototype + test sáng Day 06).


| Thành viên          | Việc phụ trách (chính)                                                                                     | Bằng chứng cần có trong repo                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Nguyễn Trọng Nguyên | **Research / evidence** — KB mock, screenshot self-use, bổ sung review App Store nếu thiếu                 | `data/kb-phu-quoc.json` (10–15 chunk); `assets/self-use-*.png`; cập nhật `evidence-pack.md`     |
| Ngô Thị Ánh         | **SPEC + repo** — giữ thin SPEC / toolkit đồng bộ; README hướng dẫn chạy demo; script trình bày 3 phút     | `02-group-spec/*.md`; `README.md` (cách chạy + link 3 file spec); `demo/demo-script.md` (kịch bản D1–D5) |
| Nguyễn Thành Tài    | **Prototype + test** — build UI chat in-stay, retrieve mock, nút **Gọi lễ tân**; chạy & ghi kết quả 5 path | `prototype/` (hoặc HTML); `test/results.md` (pass/fail D1–D5); demo ~3 phút (link trong README)          |


**Phân công nhanh sáng Day 06:**  

1. TV1 chốt KB → TV3 tích hợp retrieve.
2. TV2 viết `demo-script.md` song song TV3 code happy path (D1).
3. TV3 thêm D2–D5 + TV1/TV2 review.

**Definition of done Day 06:** Demo được 5 path; không bịa spa slot; red flag luôn escalate; repo có evidence + SPEC + prototype + kết quả test.

---

## 9. Backlog (tham chiếu — không build Day 06)

- Lịch trình đa ngày / AI itinerary  
- Đặt spa–phòng qua chat  
- API MyVinpearl / PMS realtime  
- VinWonders in-park Q&A (escalation **tổng đài**)  
- Đa ngôn ngữ; Zalo thay call

---

*Day 05 Thin SPEC — Batch 02 · Track B · MyVinpearl In-Stay Concierge*