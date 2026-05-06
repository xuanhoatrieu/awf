---
name: awf-video
description: "Tạo video animation minh họa thuật toán ML bằng Manim Community Edition, theo phong cách 3Blue1Brown. Kích hoạt bằng lệnh /video <chủ đề>. Keywords: video, animation, manim, 3b1b, gradient descent, neural network, CNN, PCA, SVM, KNN."
---

# 🎬 AWF-Video — Tạo Video Animation ML

## MỤC ĐÍCH
Tự động tạo video MP4 animation minh họa các thuật toán Machine Learning. Hỗ trợ **dual engine**:
- **ManimCE v0.20+** — CLI batch render (template tự viết)
- **ManimGL v1.7+** — 3b1b engine (code gốc từ 3b1b/videos)

## KÍCH HOẠT
- Lệnh `/video <chủ đề>` — Ví dụ: `/video Gradient Descent`
- Keywords: video, animation, manim, render, 3b1b

## HẠ TẦNG ĐÃ CÀI

| Component | Version | Path |
|-----------|---------|------|
| ManimCE | v0.20.1 | `pip install manim` | CLI batch render |
| ManimGL | v1.7.2 | `pip install manimgl` | 3b1b interactive/record |
| LaTeX | MiKTeX 25.12 | `C:\Users\xuanh\AppData\Local\Programs\MiKTeX\miktex\bin\x64` | |
| FFmpeg | 2026-04-30 | `D:\ffmpeg-2026\bin` | |
| manim-voiceover | v0.3.7 | `pip install manim-voiceover[recorder]` | |
| TTS Server | OmniVoice Studio | `http://117.0.36.6:8888` | |
| 3b1b/videos | latest | `3b1b_videos/` (shallow clone) | Source templates |

## QUY ƯỚC OUTPUT

- **Chất lượng mặc định:** 1080p/60fps (`-qh`)
- **Tỷ lệ mặc định:** 16:9 ngang (landscape)
- **Thư mục output:** `video/<tenvideo>.mp4` (flat directory, tự tạo nếu chưa có)
- **Tên file:** English snake_case (e.g., `gradient_descent_2d.mp4`)
- **Ngôn ngữ:** Giữ nguyên tiếng Anh, thêm subtitle tiếng Việt (SRT)

## QUY TRÌNH THỰC HIỆN

### Bước 1: Phân tích chủ đề
1. Đọc `<chủ đề>` từ user
2. Map vào template có sẵn trong `templates/`
3. Nếu không có template phù hợp → sinh code Manim mới

### Bước 2: Chọn hoặc sinh Scene code

**Topic → Template mapping:**
```python
TOPIC_MAP = {
    "gradient descent": ("gradient_descent.py", "GradientDescent2D"),
    "gradient descent contour": ("gradient_descent.py", "GradientDescentContour"),
    "linear regression": ("linear_regression.py", "LinearRegressionFit"),
    "neural network": ("neural_network.py", "NeuralNetworkForwardPass"),
    "activation function": ("neural_network.py", "NeuralNetworkActivation"),
    "loss landscape": ("loss_landscape.py", "LossLandscape3D"),
}
```

**Nếu không có template:** Sinh code Manim CE mới dựa trên `common_styles.py`

### Bước 3: Render video

**Sử dụng render script:**
```bash
python .agents/skills/awf-video/scripts/render_video.py \
    .agents/skills/awf-video/templates/<file>.py <SceneName> \
    --name <output_name> \
    --quality final
```

**Hoặc render trực tiếp rồi copy:**
```bash
# Render 1080p
manim -qh <scene_file>.py <SceneName>

# Copy vào video/
copy media/videos/<scene>/1080p60/<SceneName>.mp4 video/<output_name>.mp4
```

**Quality presets:**
| Flag | Resolution | Dùng khi |
|------|-----------|---------|
| `--quality preview` | 480p/15fps | Debug nhanh |
| `--quality draft` | 720p/30fps | Kiểm tra nội dung |
| `--quality final` | 1080p/60fps | **Sản phẩm cuối (mặc định)** |

### Bước 4: Trả kết quả
- Thông báo đường dẫn: `video/<tenvideo>.mp4`

## DUAL ENGINE — CHỌN ĐÚNG ENGINE

### Auto-detect (mặc định)
Script `render_video.py` tự phát hiện engine dựa trên:
- File có `from manimlib import *` → dùng **ManimGL**
- File nằm trong `3b1b_videos/` → dùng **ManimGL**
- Còn lại → dùng **ManimCE**

### Chạy thủ công
```bash
# ManimCE (template tự viết)
manim -qh templates/gradient_descent.py GradientDescent2D

# ManimGL (code 3b1b) — cần -w để write file
manimgl 3b1b_videos/_2017/nn/part1.py NetworkScene -w --hd

# Hoặc dùng render_video.py (tự detect)
python render_video.py 3b1b_videos/_2024/transformers/attention.py AttentionScene
```

### Force engine
```bash
python render_video.py scene.py MyScene --engine ce    # Force ManimCE
python render_video.py scene.py MyScene --engine 3b1b  # Force ManimGL
```

## KHO CODE 3b1b/videos

**Repo:** `3b1b_videos/` (shallow clone từ github.com/3b1b/videos)

### Source code ML quan trọng nhất:

| Source | Chủ đề | Bài ML | Scenes |
|--------|--------|--------|--------|
| `_2017/nn/part1.py` | NN Structure (146KB!) | Bài 17 | NetworkScene, LayerScene |
| `_2017/nn/part2.py` | NN Training / GD | Bài 17 | GradientScene |
| `_2017/nn/part3.py` | Backpropagation | Bài 17 | BackpropScene |
| `_2017/gradient.py` | Gradient multivariable | Bài 4-5 | GradientField |
| `_2024/transformers/attention.py` | Attention (149KB!) | Bài 17-18 | AttentionScene |
| `_2024/transformers/mlp.py` | MLP layers | Bài 17 | MLPScene |
| `_2024/transformers/ml_basics.py` | ML fundamentals | Bài 1-3 | MLBasicsScene |
| `_2024/transformers/embedding.py` | Word embeddings | Bài 17 | EmbeddingScene |
| `_2026/cross_entropy/` | Cross Entropy Loss | Bài 8 | CrossEntropyScene |
| `_2024/linalg/` | Linear Algebra | Bài 16 | EigenScene |

## TÍCH HỢP TIẾNG NÓI (TTS)

### Phương án: manim-voiceover + OmniVoice Studio

**Cấu hình giọng đọc:**
| Ngôn ngữ | Mode | Giọng | Config |
|----------|------|-------|--------|
| Tiếng Việt | Clone | ref_id=9 | `OmniVoiceService(lang="vi")` |
| Tiếng Anh | System | male/female | `OmniVoiceService(lang="en", gender="female")` |

**Cách dùng trong scene code:**
```python
from manim import *
from manim_voiceover import VoiceoverScene

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from omnivoice_service import OmniVoiceService

class MyScene(VoiceoverScene):
    def construct(self):
        # Vietnamese narration (clone voice)
        self.set_speech_service(OmniVoiceService(lang="vi"))

        with self.voiceover(text="Gradient Descent là thuật toán tối ưu...") as tracker:
            self.play(Create(axes), run_time=tracker.duration)

        # Hoặc English:
        # self.set_speech_service(OmniVoiceService(lang="en", gender="female"))
```

**File adapter:** `templates/omnivoice_service.py`

## CONVENTIONS KHI VIẾT CODE MANIM

### Import chuẩn
```python
from manim import *
import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common_styles import *
```

### Cấu trúc Scene chuẩn
```python
class GradientDescentScene(Scene):
    def construct(self):
        self.camera.background_color = C_DARK_BG

        # Phase 1: Title (2-3s)
        create_title_slide(self, "Gradient Descent", "Tìm điểm cực tiểu")

        # Phase 2: Setup (axes, labels)
        axes = Axes(...)
        self.play(Create(axes))

        # Phase 3: Main animation (15-30s)
        # ... thuật toán chính

        # Phase 4: Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])
```

### Style Guide
- Bảng màu: dùng constants từ `common_styles.py` (C_BLUE, C_RED, C_GREEN...)
- Background: `C_DARK_BG = "#1C1C2E"`
- Title: `font_size=48`, Body: `28`, Label: `24`
- Dùng `MathTex()` cho công thức toán, `Text()` cho text thường

## DANH SÁCH TEMPLATE CÓ SẴN

| File | Scene | Mô tả |
|------|-------|--------|
| `gradient_descent.py` | `GradientDescent2D` | GD trên hàm quadratic, tangent line, step tracking |
| `gradient_descent.py` | `GradientDescentContour` | GD trên contour plot 2 biến |
| `linear_regression.py` | `LinearRegressionFit` | Scatter → Bad line → Residuals → Best fit |
| `neural_network.py` | `NeuralNetworkForwardPass` | NN [3,5,4,2] forward pass |
| `neural_network.py` | `NeuralNetworkActivation` | So sánh Sigmoid, ReLU, Tanh |
| `loss_landscape.py` | `LossLandscape3D` | 3D surface + GD path + camera xoay |
| `common_styles.py` | — | Shared colors, fonts, utilities |
| `omnivoice_service.py` | — | Custom TTS adapter |

## LƯU Ý KỸ THUẬT

1. **Paths**: LUÔN dùng `pathlib.Path`, KHÔNG dùng string concat
2. **Render speed**: Mặc định `-qh` (1080p). Dùng `-ql` chỉ khi debug
3. **LaTeX**: Đã cài MiKTeX → dùng `MathTex()` thoải mái
4. **TTS Server**: Cần server OmniVoice đang chạy tại `http://117.0.36.6:8888`
5. **FFmpeg**: Đã cài tại `D:\ffmpeg-2026\bin`
6. **Font**: LUÔN dùng `font=DEFAULT_FONT` (Times New Roman) cho `Text()` → hỗ trợ tiếng Việt
7. **Dual engine**: File dùng `manimlib` → chạy bằng `manimgl`, file dùng `manim` → chạy bằng `manim`
8. **3b1b code**: Không sửa trực tiếp file trong `3b1b_videos/`. Copy ra template mới rồi chỉnh
9. **Subtitle**: Giữ nguyên text tiếng Anh trong video, tạo file `.srt` tiếng Việt đi kèm
10. **Video tiếng Việt**: Dùng TTS clone voice (ref_id=9) qua `OmniVoiceService(lang="vi")`
