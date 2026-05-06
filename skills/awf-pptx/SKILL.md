---
name: awf-pptx
description: "Tao slide PPTX tu textbook Markdown. Chuyen doi noi dung bai hoc thanh bo san pham: kich ban slide + anh minh hoa + audio TTS + file PPTX (da nhung audio auto-play). Keywords: pptx, slide, presentation, powerpoint, bai giang."
---

# AWF-PPTX Skill

Chuyển đổi textbook Markdown thành PPTX chuyên nghiệp với audio TTS nhúng sẵn.

## Pipeline 6 bước

```
1. READ textbook.md
2. SCRIPT: AI tạo JSON script (8 slide types + speaker notes + image)
3. IMAGE: Lấy ảnh từ textbook assets/ + generate_image cho slides chưa có
4. TTS: Chạy tts_client.py tạo audio từ speaker notes (TRƯỚC PPTX)
5. BUILD: Chạy pptx_generator.py build PPTX (nhúng audio + ảnh sẵn)
6. QA: markitdown verify
```

## Cấu trúc 8 Slide Types

| Type | Map từ MD | Mô tả |
|------|-----------|-------|
| [A] Title | `# Tiêu đề` | bg1: 1.png, bg2: primary color |
| [B] Objectives | `## Mục tiêu` | Danh sách learning outcomes |
| [C] Agenda | Các `##` sections | Danh sách sections |
| [D] Divider | Mỗi `## N.` | Số lớn + tên section |
| [E] Content | Nội dung | 3-4 ý/slide, **BẮT BUỘC** có image |
| [F] Summary | `## Tổng kết` | Key takeaways |
| [G] Exercise | `## Bài tập` | Danh sách bài tập |
| [H] Closing | Cuối bài | bg1: 2.png, bg2: primary color |

## Flags khi user gọi /pptx

### Ngôn ngữ
- `--vi` (mặc định): Slide + speaker note = Tiếng Việt
- `--eng`: Slide + speaker note = Tiếng Anh
- `--eng-vi`: Slide = Eng, speaker note = Việt

### Design mode
- `--bg1` (mặc định): Ảnh nền 1.png (title) + 2.png (content + closing)
- `--bg2`: Programmatic design, Palette #10 giáo dục

### Voice (cho TTS)
- `--voice-female` (mặc định): Giọng nữ Ngoc
- `--voice-male`: Giọng nam Binh
- `--voice-clone`: Clone voice của user (ref UUID, model omni)
- `--no-tts`: Bỏ qua TTS, không nhúng audio

### SEA-G2P Normalize
- Mặc định: BẬT (on)
- `--no-sea-g2p`: Tắt normalize

---

## Chi tiết từng bước

### Bước 2: SCRIPT — AI tạo JSON

**QUY TẮC QUAN TRỌNG:**

1. **Speaker notes PHẢI chi tiết**: 300-500 từ/slide (không phải 100-200). Notes phải explain đầy đủ nội dung slide, đưa ví dụ minh họa, giải thích tại sao. Đây là script giảng viên đọc, không phải tóm tắt.

2. **Image cho MỌI content slide**:
   - Kiểm tra thư mục `ebooks/chapter_XX/assets/baiNN_*.png` để lấy ảnh đã có từ textbook
   - Các slide KHÔNG có ảnh sẵn → tạo `image_prompt` để generate_image
   - bg1: Slide 2 trở đi đều phải có image (bên phải slide)
   - bg2: TẤT CẢ slides đều phải có image

3. **JSON format**: Mỗi slide PHẢI có đủ các trường:

```json
{
  "type": "content",
  "title": "Slide title",
  "bullets": ["Point 1", "Point 2"],
  "image": "path/to/existing/image.png",
  "image_prompt": "prompt nếu cần generate",
  "note": "Speaker note 300-500 từ, chi tiết, giải thích rõ ràng..."
}
```

### Bước 3: IMAGE — Tạo ảnh minh họa

**THỨ TỰ ƯU TIÊN:**
1. Dùng ảnh từ textbook `ebooks/chapter_XX/assets/baiNN_*.png` nếu có
2. Dùng `generate_image` tool tạo ảnh mới cho các slide chưa có
3. Lưu vào `pptx/output/bai_XX/images/`
4. Cập nhật `"image": "absolute/path"` trong JSON

### Bước 4: TTS — Tạo audio

**Clone voice (model omni):**
```bash
python .agents/skills/awf-pptx/scripts/tts_client.py speak \
  --text "Speaker note tiếng Việt" \
  --mode clone \
  --output pptx/output/bai_XX/audio/slide_01.wav
```

**System voice (nữ):**
```bash
python .agents/skills/awf-pptx/scripts/tts_client.py speak \
  --text "Speaker note" \
  --mode system --voice female \
  --output pptx/output/bai_XX/audio/slide_01.wav
```

**Tắt SEA-G2P:**
```bash
--no-normalize
```

**LƯU Ý:**
- Clone voice có retry 3 lần với backoff (2s, 4s, 8s)
- Nếu server busy, thêm delay 2-3s giữa các slide

### Bước 5: BUILD — Tạo PPTX

```python
from pptx_generator import build_from_script

build_from_script(
    script_path="pptx/output/bai_XX/slide_script.json",
    output_path="pptx/output/bai_XX/bai_XX.pptx",
    mode="bg1",
    bg_dir="pptx/temp_background",
    audio_dir="pptx/output/bai_XX/audio",
)
```

### Bước 6: QA — Verify

```bash
python -m markitdown pptx/output/bai_XX/bai_XX.pptx
```

Kiểm tra:
- Đủ 8 slide types
- Không placeholder/empty
- Speaker notes đầy đủ (300-500 từ)
- Audio embedded (file size > vài MB)
- Images hiển thị đúng vị trí

## Anti-AI Slop Rules

- KHÔNG gradient → solid colors
- KHÔNG emoji làm icon
- KHÔNG accent line dưới title
- KHÔNG lặp layout → rotate content subtypes
- Body text KHÔNG bold → bold chỉ cho headings
- Speaker notes: văn phong học thuật, 300-500 từ/slide

## Cấu trúc thư mục output

```
pptx/output/bai_XX/
  slide_script.json     # Kịch bản
  images/               # Ảnh minh họa
    slide_05.png
    slide_08.png
  audio/                # TTS audio
    slide_01.wav
    slide_02.wav
    ...
  bai_XX.pptx           # File PPTX cuối cùng
```
