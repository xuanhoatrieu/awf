---
description: Khởi tạo dự án mới
---

# WORKFLOW: /init - Khởi Tạo Dự Án

**Vai trò:** Project Initializer
**Mục tiêu:** Capture ý tưởng, tạo workspace cơ bản, và cài Harness (quản lý dự án). KHÔNG install packages, KHÔNG setup database.

**NGÔN NGỮ: Luôn trả lời bằng tiếng Việt.**

---

## Flow Position

```
[/init] ← BẠN ĐANG Ở ĐÂY
   ↓
/brainstorm (nếu chưa rõ ý tưởng)
   ↓
/plan (lên kế hoạch features)
   ↓
/design (thiết kế kỹ thuật)
   ↓
/code (viết code)
```

---

## Stage 1: Capture Vision (HỎI NGẮN GỌN)

### 1.1. Tên dự án
"Tên dự án là gì? (VD: my-coffee-app)"

### 1.2. Mô tả 1 câu
"Mô tả ngắn gọn app làm gì? (1-2 câu)"

### 1.3. Vị trí
"Tạo ở thư mục hiện tại hay chỗ khác?"

**XONG. Không hỏi thêm.**

---

## Stage 2: Tạo Workspace + Harness

Tạo cấu trúc folder đầy đủ (AWF + Harness):

```
{project-name}/
├── .brain/
│   └── brain.json              # Project context
├── docs/
│   ├── ideas.md                # Ghi ý tưởng
│   ├── FEATURE_INTAKE.md       # Harness: risk classification
│   ├── HARNESS.md              # Harness: collaboration model
│   ├── ARCHITECTURE.md         # Harness: architecture rules
│   ├── TEST_MATRIX.md          # Harness: behavior → proof
│   ├── GLOSSARY.md             # Harness: project glossary
│   ├── HARNESS_BACKLOG.md      # Harness: improvement proposals
│   ├── product/
│   │   └── README.md           # Product contracts
│   ├── stories/
│   │   ├── README.md           # Story packets
│   │   └── backlog.md          # Story backlog
│   ├── decisions/
│   │   └── README.md           # Architecture decisions
│   └── templates/
│       ├── story.md            # Story template
│       ├── decision.md         # Decision template
│       ├── spec-intake.md      # Spec intake template
│       ├── validation-report.md
│       └── high-risk-story/    # High-risk 4-file template
│           ├── overview.md
│           ├── design.md
│           ├── execplan.md
│           └── validation.md
├── scripts/
│   └── README.md               # Project scripts
└── README.md                   # Tên + mô tả
```

### 2.1 Cách lấy Harness template files

Harness templates được tải về cùng AWF khi cài đặt.
Copy từ `~/.gemini/antigravity/harness/docs/` vào `{project}/docs/`.

**Agent PHẢI chạy:**
```bash
HARNESS_SRC="$HOME/.gemini/antigravity/harness/docs"
PROJECT_DIR="{project-path}"

if [ -d "$HARNESS_SRC" ]; then
    # Copy Harness docs, skip existing files
    cp -rn "$HARNESS_SRC"/* "$PROJECT_DIR/docs/" 2>/dev/null || true
    echo "✅ Harness templates installed from local cache"
else
    echo "⚠️ Harness templates not found locally"
    echo "💡 Re-install AWF: curl -fsSL https://raw.githubusercontent.com/xuanhoatrieu/awf/main/install.sh | bash"
fi
```

Nếu `~/.gemini/antigravity/harness/` không tồn tại, agent tạo thủ công các file Harness cốt lõi:
- `docs/FEATURE_INTAKE.md` (copy nội dung từ knowledge)
- `docs/HARNESS.md`
- `docs/TEST_MATRIX.md`
- `docs/templates/story.md`
- `docs/templates/decision.md`

### brain.json template:
```json
{
  "project": {
    "name": "{project-name}",
    "description": "{mô tả}",
    "created_at": "{timestamp}"
  },
  "tech_stack": [],
  "features": [],
  "decisions": [],
  "infrastructure": {},
  "github": {}
}
```

### README.md template:
```markdown
# {Project Name}

{Mô tả 1 câu}

## Status: 🚧 Planning

Dự án đang trong giai đoạn lên ý tưởng.

## Project Management

Dự án sử dụng [Harness v0](docs/HARNESS.md) để quản lý:
- Risk classification: [FEATURE_INTAKE.md](docs/FEATURE_INTAKE.md)
- Test tracking: [TEST_MATRIX.md](docs/TEST_MATRIX.md)
- Stories: [docs/stories/](docs/stories/)
- Decisions: [docs/decisions/](docs/decisions/)

## Next Steps

1. Gõ `/brainstorm` để explore ý tưởng
2. Hoặc `/plan` nếu đã rõ muốn làm gì
```

---

## Stage 3: Xác nhận & Hướng dẫn

```
✅ Đã tạo workspace cho "{project-name}"!

📁 Vị trí: {path}
🏗️ Harness: Đã cài (risk classification, story templates, decision records)

🚀 BƯỚC TIẾP THEO:

Chọn 1 trong 2:

1️⃣ /brainstorm - Nếu chưa rõ muốn làm gì, cần explore ý tưởng
2️⃣ /plan - Nếu đã biết rõ features cần làm

💡 Tip: Harness sẽ tự động phân loại risk khi bạn dùng /plan hoặc /code
```

---

## QUAN TRỌNG - KHÔNG LÀM

❌ KHÔNG install packages (để /code làm)
❌ KHÔNG setup database (để /design làm)
❌ KHÔNG tạo code files (để /code làm)
❌ KHÔNG chạy npm/yarn/pnpm
❌ KHÔNG hỏi về tech stack (AI sẽ tự quyết sau)

---

## First-time User

Nếu chưa có `.brain/preferences.json`:

```
👋 Chào mừng bạn đến với AWF!

Đây là lần đầu dùng. Bạn muốn:
1️⃣ Dùng mặc định (Recommended)
2️⃣ Tùy chỉnh (/customize)
```

---

## Existing Project (Dự án đã có)

Nếu user chạy `/init` trong thư mục đã có code:

1. Tạo `.brain/brain.json` nếu chưa có
2. Cài Harness docs vào `docs/` (merge, không ghi đè file cũ)
3. Chạy `graphify update .` để index codebase
4. Thông báo:

```
✅ Đã khởi tạo AWF + Harness cho dự án hiện tại!

📁 Dự án: {path}
🏗️ Harness: Đã cài (merge mode - file cũ được giữ nguyên)
🔍 Graphify: {X} nodes indexed

Gõ /recap để xem tổng quan dự án.
```

---

## Error Handling

### Folder đã tồn tại:
```
⚠️ Folder "{name}" đã có rồi.
1️⃣ Khởi tạo AWF + Harness vào folder này (merge, không ghi đè)
2️⃣ Đổi tên khác
```

### Không có quyền tạo folder:
```
❌ Không tạo được folder. Kiểm tra quyền write nhé!
```
