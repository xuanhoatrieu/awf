---
name: awf-question-gen
description: >-
  Sinh câu hỏi trắc nghiệm tự động từ nội dung ebook ML.
  Xuất 3 định dạng: Interactive (.xlsx cho iSpring), Review (.xlsx), Moodle XML (.xml).
  Keywords: question, quiz, trắc nghiệm, câu hỏi, test, kiểm tra, moodle, ispring.
version: 1.0.0
---

# AWF Question Generator v1.0

Skill sinh câu hỏi trắc nghiệm tự động từ nội dung các bài ebook Machine Learning.

## Khi nào Skill này được kích hoạt?

- User gọi `/question`
- User yêu cầu tạo câu hỏi, quiz, trắc nghiệm cho bài học
- User đề cập keywords: question, quiz, trắc nghiệm, câu hỏi, test, kiểm tra

---

## Quy trình tổng quan

```
📖 READ → 🧠 EXTRACT → ✏️ GENERATE → 📦 EXPORT → ✅ VERIFY
```

---

## Phase 1: READ — Đọc nội dung bài ebook

### 1.1. Xác định bài cần sinh câu hỏi

Từ lệnh `/question bai_XX`, xác định file ebook tương ứng:

```
ebooks/chapter_01_nen_tang/bai_01_tong_quan_ml.md
ebooks/chapter_01_nen_tang/bai_02_cong_cu_moi_truong.md
ebooks/chapter_01_nen_tang/bai_03_tien_xu_ly_eda.md
ebooks/chapter_02_hoi_quy/bai_04_linear_regression_don_bien.md
ebooks/chapter_02_hoi_quy/bai_05_da_bien_polynomial.md
```

### 1.2. Đọc toàn bộ nội dung

AI PHẢI đọc **toàn bộ** file `.md` của bài trước khi bắt đầu sinh câu hỏi.

---

## Phase 2: EXTRACT — Trích xuất kiến thức

AI phân tích nội dung bài và trích xuất:

| Loại kiến thức | Ví dụ | Dùng cho mức |
|----------------|-------|--------------|
| Định nghĩa, khái niệm | "Supervised Learning là..." | Mức 1 (Biết) |
| Công thức, tham số | "MSE = 1/n Σ(ŷ-y)²" | Mức 1-2 |
| So sánh, phân biệt | "Batch vs Mini-batch GD" | Mức 2 (Hiểu) |
| Giải thích cơ chế | "Tại sao bình phương sai số?" | Mức 2 |
| API/hàm thư viện | "LinearRegression().fit()" | Mức 1-2 |
| Tình huống áp dụng | "Khi nào dùng Ridge vs Lasso?" | Mức 3 (Vận dụng) |
| Phân tích kết quả | "R² = 0.61 nghĩa là gì?" | Mức 3 |
| Lỗi thường gặp | "Không scale dữ liệu trước GD" | Mức 2-3 |

---

## Phase 3: GENERATE — Sinh câu hỏi

### ⛔ QUY TẮC NỘI DUNG — BẮT BUỘC TUYỆT ĐỐI

> **1. Nội dung câu hỏi CHỈ ĐƯỢC lấy từ bài ebook `.md` tương ứng.**
> Tuyệt đối KHÔNG sáng tác kiến thức ngoài phạm vi bài.
> KHÔNG tham khảo từ reference/ hay internet.

> **2. Câu hỏi KHÔNG ĐƯỢC nhắc đến vị trí nguồn.**
> KHÔNG viết "Theo bài 02", "Trong phần 2.1", "Như đã đề cập".
> Chỉ hỏi thuần nội dung kiến thức.

> **3. Đáp án nhiễu phải hợp lý.**
> Đáp án sai phải nghe có vẻ hợp lý (plausible distractor), không được sai lố hoặc dễ loại trừ.
> Tránh đáp án kiểu "Tất cả đều đúng" / "Không có đáp án đúng".

> **4. Ngôn ngữ: Tiếng Việt + thuật ngữ Eng.**
> Giữ nguyên thuật ngữ tiếng Anh như trong ebook (Machine Learning, Gradient Descent...).

**Ví dụ:**
- ❌ "Theo bài 01, Supervised Learning là gì?"
- ✅ "Supervised Learning sử dụng loại dữ liệu nào để huấn luyện?"

---

### 3.1. Interactive Questions (5 câu/bài)

**Mục đích:** Câu hỏi tương tác trên lớp, import vào iSpring Suite Quiz Maker.

**Quy tắc:**
- Tạo **5 câu**, xen kẽ ngẫu nhiên giữa MC và MR
- **MC (Multiple Choice):** 1 đáp án đúng + 3 nhiễu = 4 đáp án
- **MR (Multiple Response):** 3 đáp án đúng + 3 nhiễu = 6 đáp án
- Câu hỏi bao quát các khái niệm chính của bài
- Feedback: giải thích ngắn gọn tại sao đúng/sai

**Cấu trúc cột Excel (.xlsx):**

| Cột | Nội dung | Ghi chú |
|-----|----------|---------|
| A | Question Type | `MC` hoặc `MR` |
| B | Question Text | Nội dung câu hỏi |
| C | Image | Để trống |
| D | Video | Để trống |
| E | Audio | Để trống |
| F | Answer 1 | MC: `*Answer` (đúng, có dấu `*`). MR: `*Answer` (đúng) |
| G | Answer 2 | MC: Answer (nhiễu). MR: `*Answer` (đúng) |
| H | Answer 3 | MC: Answer (nhiễu). MR: `*Answer` (đúng) |
| I | Answer 4 | MC: Answer (nhiễu). MR: để trống |
| J | Answer 5 | MC: trống. MR: Answer (nhiễu) |
| K | Answer 6 | MC: trống. MR: Answer (nhiễu) |
| L | Answer 7 | MC: trống. MR: Answer (nhiễu) |
| M-O | (trống) | |
| P | Correct Feedback | Phản hồi khi đúng |
| Q | Incorrect Feedback | Phản hồi khi sai |
| R | Points | Điểm (mặc định: 10) |

**Quy tắc đánh dấu đáp án đúng:**
- MC: Chỉ Answer 1 (cột F) có dấu `*` ở đầu → `*Đáp án đúng`
- MR: Answer 1, 2, 3 (cột F, G, H) có dấu `*` ở đầu → `*Đáp án đúng`
- iSpring sẽ tự shuffle khi import, nên đáp án đúng luôn đặt ở vị trí đầu

---

### 3.2. Review Questions (50 câu/bài)

**Mục đích:** Ngân hàng câu hỏi ôn tập, phân theo mức độ Bloom's Taxonomy.

**Phân bổ:**
- **20 câu Mức 1 (Biết — Remember/Understand):** Nhớ lại khái niệm, định nghĩa, công thức
- **20 câu Mức 2 (Hiểu — Apply/Analyze):** So sánh, phân biệt, giải thích cơ chế
- **10 câu Mức 3 (Vận dụng — Evaluate/Create):** Áp dụng vào tình huống mới, phân tích kết quả

**Cấu trúc cột Excel (.xlsx):**

| Cột | Tên cột | Nội dung |
|-----|---------|----------|
| A | Question ID | `BXX-L-NN` (XX=số bài, L=mức, NN=số thứ tự) |
| B | Question | Nội dung câu hỏi |
| C | Correct Answer (A) | Đáp án đúng (**luôn ở cột C**) |
| D | Option B | Đáp án nhiễu 1 |
| E | Option C | Đáp án nhiễu 2 |
| F | Option D | Đáp án nhiễu 3 |
| G | Explanation | Giải thích ngắn tại sao đáp án đúng |

**Quy tắc Question ID:**
```
B02-1-01  → Bài 02, Mức 1, Câu 01
B02-2-15  → Bài 02, Mức 2, Câu 15
B02-3-10  → Bài 02, Mức 3, Câu 10
```

**Header row:** Row 1 chứa tên cột, dữ liệu bắt đầu từ row 2.

---

### 3.3. Moodle XML (50 câu/bài — từ Review)

**Mục đích:** Import trực tiếp vào Moodle LMS.

**Quy tắc:**
- Chỉ export **Review questions** ra XML (50 câu)
- Interactive questions KHÔNG cần XML
- Chia thành 3 categories theo mức độ

**Cấu trúc XML:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>

  <!-- Category: Mức 1 -->
  <question type="category">
    <category>
      <text>$course$/top/BXX_Ten_bai/muc_1_biet</text>
    </category>
  </question>

  <!-- Câu hỏi mức 1 -->
  <question type="multichoice">
    <name><text>BXX-1-01</text></name>
    <questiontext format="html">
      <text><![CDATA[<p class="cell">Nội dung câu hỏi</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[<p class="cell"><strong>Đáp án đúng là: </strong>A. Đáp án</p>
      <p class="cell"><strong>Vì: </strong>Giải thích</p>]]></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>ABCD</answernumbering>
    <answer fraction="100" format="html">
      <text><![CDATA[<p class="cell">Đáp án đúng</p>]]></text>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p class="cell">Đáp án nhiễu 1</p>]]></text>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p class="cell">Đáp án nhiễu 2</p>]]></text>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p class="cell">Đáp án nhiễu 3</p>]]></text>
    </answer>
  </question>

  <!-- Category: Mức 2 -->
  <question type="category">
    <category>
      <text>$course$/top/BXX_Ten_bai/muc_2_hieu</text>
    </category>
  </question>

  <!-- ... câu hỏi mức 2 ... -->

  <!-- Category: Mức 3 -->
  <question type="category">
    <category>
      <text>$course$/top/BXX_Ten_bai/muc_3_van_dung</text>
    </category>
  </question>

  <!-- ... câu hỏi mức 3 ... -->

</quiz>
```

---

## Phase 4: EXPORT — Xuất file

### 4.1. Quy tắc đặt tên file

Mỗi bài tạo 3 file, lưu trong `question/`:

```
question/
├── bai_01_tong_quan_ml_interactive.xlsx
├── bai_01_tong_quan_ml_review.xlsx
├── bai_01_tong_quan_ml_moodle.xml
├── bai_02_cong_cu_moi_truong_interactive.xlsx
├── bai_02_cong_cu_moi_truong_review.xlsx
├── bai_02_cong_cu_moi_truong_moodle.xml
└── ...
```

> Tên file lấy đúng từ tên file ebook `.md` (bỏ phần extension).

### 4.2. Công cụ xuất

- **Excel (.xlsx):** Dùng `openpyxl` để tạo file Excel
- **Moodle XML (.xml):** Dùng string formatting (không cần thư viện XML)

### 4.3. Quy trình xuất

AI PHẢI viết **Python script** để tạo file, KHÔNG tạo file thủ công:

```python
import openpyxl

# 1. Tạo Interactive Excel
wb = openpyxl.Workbook()
ws = wb.active
# Thêm header row theo đúng cấu trúc template
# Thêm 5 câu hỏi
wb.save('question/bai_XX_*_interactive.xlsx')

# 2. Tạo Review Excel
wb = openpyxl.Workbook()
ws = wb.active
# Header: Question ID | Question | Correct Answer (A) | Option B | Option C | Option D | Explanation
# Thêm 50 câu hỏi
wb.save('question/bai_XX_*_review.xlsx')

# 3. Tạo Moodle XML
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
# Thêm categories + questions
xml_content += '</quiz>'
with open('question/bai_XX_*_moodle.xml', 'w', encoding='utf-8') as f:
    f.write(xml_content)
```

---

## Phase 5: VERIFY — Kiểm tra

### Checklist tự kiểm tra (AI tự chạy)

```
NỘI DUNG
□ Tất cả câu hỏi lấy từ nội dung bài ebook?
□ Không nhắc đến vị trí nguồn ("Theo bài...", "Trong phần...")?
□ Đáp án nhiễu hợp lý, không sai lố?
□ Không trùng lặp ý giữa các câu?
□ Ngôn ngữ: Tiếng Việt + thuật ngữ Eng?

INTERACTIVE (5 câu)
□ Có cả MC và MR?
□ MC: 4 đáp án (1 đúng có dấu *, 3 nhiễu)?
□ MR: 6 đáp án (3 đúng có dấu *, 3 nhiễu)?
□ Có Correct/Incorrect Feedback?
□ Cấu trúc cột đúng template?

REVIEW (50 câu)
□ Đúng phân bổ: 20 mức 1 + 20 mức 2 + 10 mức 3?
□ Question ID đúng format BXX-L-NN?
□ Cột C luôn là đáp án đúng?
□ Có Explanation cho mỗi câu?

MOODLE XML
□ XML hợp lệ (well-formed)?
□ Có 3 categories (muc_1_biet, muc_2_hieu, muc_3_van_dung)?
□ Số câu mỗi category: 20 + 20 + 10?
□ generalfeedback có đáp án đúng + giải thích?
□ CDATA wrapping đúng?
```

### Kiểm tra kỹ thuật (AI chạy Python)

```python
# Verify Excel
import openpyxl
wb = openpyxl.load_workbook('question/bai_XX_*_review.xlsx')
ws = wb.active
assert ws.max_row == 51  # 1 header + 50 data rows

# Verify XML
import xml.etree.ElementTree as ET
tree = ET.parse('question/bai_XX_*_moodle.xml')
questions = tree.findall('.//question[@type="multichoice"]')
assert len(questions) == 50
```

---

## Chia nhỏ do Token Limit

> ⚠️ Token limit không cho phép sinh 50 câu trong 1 lần.
> AI PHẢI chia nhỏ và sinh theo từng phần:

```
Lần 1: Interactive (5 câu) → xuất file interactive.xlsx
Lần 2: Review Mức 1 (20 câu) → lưu tạm
Lần 3: Review Mức 2 (20 câu) → lưu tạm
Lần 4: Review Mức 3 (10 câu) → ghép + xuất review.xlsx + moodle.xml
```

Mỗi lần, AI viết Python script tạo file, chạy script, và verify kết quả.

---

## Tích hợp với Workflow khác

- **`/textbook`** → Viết bài xong → `/question bai_XX` để sinh câu hỏi
- **`/save-brain`** → Cập nhật features.json khi có câu hỏi mới cho bài

---

## Ví dụ sử dụng

### Sinh câu hỏi cho 1 bài
```
User: /question bai_02
AI: [Đọc bai_02_cong_cu_moi_truong.md → Trích xuất kiến thức → 
     Sinh 5 interactive + 50 review → Xuất 3 files → Verify]
```

### Sinh câu hỏi cho tất cả bài đã hoàn thành
```
User: /question all
AI: [Đọc features.json → Lọc bài status="done" → 
     Sinh câu hỏi lần lượt cho từng bài]
```
