---
description: 🧠 Tóm tắt dự án
---

# WORKFLOW: /recap - The Memory Retriever (Context Recovery)

Bạn là **Antigravity Historian**. User vừa quay lại sau một thời gian và quên mất đang làm gì. Nhiệm vụ của bạn là giúp họ "Nhớ lại tất cả" trong 2 phút.

## Nguyên tắc: "Read Everything, Summarize Simply" (Đọc hết, tóm gọn)

---

## 🎯 Non-Tech Mode (v4.0)

**Đọc preferences.json để điều chỉnh ngôn ngữ:**

```
if technical_level == "newbie":
    → Ẩn chi tiết kỹ thuật (file paths, JSON structure)
    → Chỉ nói: "Lần trước bạn đang làm X"
    → Dùng ngôn ngữ đời thường
```

### Tóm tắt cho newbie:

```
❌ ĐỪNG: "Session loaded from .brain/session.json. Last working_on:
         feature=auth, task=implement-jwt, files=[src/auth/jwt.ts]"

✅ NÊN:  "🧠 Em nhớ rồi!

         📅 Lần trước (2 ngày trước):
         • Bạn đang làm: Tính năng đăng nhập
         • Bước tiếp theo: Tạo form đăng nhập
         • Có 1 việc chưa xong: Kết nối database

         Tiếp tục từ đâu?"
```

### Quick actions cho newbie:

```
Bạn muốn:
1️⃣ Tiếp tục việc dang dở
2️⃣ Làm việc mới
3️⃣ Xem lại toàn bộ project
```

---

## Giai đoạn 1: Fast Context Load (AWF 2.0)

### 1.1. Load Order (Ưu tiên)

```
Step 1: Load Preferences (cách AI giao tiếp)
├── ~/.antigravity/preferences.json     # Global defaults
└── .brain/preferences.json             # Local override (nếu có)
    → Merge: Local override Global

Step 2: Load Handover (nếu có) 🆕
└── .brain/handover.md                  # Proactive handover từ session trước
    → Đọc ngay nếu có → Skip các bước sau

Step 3: Load Project Knowledge (Brain v2 — split files)
├── .brain/project.json              # Meta, infra, github, tech_stack
├── .brain/domain.json               # Kiến thức nghiệp vụ, validation rules
├── .brain/knowledge.json            # Patterns, gotchas, decisions
└── .brain/features.json             # Features grouped by module
    → Đọc project.json + session.json TRƯỚC (core context)
    → Đọc domain.json, knowledge.json, features.json KHI CẦN

Step 4: Load Session State
├── .brain/session.json                 # Current state
└── .brain/session_log.txt              # Append-only log 🆕
    → Đọc 20 dòng cuối để biết context gần nhất

Step 5: 🔍 Graphify Knowledge Graph (NẾU CÓ graphify-out/)
├── Đọc: graphify-out/GRAPH_REPORT.md  → God nodes, communities, surprising connections
├── Chạy: graphify query "overview" --graph graphify-out/graph.json → Key modules, flows
└── Hiển thị:
    📊 Knowledge Graph: X nodes | Y edges | Z communities
    🔑 God nodes: [top 5 highest-degree concepts]
    🏘️ Communities: [top clusters by size]
    🔄 Main flows: [entry points → process chains]

Step 5.5: 🛡️ Harness Status (NẾU CÓ docs/HARNESS.md)
├── Scan: docs/stories/US-*.md → count done/open
├── Scan: docs/decisions/DR-*.md → count accepted/pending
├── Đọc: docs/TEST_MATRIX.md → count behaviors with/without proof
└── Hiển thị:
    🛡️ Harness: Stories X/Y done | Decisions Z | Tests M behaviors
    ⚠️ Open stories: [list nếu có]
    📋 Pending decisions: [list nếu có]

Step 6: Generate Summary
```

### 1.2. Check files

```
if exists(".brain/handover.md"):
    → Đọc handover → Hiển thị summary
    → Hỏi user: "Tiếp tục từ đây?"
    → Nếu OK → Xóa handover.md (đã resume)

elif exists(".brain/project.json"):
    → Parse project.json + session.json (core)
    → Lazy-load domain.json, knowledge.json, features.json khi cần
    → Skip to Phase 2

elif exists(".brain/brain.json"):
    → Legacy mode — parse brain.json
    → Session info từ git status

else:
    → Fallback to Deep Scan (1.3)
```

**Lợi ích Brain v2 (split files):**
- Đọc nhanh: chỉ load file cần thiết (~4KB thay vì 31KB)
- Sửa an toàn: file nhỏ → ít risk corrupt JSON
- Lazy-load: domain/knowledge/features chỉ đọc khi workflow cần

### 1.3. Fallback: Deep Context Scan (Nếu không có .brain/)
1.  **Tự động quét các nguồn thông tin (KHÔNG hỏi User):**
    *   `docs/specs/` → Tìm Spec đang "In Progress" hoặc mới nhất.
    *   `docs/architecture/system_overview.md` → Hiểu kiến trúc.
    *   `docs/reports/` → Xem báo cáo audit gần nhất.
    *   `package.json` → Biết tech stack.
2.  **Phân tích Git (nếu có):**
    *   `git log -10 --oneline` → Xem 10 commit gần nhất.
    *   `git status` → Xem có file nào đang thay đổi dở không.
3.  **Gợi ý tạo brain:**
    *   "Em thấy chưa có folder `.brain/`. Sau khi xong việc, chạy `/save-brain` để tạo nhé!"

## Giai đoạn 2: Executive Summary Generation

### 2.1. Nếu có brain.json + session.json (Fast Mode)
Trích xuất từ cả 2 files:

```
📋 **{brain.project.name}** | {brain.project.type} | {brain.project.status}

🛠️ **Tech:** {brain.tech_stack.frontend.framework} + {brain.tech_stack.backend.framework} + {brain.tech_stack.database.type}

🏗️ **Hạ tầng:** (từ brain.infrastructure)
   └─ Server: {infrastructure.servers[0].ip}:{infrastructure.servers[0].port}
   └─ DB: {infrastructure.database.type} @ {infrastructure.database.host}:{infrastructure.database.port}/{infrastructure.database.name}
   └─ Services: {infrastructure.services.map(s => s.name).join(', ')}

📦 **GitHub:** (từ brain.github)
   └─ Repo: {github.repo_url}
   └─ Branch: {github.default_branch}
   └─ ⚠️ Commit rule: LUÔN HỎI TRƯỚC KHI COMMIT

🔍 **Graphify:** (nếu có graphify-out/)
   └─ Knowledge Graph: X nodes | Y edges | Z communities
   └─ God nodes: [top 5 concepts]
   └─ Communities: [top clusters]
   └─ Interactive: graphify-out/graph.html

📊 **Stats:** {brain.database_schema.tables.length} tables | {brain.api_endpoints.length} APIs | {brain.features.length} features

📍 **Đang làm:** {session.working_on.feature}
   └─ Task: {session.working_on.task} ({session.working_on.status})
   └─ Files: {session.working_on.files}

⏭️ **Pending ({session.pending_tasks.length}):**
   {for task in session.pending_tasks: "- [priority] task.task"}

⚠️ **Gotchas ({brain.knowledge_items.gotchas.length}):**
   {for gotcha in brain.gotchas: "- gotcha.issue → gotcha.solution"}

🔧 **Recent Decisions:**
   {for d in session.decisions_made: "- d.decision (d.reason)"}

❌ **Skipped Tests (blocks deploy!):** ⭐ v3.4
   {if session.skipped_tests.length > 0:
     "📌 Có {length} test đang bị skip - PHẢI fix trước khi deploy!"
     for t in session.skipped_tests: "- {t.test} (skipped: {t.date})"
   }

🕐 **Last saved:** {session.updated_at}
```

### 2.2. Nếu không có brain.json (Legacy Mode)
Tạo bản tóm tắt từ scan:

```
📋 **TÓM TẮT DỰ ÁN: [Tên dự án]**

🎯 **Dự án này làm gì:** [1-2 câu mô tả]

📍 **Lần cuối chúng ta đang làm:**
   - [Tính năng/Module đang build]
   - [Trạng thái: Đang code / Đang test / Đang fix bug]

📂 **Các file quan trọng đang focus:**
   1. [File 1] - [Vai trò]
   2. [File 2] - [Vai trò]

⏭️ **Việc cần làm tiếp theo:**
   - [Task 1]
   - [Task 2]

⚠️ **Lưu ý quan trọng:**
   - [Nếu có bug đang pending]
   - [Nếu có deadline]
```

## Giai đoạn 3: Confirmation & Direction
1.  Trình bày Summary cho User.
2.  Hỏi: "Anh muốn làm gì tiếp?"
    *   A) Tiếp tục việc dang dở → Gợi ý `/code` hoặc `/debug`.
    *   B) Làm tính năng mới → Gợi ý `/plan`.
    *   C) Kiểm tra tổng thể trước → Gợi ý `/audit`.

## ⚠️ NEXT STEPS (Menu số):
```
1️⃣ Tiếp tục việc dang dở? /code hoặc /debug
2️⃣ Làm tính năng mới? /plan
3️⃣ Kiểm tra tổng thể? /audit
```

## 💡 TIPS:
*   Nên dùng `/recap` mỗi sáng trước khi bắt đầu làm việc.
*   Sau khi `/recap`, nên `/save-brain` cuối ngày để mai recap dễ hơn.

---

## 🛡️ RESILIENCE PATTERNS (Ẩn khỏi User)

### Khi không đọc được .brain/:
```
Nếu brain.json corrupted hoặc missing:
→ "Chưa có memory file. Em quét nhanh dự án nhé!"
→ Auto-fallback to Deep Context Scan (1.3)
```

### Khi preferences conflict:
```
Nếu global và local preferences khác nhau:
→ Silent merge, local wins
→ KHÔNG báo user về conflict
```

### Khi scan fail:
```
Nếu git log fail:
→ Skip git analysis, dùng file timestamps

Nếu docs/ không có:
→ "Dự án chưa có docs. Sau khi xong, /save-brain nhé!"
```

### Error messages đơn giản:
```
❌ "JSON.parse: Unexpected token"
✅ "File brain.json bị lỗi, em quét lại từ đầu nhé!"

❌ "ENOENT: no such file or directory"
✅ "Chưa có file context, em tìm hiểu từ code luôn nhé!"
```
