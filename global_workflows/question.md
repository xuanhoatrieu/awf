---
description: ❓ Sinh câu hỏi trắc nghiệm từ bài ebook
---

# WORKFLOW: /question - Question Generator

Bạn là **Antigravity Question Writer**. Nhiệm vụ: đọc bài ebook ML và sinh câu hỏi trắc nghiệm chất lượng cao.

---

## Cách gọi

```
/question bai_02          → Sinh 3 file câu hỏi cho Bài 02
/question bai_01 bai_03   → Sinh cho nhiều bài
/question all             → Sinh cho tất cả bài đã hoàn thành
/question bai_02 review   → Chỉ sinh Review (50 câu)
/question bai_02 interactive → Chỉ sinh Interactive (5 câu)
```

---

## Quy trình

### Bước 1: Load Skill

```
Đọc: .agents/skills/awf-question-gen/SKILL.md
→ Nắm toàn bộ quy tắc, cấu trúc, checklist
```

### Bước 2: Xác định bài cần sinh

```
Nếu "bai_XX":
  → Tìm file: ebooks/chapter_*/bai_XX_*.md
  → Kiểm tra file tồn tại

Nếu "all":
  → Đọc .brain/features.json
  → Lọc sections có status="done"
  → Sinh lần lượt cho từng bài
```

### Bước 3: Đọc nội dung bài

```
→ view_file toàn bộ file .md
→ Trích xuất kiến thức theo bảng phân loại trong SKILL.md
```

### Bước 4: Sinh câu hỏi (chia nhỏ do token limit)

```
Lần 1: Sinh 5 câu Interactive (MC/MR)
  → Viết Python script tạo .xlsx
  → Chạy script
  → Verify file

Lần 2: Sinh 20 câu Review Mức 1 (Biết)
  → Viết Python script (append hoặc tạo mới)
  → Chạy

Lần 3: Sinh 20 câu Review Mức 2 (Hiểu)
  → Tiếp tục

Lần 4: Sinh 10 câu Review Mức 3 (Vận dụng)
  → Ghép tất cả → xuất review.xlsx + moodle.xml
  → Verify
```

### Bước 5: Verify

```
→ Chạy Python verify: đếm số dòng Excel, parse XML
→ Tự kiểm tra theo checklist trong SKILL.md
→ Báo cáo kết quả cho user
```

---

## Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ĐÃ TẠO CÂU HỎI CHO: Bài XX — [Tên bài]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Files:
   + question/bai_XX_*_interactive.xlsx (5 câu MC/MR)
   + question/bai_XX_*_review.xlsx (50 câu, 3 mức)
   + question/bai_XX_*_moodle.xml (50 câu, Moodle import)

📊 Phân bổ Review:
   Mức 1 (Biết): 20 câu
   Mức 2 (Hiểu): 20 câu
   Mức 3 (Vận dụng): 10 câu
```

---

## ⚠️ NEXT STEPS:
```
1️⃣ Review nội dung câu hỏi? Mở file Excel
2️⃣ Sinh câu hỏi bài khác? /question bai_XX
3️⃣ Import vào Moodle? Upload file .xml
4️⃣ Import vào iSpring? Mở file interactive.xlsx
```
