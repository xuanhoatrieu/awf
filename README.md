# 🚀 AWF - Antigravity Workflow Framework v4.1

> **Forked & customized** by [xuanhoatrieu](https://github.com/xuanhoatrieu)
> Original by [TUAN130294](https://github.com/TUAN130294/awf)

## ✨ What's New in v4.1 (Custom Fork)

| Feature | v3.0 (Original) | v4.1 (This Fork) |
|---------|-----------------|-------------------|
| Workflows | 14 commands | **21 commands** (+review, brainstorm, design, help, next, customize, awf-update) |
| Skills | ❌ None | **7 auto-trigger skills** |
| GitNexus | ❌ None | **✅ Code Intelligence** (knowledge graph, impact analysis) |
| Infrastructure Data | ❌ None | **✅ Persistent** (IP, port, DB, GitHub rules) |
| Save-Brain | Basic | **✅ Merge rules** (never overwrite infra/github data) |
| Recap | Basic | **✅ Infra + GitNexus + brain.json** |
| GitHub Rules | ❌ None | **✅ Always ask before commit/push** |

## 📦 Installation

### 🍎 Mac / Linux (Terminal)
```bash
curl -fsSL https://raw.githubusercontent.com/xuanhoatrieu/awf/main/install.sh | sh
```

### 🪟 Windows (PowerShell)
```powershell
iex "& { $(irm https://raw.githubusercontent.com/xuanhoatrieu/awf/main/install.ps1) }"
```

### What gets installed:
- **21 Workflows** → `~/.gemini/antigravity/global_workflows/`
- **7 Skills** → `~/.gemini/antigravity/skills/`
- **GitNexus** → Global npm package (for codebase intelligence)
- **GEMINI.md** → Updated global rules

## 🎮 Quick Start

```
/init        → Khởi tạo dự án mới
/plan        → Lên kế hoạch tính năng
/design      → Thiết kế kỹ thuật (DB, API, Flow)
/visualize   → Thiết kế UI/UX mockup
/code        → Viết code
/run         → Chạy ứng dụng
/test        → Kiểm thử
/debug       → Sửa lỗi
/refactor    → Tái cấu trúc code
/review      → Review & bàn giao dự án
/audit       → Kiểm tra bảo mật
/deploy      → Deploy production
/save-brain  → Lưu kiến thức (+ infra, GitHub rules)
/recap       → Khôi phục context (+ GitNexus, infra)
```

## 🔍 GitNexus Integration

GitNexus xây dựng knowledge graph cho codebase — auto-activates trong:
- `/recap` — overview cấu trúc dự án
- `/refactor` — blast radius analysis
- `/debug` — trace call chains
- `/review` — deep code analysis
- `/audit` — dead code + circular deps
- `/code` — context lookup trước khi code

### Index dự án:
```bash
cd your-project
npx gitnexus analyze
```

## 🧩 Skills (Auto-trigger)

| Skill | Trigger | Chức năng |
|-------|---------|-----------|
| awf-gitnexus | /recap, /refactor, /debug, /review, /audit, /code | Code Intelligence |
| awf-session-restore | Đầu session | Context restore |
| awf-auto-save | Workflow end | Auto-save progress |
| awf-adaptive-language | Đầu session | Điều chỉnh ngôn ngữ theo level |
| awf-error-translator | Khi có lỗi | Dịch lỗi kỹ thuật |
| awf-onboarding | /init lần đầu | Hướng dẫn user mới |
| awf-context-help | /help | Smart help |

## 🏗️ Persistent Infrastructure Data

`/save-brain` now saves and NEVER deletes:
- **Server info**: IP, port, SSH user, OS
- **Database**: type, host, port, name, user
- **Services**: dev server, MCP servers
- **GitHub rules**: repo URL, commit/push rules (always ask first)

## 📁 Repo Structure

```
awf/
├── workflows/          # 21 workflow .md files
├── skills/             # 7 auto-trigger skills
│   ├── awf-gitnexus/
│   ├── awf-session-restore/
│   └── ...
├── install.sh          # Linux/Mac installer
├── install.ps1         # Windows installer
└── README.md
```

## 📝 License
MIT — Fork freely, customize as needed.
