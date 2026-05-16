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

### Tài liệu tham khảo (reference/) — BẮT BUỘC

Thư mục `reference/` chứa nội dung trích xuất từ sách tham khảo, được tổ chức theo chương. Xem `reference/INDEX.md` để biết danh sách file và mục lục chi tiết.

**Quy tắc ưu tiên khi cần kiến thức chuyên môn (BẮT BUỘC):**
1. **Đọc `reference/INDEX.md` TRƯỚC** — tìm chương tham khảo tương ứng với bài đang viết (xem bảng mapping cuối INDEX)
2. **`grep_search` trong `reference/`** — tìm thuật ngữ, khái niệm cụ thể trong các file chương
3. **Tìm trên internet** — chỉ khi reference/ không có hoặc không đủ
4. **Dùng kiến thức nội tại** — chỉ khi cả hai nguồn trên không khả dụng

AI PHẢI:
- Đọc INDEX.md ở đầu mỗi bài mới để xác định nguồn tham khảo
- Đối chiếu nội dung viết với tài liệu tham khảo để đảm bảo tính chính xác
- Trích dẫn/tham chiếu nguồn khi sử dụng kiến thức từ reference/

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
| `style` | Giọng văn | ❌ mặc định: **academic-narrative** (bắt buộc tuyệt đối) |
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

**1. Motive (Động lực)** — Mở đầu mỗi chương bằng bối cảnh vấn đề cần giải quyết.
- Đặt bối cảnh thực tế hoặc mô tả vấn đề mà nội dung chương sẽ giải quyết.
- KHÔNG mở đầu bằng định nghĩa khô khan. Trước khi định nghĩa, cần trình bày lý do tồn tại của khái niệm đó.
- Ví dụ yếu: *"Gradient descent là thuật toán tối ưu hóa..."*
- Ví dụ tốt: *"Quá trình huấn luyện mô hình đòi hỏi một phương pháp tối ưu có khả năng cập nhật tham số theo hướng giảm thiểu hàm mất mát. Gradient Descent là thuật toán nền tảng thực hiện nhiệm vụ này."*

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

### ⛔ VĂN PHONG ACADEMIC-NARRATIVE — BẮT BUỘC TUYỆT ĐỐI

> **ĐÂY LÀ QUY TẮC CÓ ĐỘ ƯU TIÊN CAO NHẤT TRONG TOÀN BỘ SKILL NÀY.**
> AI PHẢI tuân thủ tuyệt đối mọi quy tắc văn phong dưới đây. Vi phạm bất kỳ điểm nào
> đều khiến bài viết KHÔNG ĐẠT CHUẨN và phải viết lại.

AI PHẢI viết theo phong cách **academic-narrative** — văn phong khoa học, hàn lâm, câu cú chặt chẽ, cô đọng, không có từ thừa, nhưng vẫn trình bày dạng tường thuật liên tục (không phải slide/bullet).

#### 1. Giọng văn: khoa học, hàn lâm, cô đọng

- **KHÔNG dùng giọng trò chuyện (conversational).** Textbook không phải podcast hay blog.
- **KHÔNG dùng từ đệm/thừa:** "đừng lo", "rất trực quan", "khá đơn giản", "thực ra", "nói cách khác", "xét cho cùng", "hấp dẫn nhất", "thú vị".
- **KHÔNG dùng khẩu ngữ:** "sai bét", "nhảy thẳng vào", "ghi nhớ", "dở đến mức nào", "quen tay".
- **KHÔNG dùng từ cảm thán/đánh giá chủ quan:** "tuyệt vời", "rất hay", "đáng kinh ngạc".
- Mỗi câu phải mang thông tin. Nếu bỏ một từ/cụm từ mà câu không mất nghĩa → bỏ ngay.
- Yếu: *"Bình phương có hai ưu điểm. Thứ nhất, nó phạt nặng các sai số lớn: một dự đoán lệch 10 đơn vị bị phạt gấp 100 lần so với một dự đoán lệch 1 đơn vị."*
- Tốt: *"Phép bình phương làm gia tăng đáng kể mức độ đóng góp của các sai số lớn vào giá trị hàm mất mát. Cụ thể, sai số có độ lớn càng cao sẽ bị khuếch đại theo bậc hai, buộc mô hình ưu tiên hiệu chỉnh các dự đoán có sai lệch lớn."*

#### 2. Ngôi kể

- **Phần lý thuyết:** Dùng câu vô nhân xưng hoặc "ta". *"Mô hình được huấn luyện trên tập dữ liệu gồm 16.000 mẫu."*, *"Ta xét hàm mất mát MSE."*
- **Phần thực hành/code:** Được dùng "chúng ta". *"Chúng ta áp dụng LinearRegression trên bộ California Housing."*
- **KHÔNG lạm dụng ngôi "bạn".** Chỉ dùng "bạn" trong phần Bài tập tự luyện. KHÔNG dùng "bạn" trong phần lý thuyết hay thực hành.

#### 3. Câu hỏi

- **KHÔNG dùng câu hỏi tu từ dân dã:** *"Tại sao lại bình phương chứ không lấy trị tuyệt đối?"*, *"Vậy làm sao biết?"*, *"Bạn sẽ làm gì?"*
- **Được dùng câu hỏi nghiên cứu ở đầu mục** để đặt vấn đề, nhưng phải viết dạng hàn lâm:
  - Yếu: *"Câu hỏi bây giờ là: khi nào một mô hình có MSE thấp lại không phải là mô hình tốt?"*
  - Tốt: *"Vấn đề đặt ra là liệu một mô hình có MSE thấp trên tập huấn luyện có nhất thiết khái quát hóa tốt trên dữ liệu mới."*

#### 4. Analogy (phép so sánh tương tự)

- Analogy **tối đa 1-2 câu**, sau đó chuyển ngay sang thuật ngữ kỹ thuật.
- **KHÔNG kéo dài analogy qua nhiều câu/đoạn.**
- Yếu: *"Hãy tưởng tượng bạn đang đứng trên một ngọn đồi trong sương mù dày đặc. Bạn không nhìn thấy toàn cảnh, chỉ cảm nhận được mặt đất dưới chân. Mục tiêu là tìm đường xuống đáy thung lũng. Bạn sẽ làm gì? Cách tự nhiên nhất: dò mặt đất xung quanh..."* (5 câu analogy)
- Tốt: *"Gradient Descent có thể hình dung như bài toán tìm điểm thấp nhất trên một bề mặt khi tầm nhìn bị giới hạn. Tại mỗi vị trí, thuật toán xác định hướng có độ dốc lớn nhất và thực hiện một bước dịch chuyển theo hướng ngược lại — tức hướng mà hàm mất mát giảm nhanh nhất."* (2 câu, chuyển ngay sang kỹ thuật)

#### 5. Thuật ngữ

- Dùng thuật ngữ chính xác: "ước lượng" (không phải "tìm ra"), "hiệu chỉnh" (không phải "sửa"), "sai lệch" (không phải "sai bét"), "khả vi" (không phải "mượt").
- Khi giới thiệu thuật ngữ mới lần đầu: in đậm thuật ngữ tiếng Việt, kèm thuật ngữ gốc Anh trong ngoặc. Ví dụ: **hàm mất mát** (loss function).
- Sau lần định nghĩa đầu, sử dụng nhất quán, không giải thích lại, không đổi tên gọi.

#### 6. Cấu trúc câu

- Mỗi câu tối đa 1-2 mệnh đề. Câu dài hơn 30 từ nên tách thành 2 câu.
- Ưu tiên câu khẳng định. Hạn chế câu hỏi.
- Câu bị động được phép trong ngữ cảnh khoa học: *"Mô hình được huấn luyện trên 16.000 mẫu"*.
- **KHÔNG viết câu dạng podcast/blog:** *"Giờ hãy quay lại..."*, *"OK, bây giờ..."*, *"Hãy tưởng tượng..."*

#### 7. Chuyển tiếp giữa các phần

- Cuối mỗi phần, viết 1-2 câu dẫn sang phần tiếp theo bằng giọng hàn lâm.
- Yếu: *"Giờ hãy quay lại bộ dữ liệu California Housing quen thuộc."*
- Tốt: *"Với nền tảng lý thuyết đã trình bày, phần tiếp theo áp dụng Linear Regression trên bộ dữ liệu California Housing."*

#### 8. Viết dạng đoạn văn liên tục, KHÔNG viết dạng gạch đầu dòng ngắn

Mỗi khái niệm phải được trình bày bằng **3-5 đoạn văn**, mỗi đoạn 3-5 câu. KHÔNG tóm tắt 1 khái niệm trong 2-3 câu rồi chuyển sang mục khác.

#### 9. Dùng một ví dụ xuyên suốt (running example)

Chọn một ví dụ thực tế và dùng lại xuyên suốt chương để minh họa nhiều khái niệm. Ví dụ xuyên suốt giúp người đọc không phải chuyển đổi ngữ cảnh liên tục.

#### 10. Không dùng bảng so sánh thay thế nội dung

Bảng chỉ là tóm tắt cuối phần, KHÔNG phải nội dung chính. Nội dung chính PHẢI là đoạn văn giải thích chi tiết.

#### 11. Chuẩn hóa ngôn từ học thuật — KHÔNG dùng từ biểu cảm

> **QUY TẮC BẮT BUỘC:** Trong văn bản học thuật, mọi từ ngữ biểu cảm, ẩn dụ cảm xúc,
> hoặc tu từ văn học PHẢI được thay thế bằng thuật ngữ kỹ thuật chính xác.

AI PHẢI rà soát và thay thế toàn bộ các từ biểu cảm bằng thuật ngữ chuyên ngành. Bảng tham chiếu dưới đây liệt kê các trường hợp phổ biến:

| Từ biểu cảm (CẤM) | Thuật ngữ thay thế (BẮT BUỘC) |
|---|---|
| trái tim, linh hồn | cơ sở cốt lõi, thành phần trung tâm |
| thảm họa, tai họa | hạn chế toán học, giới hạn lý thuyết |
| trống rỗng, rỗng tuếch | không có giai đoạn tối ưu hóa tham số |
| sụp đổ, tan vỡ | vượt quá khả năng xử lý, mất tính ổn định |
| nghiền nát, đè bẹp | lấn át phương sai, chi phối hoàn toàn |
| ngớ ngẩn, ngu ngốc | không phù hợp, thiếu cơ sở lý thuyết |
| gục ngã, chết yểu | không hội tụ, mất hiệu lực |
| bùng nổ, cháy nổ | tăng trưởng không kiểm soát, phân kỳ |
| ma thuật, phép thuật | cơ chế toán học, phép biến đổi |
| kẻ thù, đối thủ | yếu tố gây nhiễu, thách thức kỹ thuật |
| vũ khí, công cụ sắc bén | phương pháp hiệu quả, kỹ thuật tối ưu |
| chiến đấu, xung trận | giải quyết, xử lý |

**Nguyên tắc tổng quát:** Nếu một từ/cụm từ mang tính cảm xúc, văn học, hoặc khẩu ngữ — thay thế bằng thuật ngữ kỹ thuật trung tính, chính xác nhất có thể. Đọc lại toàn bộ bài viết ít nhất một lần để phát hiện các từ biểu cảm còn sót lại.

#### 12. Mở rộng đoạn văn (Paragraph Expansion) — Chiều sâu lý luận

> **QUY TẮC BẮT BUỘC:** Mỗi khái niệm kỹ thuật quan trọng PHẢI được mở rộng
> bằng phân tích định lượng, dẫn giải toán học, hoặc ví dụ minh họa cụ thể.

AI KHÔNG được viết đoạn văn chỉ gồm 1-2 câu định nghĩa rồi chuyển sang mục khác. Mỗi đoạn PHẢI có chiều sâu:

- **Phân tích định lượng:** Bổ sung công thức, hằng số, hoặc ước lượng cụ thể. Ví dụ: thay vì viết "KNN tốn bộ nhớ", viết "Với tập dữ liệu MNIST (60,000 mẫu × 784 chiều, kiểu float64), mô hình KNN yêu cầu $60{,}000 \times 784 \times 8 \approx 376$ MB RAM chỉ riêng cho việc lưu trữ dữ liệu huấn luyện."
- **Dẫn giải bằng công thức:** Khi đề cập đến hiện tượng toán học (như Lời nguyền chiều không gian), PHẢI dẫn giải bằng công thức cụ thể (ví dụ: hàm Gamma cho thể tích siêu hình cầu) chứ không chỉ mô tả bằng lời.
- **Ví dụ minh họa:** Sau mỗi khái niệm trừu tượng, bổ sung ít nhất 1 ví dụ có số liệu cụ thể. Sử dụng dạng "Ví dụ:" (không dùng "Ví dụ thực tế:").
- **Phân tích hệ quả:** Giải thích tại sao hiện tượng/công thức đó quan trọng, nó ảnh hưởng đến mô hình như thế nào trong thực hành.

#### 13. Chuỗi dẫn giải công thức (Formula Derivation Chain) — BẮT BUỘC

> **QUY TẮC BẮT BUỘC:** Mọi công thức toán học trong bài PHẢI được trình bày
> theo chuỗi dẫn giải đầy đủ, không được đặt công thức rồi bỏ qua.

Chuỗi dẫn giải gồm 5 bước (không nhất thiết phải có tất cả, nhưng PHẢI có ít nhất 3/5):

```
1. ĐỘNG LỰC (Motivation): Tại sao cần công thức này? Nó giải quyết vấn đề gì?
2. DẠNG TỔNG QUÁT (General Form): Trình bày công thức gốc đầy đủ.
3. GIẢI THÍCH THAM SỐ (Parameter Explanation): Mỗi ký hiệu/biến trong công thức
   đều PHẢI được giải thích rõ ràng (tên, ý nghĩa vật lý, đơn vị nếu có).
4. BIẾN ĐỔI / TRƯỜNG HỢP ĐẶC BIỆT (Derivation/Special Cases):
   - Biến đổi từ dạng tổng quát sang dạng cụ thể (nếu có).
   - Hoặc trình bày các trường hợp đặc biệt khi tham số thay đổi.
   - Ví dụ: Minkowski Distance với p=1 → Manhattan, p=2 → Euclidean.
5. ỨNG DỤNG / VÍ DỤ (Application/Example):
   - Khi nào dùng công thức này?
   - Ví dụ tính toán cụ thể với số liệu (nếu phù hợp).
   - Hoặc mô tả bài toán thường áp dụng.
```

**Ví dụ ĐÚNG chuẩn (5 bước):**
```
[Motivation] Để xác định mẫu nào là láng giềng gần nhất, ta cần đo
lường khoảng cách hình học giữa các vector đặc trưng.

[General Form] $d(\mathbf{a}, \mathbf{b}) = \left( \sum |a_i - b_i|^p \right)^{1/p}$

[Parameters] Trong đó: p là bậc (order) kiểm soát dạng hình học,
a_i và b_i là tọa độ của hai vector trên chiều thứ i.

[Special Cases] Khi p=1 → Manhattan Distance (tổng trị tuyệt đối).
Khi p=2 → Euclidean Distance (đường thẳng tuyến tính).

[Application] Euclidean phù hợp cho dữ liệu có phương sai đồng
nhất. Manhattan chịu nhiễu tốt hơn khi dữ liệu có outliers.
```

**Ví dụ SAI (chỉ đặt công thức rồi bỏ qua):**
```
Khoảng cách Minkowski: $d(a,b) = (\sum |a_i - b_i|^p)^{1/p}$
(Không giải thích gì thêm, chuyển sang mục khác)
```

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

#### B. Thực thi code & Xuất biểu đồ — BẮT BUỘC

> **QUY TẮC BẮT BUỘC:** Mọi code trong textbook PHẢI được chạy thực tế. Biểu đồ PHẢI được lưu vào assets/.

10. **Chạy code:** AI PHẢI thực thi code Python trong bài để lấy kết quả thực. KHÔNG viết output giả hoặc "Kết quả mong đợi" mà không chạy.
11. **Xuất biểu đồ:** Mọi biểu đồ (`plt.show()`) PHẢI được lưu dưới dạng file ảnh vào thư mục `assets/` cùng cấp với bài viết, sử dụng `plt.savefig('assets/baiXX_ten_bieu_do.png', dpi=150, bbox_inches='tight')`. Ảnh này sẽ được nhúng vào file .md để export sang DOCX.
12. **Giải thích biểu đồ bằng giọng hàn lâm:** Bên dưới mỗi biểu đồ, PHẢI có đoạn phân tích chi tiết (3-5 câu) bằng văn phong khoa học. Không dùng bullet point ngắn. Ví dụ:
    - Yếu: *"- Xu hướng tăng. - Phân tán rộng."*
    - Tốt: *"Hình X cho thấy mối quan hệ tuyến tính dương giữa thu nhập trung bình và giá nhà. Tuy nhiên, phương sai của biến phản hồi gia tăng đáng kể ở vùng thu nhập cao (hiện tượng heteroscedasticity), cho thấy thu nhập chỉ giải thích được một phần biến động giá nhà. Ngoài ra, sự tập trung của các quan sát tại ngưỡng giá trị 5.0 phản ánh cơ chế truncation trong quá trình thu thập dữ liệu."*

#### C. File thực hành kèm theo — BẮT BUỘC

> **QUY TẮC BẮT BUỘC:** Mỗi bài textbook PHẢI kèm file thực hành Python (.py) đặt cùng thư mục.

13. **Tạo file thực hành:** Sau khi viết xong nội dung bài textbook (.md), AI PHẢI tạo file thực hành Python đặt cùng thư mục. Ví dụ: `bai_05_da_bien_polynomial.md` → `Bai_05_DaBien_Polynomial.py`.
14. **Format file thực hành:** Tuân theo mẫu các bài 02-04 tại `Bai giang/`. Cấu trúc:
    - Header docstring: tên bài, mục tiêu thực hành, kiến thức cần có
    - Chia thành các PHẦN (section) rõ ràng: `# ============ PHẦN X: TÊN ============`
    - Phần markdown (giải thích) nằm trong triple-quote `""" ... """`
    - Code nằm bên ngoài triple-quote
    - Mỗi biểu đồ có nhận xét ngay bên dưới (trong triple-quote)
    - Kết thúc bằng Bài tập tự luyện (3 cấp: cơ bản, trung bình, nâng cao)
15. **Convert sang notebook:** File .py có thể convert sang .ipynb bằng `convert.py` trong `Bai giang/`.
16. **Nội dung thực hành:** Code trong file thực hành PHẢI thực thi được end-to-end (chạy từ đầu đến cuối không lỗi) và bao phủ toàn bộ khái niệm lý thuyết trong bài.

#### D. Phong cách viết (Stanford Clarity + Anti-AI)

AI PHẢI áp dụng 5 nguyên tắc Stanford (đã mô tả chi tiết ở phần "Nền tảng viết" phía trên):

17. **Chủ ngữ hành động:** Câu bắt đầu bằng ai/cái gì hành động. Tránh câu thụ động không cần thiết.
18. **Tránh nominalization:** Không biến hành động thành danh từ ("Sự cải thiện" → "cải thiện").
19. **Thông tin cũ → mới:** Đầu câu = thông tin đã biết, cuối câu = thông tin mới.
20. **Cohesion + Coherence:** Câu nối câu tự nhiên, đoạn có luận điểm rõ ràng tiến triển.
21. **Ngắn gọn:** Bỏ từ thừa. Nếu bỏ đi không mất nghĩa thì bỏ.
22. **Giọng văn academic-narrative:** Khoa học, hàn lâm, cô đọng. KHÔNG dùng giọng trò chuyện, blog, hay PR. Xem chi tiết tại mục "⛔ VĂN PHONG ACADEMIC-NARRATIVE" phía trên.
23. **Thuật ngữ nhất quán:** Gọi đúng tên xuyên suốt, tránh "elegant variation" ("Python" → "ngôn ngữ lập trình này" → "công cụ nói trên").

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
1. Đọc reference/INDEX.md → xác định chương tham khảo tương ứng
2. Đọc reference/ chapters liên quan → thu thập kiến thức
3. Đọc outline + context bài trước (nếu có)
4. Xác định Learning Outcomes + Assessments TRƯỚC
5. Viết draft đầy đủ theo template
6. Chạy tất cả code, lưu biểu đồ vào assets/
7. Tạo file thực hành .py cùng thư mục (theo format Bai giang/)
8. Tự review theo Anti-AI Checklist (xem bên dưới)
9. Lưu file + update _part_meta.json (status, word_count)
10. Thông báo user review
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

⛔ ACADEMIC TONE (BẮT BUỘC TUYỆT ĐỐI)
□ Không có câu hỏi tu từ dân dã ("Tại sao lại...?", "Vậy làm sao?", "Bạn sẽ làm gì?")?
□ Không có từ đệm thừa ("đừng lo", "rất trực quan", "khá đơn giản", "xét cho cùng")?
□ Không có khẩu ngữ ("sai bét", "nhảy thẳng vào", "quen tay", "dở đến mức nào")?
□ Không lạm dụng ngôi "bạn" (chỉ dùng ở bài tập tự luyện)?
□ Analogy ngắn gọn (≤ 2 câu), không kéo dài qua nhiều đoạn?
□ Thuật ngữ chính xác, dùng từ hàn lâm thay khẩu ngữ?
□ Câu cô đọng, mỗi câu ≤ 2 mệnh đề, không nhồi nhiều ý?
□ Không có câu dạng podcast/blog ("Giờ hãy...", "OK bây giờ...", "Hãy tưởng tượng...")?
□ Chuyển tiếp giữa các phần bằng giọng hàn lâm, không suồng sã?

CHUẨN HÓA NGÔN TỪ (BẮT BUỘC)
□ Không chứa từ biểu cảm/ẩn dụ cảm xúc (thảm họa, trái tim, sụp đổ, nghiền nát, ma thuật...)?
□ Mọi từ biểu cảm đã được thay thế bằng thuật ngữ kỹ thuật trung tính?
□ Đã rà soát toàn bộ bài viết ít nhất 1 lần để phát hiện từ biểu cảm sót?

MỞ RỘNG ĐOẠN VĂN (BẮT BUỘC)
□ Mỗi khái niệm quan trọng có ≥ 3 câu phân tích (không chỉ 1-2 câu định nghĩa)?
□ Có phân tích định lượng (công thức, số liệu, ước lượng cụ thể)?
□ Mỗi khái niệm trừu tượng có ít nhất 1 ví dụ minh họa?
□ Dùng dạng "Ví dụ:" (không dùng "Ví dụ thực tế:")?

CHUỖI DẪN GIẢI CÔNG THỨC (BẮT BUỘC)
□ Mỗi công thức có ít nhất 3/5 bước: Động lực → Dạng tổng quát → Giải thích tham số → Biến đổi → Ứng dụng?
□ Không có công thức nào được đặt rồi bỏ qua không giải thích?
□ Mỗi ký hiệu/biến trong công thức đều được định nghĩa rõ ràng?

CHẤT LƯỢNG
□ Code chạy được, output đúng?
□ Thuật ngữ nhất quán với các bài trước?
□ Liên kết bài trước/sau rõ ràng?
□ Có phần lưu ý/lỗi thường gặp?
□ Câu rõ ràng (chủ ngữ hành động, tránh nominalization)?

SẢN PHẨM ĐI KÈM (BẮT BUỘC)
□ Đã tìm kiếm trong reference/ trước khi viết?
□ Mọi biểu đồ đã lưu vào assets/ (dạng .png)?
□ Mỗi biểu đồ có đoạn phân tích hàn lâm 3-5 câu bên dưới?
□ Đã tạo file thực hành .py cùng thư mục với bài?
□ File .py chạy end-to-end không lỗi?
□ File .py theo format mẫu Bai giang/ (header, sections, triple-quote)?
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
