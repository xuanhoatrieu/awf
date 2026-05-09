# 🚀 AWF - Antigravity Workflow Framework v4.2

> **Forked & customized** by [xuanhoatrieu](https://github.com/xuanhoatrieu)
> Original by [TUAN130294](https://github.com/TUAN130294/awf)

AWF biến AI coding agent thành đồng nghiệp chuyên nghiệp — biết lên kế hoạch, phân loại rủi ro, viết code, test, deploy, và ghi lại mọi quyết định.

## ✨ What's New in v4.2

| Feature | Mô tả |
|---------|--------|
| **27 Workflow Commands** | `/init` → `/deploy` + `/textbook`, `/pptx`, `/question`, `/video` |
| **11 Auto-trigger Skills** | Graphify, session-restore, auto-save, textbook, PPTX+TTS, video... |
| **Graphify Intelligence** | Knowledge graph cho codebase (25 ngôn ngữ, AST-based, multimodal) |
| **Harness Integration** | Feature intake, risk classification, story templates, decision records |
| **Persistent Brain** | `brain.json` giữ infra/github data vĩnh viễn |
| **Git Safety** | Luôn hỏi trước khi commit/push |

---

## 📦 Cài đặt

### 🍎 Mac / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/xuanhoatrieu/awf/main/install.sh | bash
```

### 🪟 Windows (PowerShell)

```powershell
iex "& { $(irm https://raw.githubusercontent.com/xuanhoatrieu/awf/main/install.ps1) }"
```

### Cài Harness vào dự án (tùy chọn)

Harness thêm tài liệu quản lý dự án **per-project** — giúp agent phân loại rủi ro, tạo story, ghi decision records.

```bash
# Cài vào dự án mới (clean)
curl -fsSL "https://raw.githubusercontent.com/hoangnb24/harness-experimental/main/scripts/install-harness.sh?$(date +%s)" | bash -s -- --yes

# Cài vào dự án đã có (merge, giữ file cũ)
curl -fsSL "https://raw.githubusercontent.com/hoangnb24/harness-experimental/main/scripts/install-harness.sh?$(date +%s)" | bash -s -- --merge --yes
```

### Sau khi cài:

```
~/.gemini/                          ← AWF (global, mọi dự án)
├── GEMINI.md                       ← Global rules
├── awf_version                     ← 4.2.0
└── antigravity/
    ├── global_workflows/           ← 27 workflow .md files
    └── skills/                     ← 11 skills + scripts

your-project/                       ← Harness (per-project)
├── docs/
│   ├── FEATURE_INTAKE.md           ← Risk classification
│   ├── HARNESS.md                  ← Human-agent collaboration
│   ├── TEST_MATRIX.md              ← Behavior → proof
│   ├── stories/                    ← Story packets
│   ├── decisions/                  ← Architecture decisions
│   └── templates/                  ← Reusable templates
└── .brain/brain.json               ← AWF persistent data
```

---

## 🎮 Workflow Commands

### Planning & Design
| Command | Chức năng |
|---------|-----------|
| `/init` | Khởi tạo dự án mới + brain.json |
| `/plan` | Lên kế hoạch tính năng (+ Harness risk classification) |
| `/design` | Thiết kế kỹ thuật (DB, API, Flow) |
| `/visualize` | Thiết kế UI/UX mockup |
| `/brainstorm` | Nghiên cứu & brainstorm ý tưởng |

### Development
| Command | Chức năng |
|---------|-----------|
| `/code` | Viết code theo spec (+ Graphify context lookup) |
| `/run` | Chạy ứng dụng |
| `/debug` | Sửa lỗi (+ Graphify call chain tracing) |
| `/test` | Kiểm thử (+ Harness TEST_MATRIX update) |
| `/refactor` | Tái cấu trúc (+ Graphify blast radius analysis) |

### Review & Deploy
| Command | Chức năng |
|---------|-----------|
| `/review` | Review & bàn giao dự án |
| `/audit` | Kiểm tra bảo mật (+ Graphify dead code detection) |
| `/deploy` | Deploy production |
| `/rollback` | Quay lại phiên bản cũ |

### Knowledge Management
| Command | Chức năng |
|---------|-----------|
| `/save-brain` | Lưu kiến thức (+ infra, GitHub rules) |
| `/recap` | Khôi phục context (+ Graphify, infra) |
| `/next` | Gợi ý bước tiếp theo |
| `/help` | Trợ giúp & hướng dẫn |
| `/customize` | Cá nhân hóa trải nghiệm |

### Content Creation
| Command | Chức năng |
|---------|-----------|
| `/textbook` | Viết ebook/textbook (Backward Design) |
| `/pptx` | Tạo slide PPTX + TTS audio |
| `/question` | Sinh câu hỏi trắc nghiệm (iSpring, Moodle) |
| `/video` | Tạo video animation ML (Manim) |
| `/export` | Xuất bài học ra DOCX |

---

## 🔍 Graphify Code Intelligence

Graphify xây dựng knowledge graph cho toàn bộ codebase — giúp agent hiểu cấu trúc dự án ở mức symbol (function, class, import, call chain).

```bash
# Cài Graphify
pip install graphifyy

# Index dự án
cd your-project && graphify update .

# Xem report
cat graphify-out/GRAPH_REPORT.md
```

**Auto-activates trong:** `/recap`, `/refactor`, `/debug`, `/review`, `/audit`, `/code`

| Khả năng | Command |
|----------|---------|
| Impact analysis | `graphify query "function_name"` |
| Call chain tracing | `graphify path "SymbolA" "SymbolB"` |
| Symbol explanation | `graphify explain "ClassName"` |
| Codebase overview | Đọc `GRAPH_REPORT.md` (god nodes, communities) |

---

## 🏗️ Harness Integration

Harness cung cấp quy trình quản lý dự án theo chuẩn [Harness Engineering](https://openai.com/index/harness-engineering/):

### Feature Intake Flow

```
Yêu cầu của anh
    ↓
Phân loại input (spec / change / maintenance)
    ↓
Risk checklist (auth, data, external systems...)
    ↓
Chọn lane: Tiny → Normal → High-risk
    ↓
Tạo story + validation expectations
    ↓
Code theo AWF workflow
```

### Risk Lanes

| Lane | Khi nào | Yêu cầu |
|------|---------|---------|
| **Tiny** | Sửa nhỏ, ít rủi ro | Patch trực tiếp |
| **Normal** | Story-sized, bounded | Story file + validation + test matrix |
| **High-risk** | Auth, data, security | Story folder (4 files) + human confirmation |

---

## 🧩 Skills (Auto-trigger)

| Skill | Trigger | Chức năng |
|-------|---------|-----------|
| awf-graphify | `/recap`, `/refactor`, `/debug`, `/review`, `/audit`, `/code` | Knowledge graph intelligence |
| awf-session-restore | Đầu session | Context restore |
| awf-auto-save | Workflow end | Auto-save progress |
| awf-adaptive-language | Đầu session | Điều chỉnh ngôn ngữ theo level |
| awf-error-translator | Khi có lỗi | Dịch lỗi kỹ thuật |
| awf-onboarding | `/init` lần đầu | Hướng dẫn user mới |
| awf-context-help | `/help` | Smart help |
| awf-textbook | `/textbook` | Ebook/textbook writing |
| awf-question-gen | `/question` | Quiz generation (iSpring, Moodle) |
| awf-pptx | `/pptx` | PPTX slide + TTS audio |
| awf-video | `/video` | ML animation (Manim) |

---

## 🧠 Persistent Brain

`/save-brain` lưu và **KHÔNG BAO GIỜ xóa:**
- **Server info**: IP, port, SSH user, OS
- **Database**: type, host, port, name, user
- **Services**: dev server, MCP servers
- **GitHub rules**: repo URL, commit/push rules (always ask first)

---

## 📁 Repo Structure

```
awf/
├── README.md               # Tài liệu này
├── install.sh              # Linux/Mac installer
├── install.ps1             # Windows installer
├── workflows/              # 27 workflow .md files
│   ├── plan.md
│   ├── code.md
│   ├── ...
│   └── video.md
├── skills/                 # 11 auto-trigger skills
│   ├── awf-graphify/
│   ├── awf-pptx/
│   │   ├── SKILL.md
│   │   └── scripts/       # pptx_generator.py, tts_client.py...
│   ├── awf-video/
│   │   ├── SKILL.md
│   │   ├── scripts/       # render_video.py, scan_3b1b.py
│   │   └── templates/     # Manim scene templates
│   └── ...
├── pptx/                   # PPTX template resources
└── index.html              # Landing page
```

---

## 🔄 AWF + Harness: Cách kết hợp

| Anh gõ | AWF làm gì | Harness làm gì |
|--------|------------|----------------|
| `/plan` | Lên plan kỹ thuật + Graphify | Phân loại risk + tạo story |
| `/code` | Code + Graphify context | Kiểm tra acceptance criteria |
| `/test` | Chạy test suite | Update TEST_MATRIX.md |
| `/review` | Review code quality | Kiểm tra story done, decision log |
| `/save-brain` | Lưu brain.json | Cập nhật story status |

**Anh không cần thay đổi cách làm việc** — vẫn gõ `/command` bình thường. Harness chỉ thêm tài liệu trong dự án để agent thông minh hơn.

---

## 📝 License

MIT — Fork freely, customize as needed.
