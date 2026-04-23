# /textbook — Viết Textbook/Ebook

## Kích hoạt Skill
Đọc file `.agents/skills/awf-textbook/SKILL.md` để nắm toàn bộ quy trình.

## Cách gọi

### Viết bài cụ thể
```
User: /textbook viết bài 4
→ AI đọc _meta.json → tìm bài 4 → viết theo SKILL.md → update progress
```

### Viết bài tiếp theo
```
User: /textbook viết bài tiếp
→ AI đọc _meta.json → tìm bài đầu tiên có status "not_started" → viết
```

### Xem tiến độ
```
User: /textbook tiến độ
→ AI đọc ebooks/progress.md → hiển thị bảng
```

## Bước 1: Thu thập thông tin
Hỏi user (nếu chưa có):
1. **Chủ đề** sách?
2. **Đối tượng** đọc giả?
3. **Outline** / kế hoạch có sẵn? (file path hoặc mô tả)
4. **Ngôn ngữ** viết? (vi/en)
5. **Ngôn ngữ lập trình** nếu có? (Python, JS...)
6. **Thư mục lưu?** (mặc định: `./ebooks/`)

## Bước 2: Tạo khung sườn (Scaffold)
// turbo
1. Tạo thư mục `ebooks/` với cấu trúc chapter/bài theo outline
2. Tạo `_meta.json` tổng
3. Tạo `_chapter_meta.json` cho mỗi chapter
4. Tạo `README.md` mục lục
5. Tạo `progress.md` bảng tiến độ

## Bước 3: Viết nội dung
Với mỗi bài (section):
1. Đọc `_meta.json` → xác định bài cần viết
2. Đọc `_chapter_meta.json` → lấy learning outcomes
3. Đọc outline + context bài trước (nếu có)
4. Xác định Learning Outcomes + Assessments TRƯỚC (Backward Design)
5. Viết theo template chuẩn trong SKILL.md
6. Tự review theo Anti-AI Checklist
7. Lưu file + update `_chapter_meta.json` (status, word_count)
8. Update `progress.md`
9. Gửi user review

## Bước 4: Review & Chỉnh sửa
1. User đọc và feedback
2. AI chỉnh sửa theo feedback
3. Update status → "completed" khi user approve
4. Lặp lại đến khi user hài lòng

## Bước 5: Export (khi cần)
1. User chọn format: PDF / DOCX / Website
2. AI tạo script export phù hợp
3. Chạy export

## Post-Workflow: Auto-Save
Sau khi hoàn thành:
1. Update progress.md
2. Update _meta.json → status
3. Nếu có decisions/gotchas mới → ghi lại
