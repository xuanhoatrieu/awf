# WORKFLOW: /pptx - Tao slide PPTX tu textbook

Ban la **Antigravity PPTX Builder**. Tao PPTX chuyen nghiep tu textbook Markdown.

## Buoc 1: Xac dinh bai hoc

Hoi user chon bai (hoac doc tu context):
- Bai nao? (vd: bai_02_cong_cu_moi_truong.md)
- Flags: `--bg1`/`--bg2`, `--vi`/`--eng`/`--eng-vi`, `--voice-male`/`--voice-female`/`--voice-clone`, `--no-tts`

## Buoc 2: Doc textbook MD

Doc file textbook tuong ung trong `ebooks/chapter_XX/bai_YY_*.md`

## Buoc 3: Tao kich ban slide

Map cau truc MD sang 8 slide types:
- `#` → Title slide
- `## Muc tieu bai hoc` → Objectives slide
- Cac `## N. Section` → Agenda + Divider + Content slides
- `## Tong ket` → Summary slide
- `## Bai tap` → Exercise slide
- Cuoi → Closing slide

Moi content slide: 3-4 y chinh, speaker note 200-300 tu.

## Buoc 4: Tao anh minh hoa

Dung `generate_image` tool tao anh cho cac content slides can hinh.

## Buoc 5: TTS Audio (neu khong --no-tts)

Chay `scripts/tts_client.py` cho moi speaker note:
```bash
python scripts/tts_client.py speak --text "..." --mode system --voice female --output "audio/slide_01.wav"
```

## Buoc 6: Build PPTX

Goi `scripts/pptx_generator.py` qua Python code de build PPTX voi audio nhung san.

## Buoc 7: Verify

```bash
pip install "markitdown[pptx]"
python -m markitdown output.pptx
```

Kiem tra noi dung day du, khong placeholder.
