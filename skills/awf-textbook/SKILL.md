---
name: awf-textbook
description: >-
  Quy trình chuẩn hóa viết textbook/ebook theo phương pháp Backward Design,
  tích hợp tiêu chuẩn chống văn phong AI, tối ưu cho giảng viên & content creator.
  Keywords: textbook, ebook, sách, viết, write, book, chapter, bài học, lesson.
version: 2.0.0
---

# AWF Textbook Writer v2.0

Skill chuẩn hóa quy trình viết textbook/ebook chuyên nghiệp.

Nền tảng phương pháp:
- **Backward Design** (Wiggins & McTighe / MIT / OSU) — thiết kế từ mục tiêu → đánh giá → nội dung.
- **Harvard Writing Elements** (Gordon Harvey) — thesis, motive, evidence, analysis cho từng chương.
- **Stanford Clarity** (Williams) — câu rõ ràng, chủ ngữ hành động, tránh nominalization.
- **Anti-AI Writing Standards** (Wikipedia) — loại bỏ văn phong đặc trưng AI.

Tham khảo chi tiết: `textbook_writing_guide.md` trong thư mục gốc dự án.

## Khi nào Skill này được kích hoạt?

- User gọi `/textbook`
- User yêu cầu viết sách, ebook, tài liệu giảng dạy
- User đề cập keywords: textbook, ebook, sách, viết bài, chapter, lesson

## Quy trình tổng quan

```
📋 PLAN → 🏗️ SCAFFOLD → ✍️ WRITE → 🔍 REVIEW → 📦 EXPORT
```

---

## Phase 1: PLAN — Thiết kế nội dung (Backward Design)

AI PHẢI tuân theo quy trình Backward Design, KHÔNG bắt đầu bằng việc chọn nội dung.

### Bước 1.1 — Thu thập thông tin đầu vào

AI PHẢI hỏi user nếu chưa có đủ thông tin:

| Thông tin | Mô tả | Bắt buộc |
|-----------|--------|----------|
| `topic` | Chủ đề sách | ✅ |
| `audience` | Đối tượng đọc giả (SV năm mấy, trình độ gì) | ✅ |
| `outline` | Dàn bài / kế hoạch có sẵn (file .md hoặc mô tả) | ✅ |
| `language` | Ngôn ngữ viết (vi/en) | ✅ |
| `code_language` | Ngôn ngữ lập trình nếu có (Python, JS...) | ❌ |
| `style` | Giọng văn (academic, friendly, tutorial) | ❌ mặc định: friendly-academic |
| `output_dir` | Thư mục lưu output | ❌ mặc định: `./ebooks/` |

### Bước 1.2 — Xác định mục tiêu theo Backward Design

Với MỖI chương (chapter), AI phải xác định theo thứ tự:

```
1. LEARNING OUTCOMES (đầu ra cụ thể)
   → Người đọc sẽ LÀM ĐƯỢC GÌ sau chương này?
   → Sử dụng Bloom's Taxonomy: define, explain, apply, analyze, evaluate, create.
   → Viết 2-4 outcomes đo lường được.

2. ASSESSMENTS (bài đánh giá)
   → Bài tập/dự án nào CHỨNG MINH người đọc đã đạt outcomes?
   → Phân cấp: cơ bản → trung bình → nâng cao.
   → Scaffolding: bài tập nhỏ dẫn đến bài tập lớn.

3. CONTENT (nội dung)
   → Lý thuyết/công cụ nào CẦN THIẾT để làm bài tập trên?
   → CHỈ đưa nội dung phục vụ trực tiếp cho assessments.
   → Bỏ qua kiến thức "hay biết" nhưng không cần cho bài tập.
```

### Bước 1.3 — Phân chia cấu trúc ebook

Từ outline, AI chia thành **Part** (Phần) và **Chapter** (Bài):

```
ebooks/
├── _meta.json                    # Metadata toàn bộ series
├── part_01_ten_phan/
│   ├── _part_meta.json           # Metadata phần
│   ├── chapter_01_ten_bai.md     # Bài 1
│   ├── chapter_02_ten_bai.md     # Bài 2
│   └── assets/                   # Hình ảnh, diagram cho phần này
├── part_02_ten_phan/
│   ├── ...
└── README.md                     # Mục lục tổng + hướng dẫn đọc
```

---

## Phase 2: SCAFFOLD — Tạo khung sườn

### File `_meta.json` (Series metadata)
```json
{
  "title": "Tên series ebook",
  "author": "",
  "audience": "",
  "language": "vi",
  "total_parts": 6,
  "total_chapters": 18,
  "status": "in_progress",
  "created_at": "",
  "updated_at": "",
  "parts": [
    {
      "id": 1,
      "title": "Tên phần",
      "chapters": [1, 2, 3],
      "status": "not_started"
    }
  ]
}
```

### File `_part_meta.json` (Part metadata)
```json
{
  "part_id": 1,
  "title": "Tên phần",
  "description": "Mô tả ngắn",
  "chapters": [
    {
      "id": 1,
      "title": "Tên bài",
      "learning_outcomes": [],
      "status": "not_started",
      "word_count": 0,
      "last_updated": ""
    }
  ]
}
```

---

## Nền tảng viết: Cấu trúc học thuật & Phong cách rõ ràng

AI PHẢI nắm vững hai nền tảng sau TRƯỚC KHI viết bất kỳ chapter nào.

### Cấu trúc văn bản học thuật (Harvard — Gordon Harvey)

Mỗi chương textbook là một bài viết học thuật thu nhỏ. AI phải đảm bảo đủ 6 yếu tố sau:

**1. Motive (Động lực)** — Mở đầu mỗi chương bằng lý do "tại sao cần biết".
- Đặt một câu hỏi, một tình huống thực tế, hoặc một vấn đề mà người đọc sẽ gặp.
- KHÔNG mở đầu bằng định nghĩa khô khan. Trước khi định nghĩa, hãy cho người đọc lý do để quan tâm.
- Ví dụ yếu: *"Gradient descent là thuật toán tối ưu hóa..."*
- Ví dụ tốt: *"Bạn đã xây dựng mô hình nhưng loss không giảm. Làm sao để 'dạy' máy tính tự cải thiện? Gradient descent giải quyết chính xác vấn đề này."*

**2. Thesis (Luận điểm)** — Mỗi phần lý thuyết phải có một mệnh đề/insight cụ thể, không chỉ là "trình bày về X".
- Ví dụ yếu: *"Phần này giới thiệu về overfitting."*
- Ví dụ tốt: *"Overfitting xảy ra khi mô hình 'ghi nhớ' dữ liệu huấn luyện thay vì 'học' quy luật — và regularization buộc mô hình phải đơn giản hơn để tránh điều này."*

**3. Evidence (Bằng chứng)** — Mỗi khẳng định lý thuyết PHẢI kèm bằng chứng cụ thể.
- Code chạy được + output thực tế
- Biểu đồ, bảng số liệu, visualization
- So sánh trước/sau, có/không
- KHÔNG viết khẳng định chung chung mà không chứng minh.

**4. Analysis (Phân tích)** — Sau khi trình bày evidence, PHẢI giải thích nó có nghĩa gì.
- Khi chạy code và thấy kết quả, giải thích: "Kết quả 95% accuracy cho thấy mô hình đã học được pattern chính, nhưng khoảng cách giữa train accuracy (99%) và test accuracy (95%) cho thấy có dấu hiệu overfitting nhẹ."
- KHÔNG chỉ in output rồi bỏ qua.

**5. Key terms (Thuật ngữ)** — Định nghĩa thuật ngữ mới ngay lần đầu sử dụng. Dùng nhất quán xuyên suốt chương và toàn bộ sách.

**6. Structure (Cấu trúc tiến triển)** — Mạch nội dung phải đi theo logic tiến triển, không phải liệt kê rời rạc.
- Mô hình chuẩn: Vấn đề → Giải pháp → Chứng minh bằng code → Phân tích kết quả → Mở rộng/giới hạn
- Mỗi phần xây dựng trên phần trước. Câu đầu mỗi đoạn kết nối với đoạn trước (transition tự nhiên, không dùng "Additionally").
- Nếu có nhiều khái niệm, sắp xếp từ đơn giản → phức tạp, hoặc từ cụ thể → trừu tượng.

### Phong cách viết rõ ràng (Stanford — Joseph M. Williams)

AI phải tuân theo các nguyên tắc viết rõ ràng sau:

**1. Chủ ngữ = nhân vật hành động.** Câu nên bắt đầu bằng ai/cái gì đang làm gì.
- Yếu: *"Việc huấn luyện mô hình được thực hiện bằng gradient descent."*
- Tốt: *"Chúng ta huấn luyện mô hình bằng gradient descent."*
- Yếu: *"Có thể thấy rằng kết quả cho thấy sự cải thiện."*
- Tốt: *"Kết quả cải thiện rõ rệt: accuracy tăng từ 85% lên 93%."*

**2. Động từ = hành động chính.** Tránh biến hành động thành danh từ (nominalization).
- Yếu: *"Sự cải thiện độ chính xác có sự phụ thuộc vào việc lựa chọn learning rate."*
- Tốt: *"Độ chính xác cải thiện khi ta chọn learning rate phù hợp."*
- Yếu: *"Việc thực hiện quá trình tiền xử lý dữ liệu là bước đầu tiên."*
- Tốt: *"Trước tiên, ta tiền xử lý dữ liệu."*

**3. Thông tin cũ trước, thông tin mới sau.** Mỗi câu bắt đầu bằng thông tin đã biết (liên kết với câu trước), rồi dẫn đến thông tin mới ở cuối câu.
- Ví dụ: *"Learning rate kiểm soát bước nhảy. [cũ] Nếu bước nhảy quá lớn, thuật toán sẽ vượt qua điểm tối ưu và dao động. [mới]"*

**4. Cohesion (liên kết câu) và Coherence (mạch đoạn).**
- Cohesion: Cuối câu này dẫn sang đầu câu sau. Đọc liền 2 câu phải thấy mạch nối tự nhiên.
- Coherence: Đọc toàn đoạn phải thấy một luận điểm rõ ràng tiến triển, không phải tập hợp các câu rời rạc.
- Nếu một đoạn có quá nhiều ý, tách thành nhiều đoạn nhỏ, mỗi đoạn 1 ý chính.

**5. Ngắn gọn.** Bỏ từ thừa. Nếu bỏ đi mà câu không mất nghĩa thì bỏ.
- Yếu: *"Về cơ bản thì có thể nói rằng neural network hoạt động theo cách mà nó nhận input."*
- Tốt: *"Neural network nhận input, xử lý qua các lớp, và tạo output."*

### Phong cách tường thuật (Géron Style — Hands-on ML)

AI PHẢI viết theo phong cách tường thuật (narrative), KHÔNG viết dạng slide/bullet. Đây là sự khác biệt quan trọng nhất giữa ebook và bài giảng.

**1. Viết dạng đoạn văn liên tục, KHÔNG viết dạng gạch đầu dòng ngắn.**
Mỗi khái niệm (VD: Supervised Learning, Clustering) phải được trình bày bằng **3-5 đoạn văn** (paragraph), mỗi đoạn 3-5 câu. KHÔNG tóm tắt 1 khái niệm trong 2-3 câu rồi nhảy sang mục khác.
- Yếu: *"Clustering là nhóm các mẫu dữ liệu tương tự nhau lại. Ví dụ: phân nhóm khách hàng."* (2 câu là quá ngắn)
- Tốt: Giải thích clustering là gì (1 đoạn), cho ví dụ cụ thể với dữ liệu thực (1 đoạn), mô tả cách thuật toán hoạt động bằng trực giác (1 đoạn), và giới hạn/lưu ý (1 đoạn).

**2. Dùng một ví dụ xuyên suốt (running example).**
Chọn một ví dụ thực tế và dùng lại xuyên suốt chương để minh họa nhiều khái niệm. Géron dùng "spam filter" xuyên suốt chương 1 để giải thích Supervised, ML vs truyền thống, online learning, v.v. Ví dụ xuyên suốt giúp người đọc không bị "nhảy" giữa các tình huống rời rạc.

**3. Giọng văn "conversational" (trò chuyện).**
Dùng ngôi thứ hai ("bạn", "you") và ngôi thứ nhất số nhiều ("chúng ta", "we"). Nghĩ như đang giải thích cho một sinh viên ngồi trước mặt.
- Yếu: *"Supervised Learning được định nghĩa là phương pháp học từ dữ liệu có nhãn."*
- Tốt: *"Giả sử bạn có 1000 email, mỗi email đã được gắn nhãn 'spam' hoặc 'không spam'. Bạn đưa toàn bộ cho máy tính và nói: 'Hãy tìm ra quy luật để phân loại email mới'. Đó là Supervised Learning."*

**4. Chuyển tiếp tự nhiên giữa các phần.**
Không nhảy đột ngột từ mục này sang mục khác. Cuối mỗi phần, viết 1-2 câu dẫn sang phần tiếp theo. Ví dụ: *"Chúng ta đã thấy cách Supervised Learning hoạt động khi có nhãn. Nhưng nếu dữ liệu không có nhãn thì sao?"*

**5. Độ sâu nội dung: mỗi sub-concept trình bày 3-5 paragraph.**
Khi giới thiệu một khái niệm con (VD: Clustering, Dimensionality Reduction, Anomaly Detection), viết 3-5 đoạn văn bao gồm:
- Định nghĩa/giải thích bằng trực giác
- Ví dụ thực tế cụ thể (không phải "VD: phân nhóm khách hàng" mà phải mô tả cụ thể tình huống)
- Cách hoạt động (ở mức trực giác)
- Khi nào dùng, khi nào không nên dùng

**6. Không dùng bảng so sánh thay thế nội dung.**
Bảng chỉ là tóm tắt cuối phần, KHÔNG phải nội dung chính. Nội dung chính PHẢI là đoạn văn giải thích chi tiết.

---

## Phase 3: WRITE — Viết nội dung

### Template chuẩn cho mỗi Chapter (Bài)

```markdown
# [Tên bài học]

> **Phần [X]** · Bài [Y] · [Tên series]

## Mục tiêu bài học
Sau khi hoàn thành bài này, bạn sẽ:
- Giải thích được ... (Understand)
- Xây dựng được ... (Apply/Create)
- Phân biệt được ... (Analyze)

## Kiến thức cần có
- Bài trước: [link]
- Yêu cầu: ...

---

## 1. [Vấn đề cần giải quyết — Motive]

Tại sao chúng ta cần biết điều này? Bắt đầu bằng một tình huống
thực tế, một câu hỏi, hoặc một vấn đề mà người đọc sẽ gặp.

## 2. [Khái niệm cốt lõi — Thesis + Evidence]

### 2.1 [Khái niệm A]
Giải thích trực quan, dùng analogy nếu phù hợp.

> **Ví dụ đời sống:** [Analogy giúp dễ hình dung]

### 2.2 [Khái niệm B]
Nội dung chuyên sâu hơn. Mỗi khẳng định kèm bằng chứng
(code, data, hoặc visualization).

---

## 3. Thực hành

### Bài thực hành 1: [Tên]

**Mục tiêu:** Liên kết trực tiếp với Learning Outcome nào.

```python
# Code mẫu có comment chi tiết
import numpy as np

# Bước 1: Chuẩn bị dữ liệu
data = np.array([1, 2, 3])  # Tạo mảng numpy
```

**Giải thích code:**
- Dòng 1: ...
- Dòng 2: ...

**Kết quả mong đợi:**
```
Output: [1 2 3]
```

---

## Lưu ý quan trọng và lỗi thường gặp

> [!WARNING]
> **[Tên lỗi phổ biến]:** Mô tả lỗi và cách tránh.

> [!TIP]
> **Mẹo:** Gợi ý hữu ích cho thực hành.

---

## Tổng kết

| Khái niệm | Ý nghĩa | Khi nào dùng |
|------------|----------|-------------|
| ... | ... | ... |

Điểm chính cần nhớ:
1. ...
2. ...

---

## Bài tập tự luyện

### Bài 1 (Cơ bản)
Gắn với Learning Outcome cụ thể. Mô tả yêu cầu rõ ràng.

### Bài 2 (Trung bình)
Yêu cầu kết hợp nhiều khái niệm trong bài.

### Bài 3 (Nâng cao)
Mở rộng ra tình huống thực tế hoặc yêu cầu sáng tạo.

---

## Tài liệu tham khảo
- [Tên tài liệu](link)

---
*Bài tiếp theo: [Tên bài kế tiếp] →*
```

### Quy tắc viết nội dung

#### A. Cấu trúc nội dung (Backward Design + Harvard)

AI PHẢI áp dụng 6 yếu tố Harvard và nguyên tắc Backward Design (đã mô tả chi tiết ở phần "Nền tảng viết" phía trên) vào mỗi chapter:

1. Mở đầu bằng **Motive** (tình huống/câu hỏi thực tế), KHÔNG bằng định nghĩa khô khan.
2. Mỗi phần lý thuyết có **Thesis** cụ thể (mệnh đề/insight), KHÔNG chỉ "giới thiệu về X".
3. Mọi khẳng định kèm **Evidence** (code chạy được, data, visualization). KHÔNG khẳng định suông.
4. Sau evidence PHẢI có **Analysis** — giải thích kết quả có nghĩa gì, không chỉ in output.
5. **Key terms** định nghĩa ngay lần đầu, dùng nhất quán xuyên suốt.
6. **Structure** tiến triển: Vấn đề → Giải pháp → Code chứng minh → Phân tích → Mở rộng. KHÔNG liệt kê rời rạc.
7. Lý thuyết PHẢI phục vụ trực tiếp cho phần Thực hành (Assessments). Không đưa nội dung dư thừa.
8. Mỗi khái niệm MỚI phải có ít nhất 1 ví dụ minh họa. Code snippet PHẢI có comment và giải thích.
9. Tham chiếu ngược lại bài trước khi dùng kiến thức cũ. Mỗi bài tăng dần độ khó.

#### B. Phong cách viết (Stanford Clarity + Anti-AI)

AI PHẢI áp dụng 5 nguyên tắc Stanford (đã mô tả chi tiết ở phần "Nền tảng viết" phía trên):

10. **Chủ ngữ hành động:** Câu bắt đầu bằng ai/cái gì hành động. Tránh câu thụ động không cần thiết.
11. **Tránh nominalization:** Không biến hành động thành danh từ ("Sự cải thiện" → "cải thiện").
12. **Thông tin cũ → mới:** Đầu câu = thông tin đã biết, cuối câu = thông tin mới.
13. **Cohesion + Coherence:** Câu nối câu tự nhiên, đoạn có luận điểm rõ ràng tiến triển.
14. **Ngắn gọn:** Bỏ từ thừa. Nếu bỏ đi không mất nghĩa thì bỏ.
15. **Giọng văn tự nhiên, trung lập:** Thân thiện nhưng chính xác. Không dùng giọng PR/quảng cáo.
16. **Thuật ngữ nhất quán:** Gọi đúng tên xuyên suốt, tránh "elegant variation" ("Python" → "ngôn ngữ lập trình này" → "công cụ nói trên").

#### C. Anti-AI Vocabulary (PHẢI tuân thủ)

11. **KHÔNG dùng các từ sau** (hoặc tương đương tiếng Việt):
    - crucial, pivotal, vital → dùng: important, useful
    - delve, underscore, showcase, foster → dùng: explore, show, support
    - tapestry, landscape (nghĩa bóng), testament → dùng: mix, field, example
    - vibrant, intricate, meticulous, enduring → dùng: lively, complex, careful, lasting
    - Additionally/Moreover/Furthermore (đầu câu máy móc) → viết lại câu tự nhiên

12. **KHÔNG dùng cấu trúc AI đặc trưng:**
    - Rule of Three: liệt kê đúng 3 tính từ/mệnh đề (nhanh, hiệu quả, đáng tin cậy)
    - Negative parallelism: "Không chỉ là X, mà còn là Y"
    - "Despite challenges": "Bất chấp thách thức, tương lai hứa hẹn..."
    - Superficial analysis: chèn mệnh đề "vĩ mô" ở cuối câu ("...là minh chứng cho sự phát triển...")
    - Puffery: mô tả mọi thứ là groundbreaking, revolutionary, game-changing

#### D. Định dạng (Formatting)

13. **In đậm:** Chỉ in đậm thuật ngữ khi định nghĩa lần đầu. KHÔNG in đậm cả cụm từ/câu dài.
14. **Danh sách:** Tránh lạm dụng inline-header lists (`- **Tên:** Mô tả dài`). Ưu tiên viết thành đoạn văn hoặc dùng heading nhỏ.
15. **Dấu câu:** Không lạm dụng em dash (—). Dùng dấu phẩy, ngoặc đơn, hoặc tách câu.
16. **Emoji:** Hạn chế tối đa trong giáo trình. Không dùng emoji làm bullet point.
17. **Heading:** Dùng Sentence case (viết hoa chữ đầu), không dùng Title Case.
18. **Độ sâu:** Mỗi nội dung/khái niệm trình bày 3-5 paragraph. Không giới hạn số từ cụ thể.

### Quy trình viết 1 chapter

```
1. AI đọc outline + context bài trước (nếu có)
2. AI xác định Learning Outcomes + Assessments TRƯỚC
3. AI viết draft đầy đủ theo template
4. AI tự review theo Anti-AI Checklist (xem bên dưới)
5. Lưu file + update _part_meta.json (status, word_count)
6. Thông báo user review
```

### Anti-AI Self-Review Checklist

Sau khi viết xong mỗi chapter, AI PHẢI tự kiểm tra toàn bộ các mục sau:

```
BACKWARD DESIGN
□ Có Learning Outcomes cụ thể, đo lường được (dùng Bloom's verbs)?
□ Bài tập/thực hành trực tiếp đo Outcomes?
□ Mọi lý thuyết phục vụ trực tiếp cho bài tập? (Không có nội dung thừa?)
□ Bài mở đầu bằng Motive (tại sao cần biết)?

HARVARD ELEMENTS
□ Mỗi phần lý thuyết có thesis/insight rõ ràng?
□ Có evidence cụ thể (code, data, ví dụ)?
□ Có analysis (giải thích kết quả)?
□ Thuật ngữ (key terms) được định nghĩa và dùng nhất quán?

ANTI-AI VOCABULARY
□ Không chứa từ: crucial, pivotal, delve, underscore, tapestry, vibrant, intricate, testament, showcase, foster, garner?
□ Không bắt đầu câu máy móc bằng "Additionally," / "Moreover," / "Furthermore,"?
□ Không có tương đương tiếng Việt: then chốt, tối quan trọng, bức tranh toàn cảnh, minh chứng sống động?

ANTI-AI STRUCTURE
□ Không có Rule of Three (3 tính từ/mệnh đề liệt kê)?
□ Không có Negative Parallelism ("Không chỉ X mà còn Y")?
□ Không kết thúc bằng "Despite challenges / Bất chấp thách thức"?
□ Không chèn Superficial Analysis (mệnh đề đánh giá vĩ mô cuối câu)?
□ Không Puffery (groundbreaking, revolutionary)?
□ Không Elegant Variation (đổi tên gọi liên tục để tránh lặp)?

ANTI-AI FORMATTING
□ Không lạm dụng in đậm (chỉ in đậm thuật ngữ lần đầu)?
□ Không lạm dụng inline-header lists?
□ Không lạm dụng em dash (—)?
□ Không dùng emoji làm bullet?
□ Heading dùng Sentence case?

CHẤT LƯỢNG
□ Code chạy được, output đúng?
□ Thuật ngữ nhất quán với các bài trước?
□ Liên kết bài trước/sau rõ ràng?
□ Có phần lưu ý/lỗi thường gặp?
□ Câu rõ ràng (chủ ngữ hành động, tránh nominalization)?
```

---

## Phase 4: REVIEW — Kiểm tra chất lượng

### Checklist tự đánh giá (AI tự kiểm tra)
- [ ] **Accuracy:** Kiến thức chính xác, không sai kỹ thuật
- [ ] **Completeness:** Đủ nội dung theo outline và Learning Outcomes
- [ ] **Code works:** Code snippet chạy được, output đúng
- [ ] **Consistency:** Thuật ngữ nhất quán với các bài trước
- [ ] **Flow:** Mạch logic tiến triển (vấn đề → giải pháp → chứng minh → mở rộng)
- [ ] **Accessibility:** Đối tượng target đọc hiểu được
- [ ] **Anti-AI:** Đã chạy qua Anti-AI Self-Review Checklist ở trên

### User review
Sau khi AI viết xong, dùng `notify_user` với:
- `PathsToReview`: đường dẫn file chapter vừa viết
- Gợi ý check: giọng văn, độ chi tiết, thuật ngữ, tính tự nhiên

---

## Phase 5: EXPORT — Xuất bản

### Hỗ trợ export (khi user yêu cầu)
- **Pandoc → PDF/DOCX:** `pandoc chapter.md -o chapter.pdf`
- **Jupyter Book:** Chuyển md → notebook format
- **Quarto:** Render thành website/PDF chuyên nghiệp
- **MkDocs:** Tạo site tài liệu online

AI sẽ tạo script export phù hợp khi user cần.

---

## Tích hợp với các Workflow/Skill khác

### Auto-save (awf-auto-save)
- Sau mỗi chapter viết xong → auto-save session
- Track tiến độ: bao nhiêu chapter done

### Context-help (awf-context-help)
- Khi user hỏi về quy trình viết → giải thích phase hiện tại
- Gợi ý `/textbook` khi detect ý định viết sách

---

## Ví dụ sử dụng

### Tạo khung sườn mới
```
User: /textbook
AI: Tôi cần biết:
    1. Chủ đề sách?
    2. Đối tượng đọc?
    3. Bạn có outline/kế hoạch sẵn không?
    4. Ngôn ngữ viết?
```

### Viết chapter cụ thể
```
User: Viết Bài 1 Phần 1 cho ebook Machine Learning
AI: [Đọc _meta.json → xác định Outcomes + Assessments → viết theo template → chạy Anti-AI checklist → save]
```

### Tiếp tục viết
```
User: Viết bài tiếp theo
AI: [Đọc _part_meta.json → tìm bài chưa viết → viết → save]
```
