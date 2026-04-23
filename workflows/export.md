# /export — Export ebook ra DOCX

## Cách sử dụng

### Export 1 bài cụ thể
```
User: /export bai_01
→ AI chạy: python ebooks/export.py bai_01
→ Output: ebooks/chapter_01_nen_tang/bai_01_tong_quan_ml.docx
```

### Export toàn bộ 1 chapter
```
User: /export chapter_01
→ AI chạy: python ebooks/export.py chapter_01
→ Output: ebooks/chapter_01_nen_tang/chapter_01_nen_tang.docx (gộp tất cả bài)
```

### Export toàn bộ ebook
```
User: /export all
→ AI chạy: python ebooks/export.py all
→ Output: ebooks/Nhap_Mon_Hoc_May.docx
```

## Cấu hình DOCX
Template: `ebooks/_reference.docx`
- **Trang:** A4 (21 x 29.7 cm)
- **Margins:** top/bottom/right 2cm, left 3cm
- **Font:** Times New Roman 13pt
- **Alignment:** Justify (căn đều 2 bên)
- **Code blocks:** Consolas 11pt, left-aligned

## Thực hiện
// turbo
1. Refresh PATH: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`
2. Chạy: `python ebooks/export.py <target>`
3. Thông báo kết quả cho user

## Yêu cầu
- Pandoc đã cài (`winget install JohnMacFarlane.Pandoc`)
- python-docx đã cài (`pip install python-docx`)
