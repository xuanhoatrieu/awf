---
description: "🎬 Tạo video animation ML bằng Manim"
---

# 🎬 /video — Tạo Video Animation ML

## Kích hoạt
```
/video <chủ đề>
```

## Quy trình

### Bước 1: Đọc Skill
// turbo
Đọc file SKILL.md để lấy hướng dẫn chi tiết.
```
view_file .agents/skills/awf-video/SKILL.md
```

### Bước 2: Phân tích chủ đề
Xác định chủ đề từ input user và map vào template có sẵn:

| Keyword | Template |
|---------|----------|
| gradient descent | `gradient_descent.py` |
| linear regression | `linear_regression.py` |
| neural network | `neural_network.py` |
| loss, landscape | `loss_landscape.py` |

Nếu không có template phù hợp → sinh code Manim mới dựa trên `common_styles.py`.

### Bước 3: Render video
```bash
# Medium quality (mặc định, nhanh)
manim -qm <template_file>.py <SceneName>

# High quality (khi user yêu cầu "-qh" hoặc "high quality")
manim -qh <template_file>.py <SceneName>
```

### Bước 4: Trả kết quả
- Thông báo đường dẫn video cho user
- Video nằm tại: `media/videos/<file>/720p30/` hoặc `1080p60/`

## Lưu ý
- Luôn `cd` vào thư mục chứa file template trước khi render
- Dùng `-qm` để preview, `-qh` cho sản phẩm cuối
- Nếu LaTeX lỗi → dùng `Text()` thay `MathTex()`
