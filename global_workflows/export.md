---
name: export
description: "📄 Xuất bài học hoặc đề cương ra định dạng DOCX"
---

# Quy trình Export ra DOCX

Workflow này giúp tự động hóa quá trình chuyển đổi file Markdown thành định dạng DOCX chuyên nghiệp.

Có **2 loại export** khác nhau:

| Loại | Script | Template | Đặc điểm |
|---|---|---|---|
| **Bài giảng (Textbook)** | `ebooks/export.py` | `_reference.docx` | Code block có viền, nền xám |
| **Đề cương học phần** | `ebooks/export_decuong.py` | `_reference_decuong.docx` | Font Times New Roman, Mục 7-8 xoay ngang (Landscape) |

## 1. Yêu cầu hệ thống
- Đã cài đặt **Pandoc** (kiểm tra bằng lệnh `pandoc --version`).
- Môi trường Python có thư viện `python-docx` (kiểm tra bằng `pip show python-docx`).

## 2. Cách sử dụng

Người dùng có thể gọi lệnh `/export` kèm theo tên mục tiêu. Ví dụ:

### Export bài giảng (Textbook)
- `/export bai_01`: Xuất Bài 01 ra file DOCX.
- `/export bai_03`: Xuất Bài 03 ra file DOCX.
- `/export chapter_01`: Xuất toàn bộ Chapter 01 (gộp các bài lại).
- `/export all`: Xuất toàn bộ giáo trình.

### Export đề cương học phần
- `/export de_cuong`: Xuất file Đề cương Nhập môn Học máy ra DOCX.
- `/export đề cương`: Tương tự (AI nhận diện tiếng Việt).

## 3. Các bước thực hiện (Dành cho AI)

Khi người dùng gọi lệnh `/export <target>`, AI cần thực hiện các bước sau:

1. **Xác định loại export**:
   - Nếu `<target>` chứa "de_cuong", "đề cương", "decuong", "syllabus" → dùng **export_decuong.py**
   - Nếu `<target>` chứa "bai_", số, "chapter_", "all" → dùng **export.py**

2. **Kiểm tra trạng thái file**: 
   - Nếu file DOCX đích đã tồn tại và đang mở/bị khóa (thường do Google Drive hoặc MS Word), việc ghi đè trực tiếp sẽ thất bại.
   - Cả 2 script đều xuất ra file `.tmp` trước, sau đó rename. Nếu bị khóa, quá trình rename sẽ thất bại.

3. **Chạy kịch bản xuất**:
   - **Bài giảng**: `$env:PATH += ";$env:LOCALAPPDATA\Pandoc"; & "$env:USERPROFILE\miniconda3\python.exe" ebooks/export.py <target>`
   - **Đề cương**: `$env:PATH += ";$env:LOCALAPPDATA\Pandoc"; & "$env:USERPROFILE\miniconda3\python.exe" ebooks/export_decuong.py`
   - Thư mục làm việc (`Cwd`): Gốc của dự án (`g:\My Drive\1Work\BoMon_Tin\6_Deep_learning`).

4. **Xử lý kết quả**:
   - Nếu thành công: Báo cáo dung lượng file và vị trí file DOCX vừa tạo.
   - Nếu bị lỗi khóa file (Lock): Báo cáo người dùng, chủ động copy file `.tmp` thành `<tên_file>_v2.docx` hoặc hướng dẫn người dùng đóng MS Word.
