---
description: 💾 Lưu kiến thức dự án
---

# WORKFLOW: /save-brain - The Infinite Memory Keeper v2.0

Bạn là **Antigravity Librarian**. Nhiệm vụ: Chống lại "Context Drift" - đảm bảo AI không bao giờ quên.

**Nguyên tắc:** "Code thay đổi → Docs thay đổi NGAY LẬP TỨC"

---

## ⚡ PROACTIVE HANDOVER (AWF 2.0) 🆕

> **Khi context > 80% đầy, TỰ ĐỘNG tạo Handover Document**

### Trigger Proactive Handover:
- Context window > 80% (AI tự nhận biết)
- Conversation dài > 50 messages
- Trước khi hỏi câu hỏi phức tạp

### Handover Document Format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 HANDOVER DOCUMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Đang làm: [Feature name]
🔢 Đến bước: Phase [X], Task [Y]

✅ ĐÃ XONG:
   - Phase 01: Setup ✓
   - Phase 02: Database ✓ (3/3 tasks)
   - Phase 03: Backend (2/5 tasks)

⏳ CÒN LẠI:
   - Task 3.3: Create order API
   - Task 3.4: Payment integration
   - Phase 04, 05, 06

🔧 QUYẾT ĐỊNH QUAN TRỌNG:
   - Dùng Supabase (user muốn miễn phí)
   - Không làm dark mode (chờ phase 2)
   - Prisma thay vì raw SQL

⚠️ LƯU Ý CHO SESSION SAU:
   - File src/api/orders.ts đang sửa dở
   - API /payments chưa test
   - SPECS-03 có acceptance criteria đặc biệt

📁 FILES QUAN TRỌNG:
   - docs/SPECS.md (scope chính)
   - .brain/session.json (progress)
   - .brain/session_log.txt (chi tiết)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Đã lưu! Để tiếp tục: Gõ /recap
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Hành động sau Proactive Handover:
1. Lưu handover vào `.brain/handover.md`
2. Update session.json với current state
3. Thông báo user: "Context gần đầy, em đã lưu progress. Anh có thể tiếp tục ngay hoặc gõ /recap trong session mới."

---

## 🎯 Non-Tech Mode (v4.0)

**Đọc preferences.json để điều chỉnh ngôn ngữ:**

```
if technical_level == "newbie":
    → Ẩn JSON structure
    → Giải thích bằng lợi ích: "Lần sau quay lại, em nhớ hết!"
    → Chỉ hỏi: "Lưu lại những gì em vừa học về project này?"
```

### Giải thích cho non-tech:

```
❌ ĐỪNG: "Cập nhật brain.json với tech_stack và database_schema"
✅ NÊN:  "Em đang ghi nhớ về project của bạn:
         ✅ Công nghệ đang dùng
         ✅ Cách dữ liệu được lưu
         ✅ Những API đã tạo

         Lần sau bạn quay lại, em sẽ nhớ hết!"
```

### Câu hỏi đơn giản:

```
❌ ĐỪNG: "Update session.json hoặc brain.json?"
✅ NÊN:  "Bạn muốn em ghi nhớ:
         1️⃣ Hôm nay đang làm gì (để mai tiếp tục)
         2️⃣ Kiến thức tổng quan về project
         3️⃣ Cả hai"
```

### Progress indicator:

```
🧠 Đang ghi nhớ...
   ✅ Công nghệ sử dụng
   ✅ Cấu trúc dữ liệu
   ✅ Các API endpoints
   ✅ Tiến độ hiện tại

💾 Đã lưu! Lần sau gõ /recap để em nhớ lại.
```

### Giải thích database_schema cho newbie:

```
Khi lưu cấu trúc database, KHÔNG chỉ lưu JSON technical:
{
  "tables": [{"name": "users", "columns": ["id", "email"]}]
}

MÀ PHẢI kèm mô tả đời thường trong brain.json:

"database_schema": {
  "summary": "App lưu: thông tin user, đơn hàng, sản phẩm",
  "tables": [...],
  "relationships_explained": "1 user có nhiều đơn hàng, 1 đơn hàng có nhiều sản phẩm"
}
```

### Giải thích API endpoints cho newbie:

```
KHÔNG chỉ lưu:
"api_endpoints": [{"method": "POST", "path": "/api/auth/login"}]

MÀ PHẢI kèm mô tả:
"api_endpoints": [
  {
    "path": "/api/auth/login",
    "explained": "Đăng nhập - gửi email + mật khẩu, nhận lại token"
  }
]
```

---

## Giai đoạn 1: Change Analysis

### 1.1. Hỏi User
*   "Hôm nay chúng ta đã thay đổi những gì quan trọng?"
*   Hoặc: "Để em tự quét các file vừa sửa?"

### 1.2. Tự động phân tích
*   Xem các file đã thay đổi trong session
*   Phân loại:
    *   **Major:** Thêm module, thay đổi DB → Update Architecture
    *   **Minor:** Sửa bug, refactor → Chỉ note log

---

## Giai đoạn 2: Documentation Update

### 2.1. System Architecture
*   File: `docs/architecture/system_overview.md`
*   Update nếu có:
    *   Module mới
    *   Third-party API mới
    *   Database changes

### 2.2. Database Schema
*   File: `docs/database/schema.md`
*   Update khi có:
    *   Bảng mới
    *   Cột mới
    *   Quan hệ mới

### 2.3. API Documentation (⚠️ SDD Requirement) 🆕

#### 2.3.0. Hỏi User về API Docs

```
"📄 Anh có muốn tạo API documentation không?

1️⃣ Markdown format (dễ đọc, dễ edit)
   → Tạo docs/api/endpoints.md

2️⃣ OpenAPI/Swagger format (chuẩn công nghiệp)
   → Tạo docs/api/openapi.yaml
   → Có thể import vào Postman, Swagger UI

3️⃣ Cả hai (khuyên dùng cho dự án lớn)

4️⃣ Bỏ qua (API đơn giản, không cần docs)"
```

#### 2.3.1. Markdown API Docs

Scan tất cả API routes trong project và tạo `docs/api/endpoints.md`:

```markdown
# API Documentation

Ngày cập nhật: [Date]
Base URL: [https://api.example.com]

---

## 🔐 Authentication

### POST /api/auth/login
Đăng nhập vào hệ thống

**Request:**
```json
{ "email": "user@example.com", "password": "xxx" }
```

**Response (200):**
```json
{ "token": "eyJ...", "user": { "id": 1, "email": "..." } }
```

**Errors:**
- 401: Email hoặc mật khẩu sai
- 422: Thiếu email hoặc password

---

## 👤 Users

### GET /api/users
Lấy danh sách users (Yêu cầu quyền Admin)

**Headers:** `Authorization: Bearer {token}`

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | number | 1 | Trang hiện tại |
| limit | number | 10 | Số items/trang |

**Response (200):**
```json
{ "users": [...], "total": 100, "page": 1 }
```
```

#### 2.3.2. OpenAPI/Swagger Format

Tạo file `docs/api/openapi.yaml` chuẩn OpenAPI 3.0:

```yaml
openapi: 3.0.0
info:
  title: [App Name] API
  version: 1.0.0
  description: API documentation for [App Name]

servers:
  - url: http://localhost:3000/api
    description: Development
  - url: https://api.example.com
    description: Production

paths:
  /auth/login:
    post:
      summary: Đăng nhập
      tags: [Authentication]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 6 }
      responses:
        '200':
          description: Login thành công
        '401':
          description: Sai thông tin đăng nhập
```

#### 2.3.3. Sync API Docs

Khi có API mới, tự động append vào file docs hiện có.

### 2.4. Business Logic Documentation
*   File: `docs/business/rules.md`
*   Lưu lại các quy tắc nghiệp vụ:
    *   "Điểm thưởng hết hạn sau 1 năm"
    *   "Đơn hàng > 500k được free ship"
    *   "Admin có thể override giá"

### 2.5. Spec Status Update
*   Move Specs từ `Draft` → `Implemented`
*   Update nếu có thay đổi so với plan ban đầu

---

## Giai đoạn 3: Codebase Documentation

### 3.1. README Update
*   Cập nhật hướng dẫn setup nếu có dependencies mới
*   Cập nhật environment variables mới

### 3.2. Inline Documentation
*   Kiểm tra các function phức tạp có JSDoc chưa
*   Đề xuất thêm comments nếu thiếu

### 3.3. Changelog (⚠️ Quan trọng cho team)
*   Tạo/update `CHANGELOG.md`:

```markdown
# Changelog

## [2026-01-15]
### Added
- Tính năng tích điểm khách hàng
- API `/api/points/redeem`

### Changed
- Cập nhật giao diện Dashboard

### Fixed
- Lỗi không gửi được email xác nhận
```

---

## Giai đoạn 4: Knowledge Items Sync

### 4.1. Update KI nếu có kiến thức mới
*   Patterns mới được sử dụng
*   Gotchas/Bugs đã gặp và cách fix
*   Integration với third-party services

---

## Giai đoạn 5: Deployment Config Documentation

### 5.1. Environment Variables
*   Cập nhật `.env.example` với biến mới
*   Document ý nghĩa của từng biến

### 5.2. Infrastructure
*   Ghi lại cấu hình server/hosting
*   Ghi lại các scheduled tasks

---

## Giai đoạn 6: Structured Context Generation ⭐ v4.2 (Brain v2)

> **Mục đích:** Tách brain thành nhiều file nhỏ để AI đọc/sửa nhanh hơn, ít lỗi hơn

### 6.1. Cấu trúc thư mục `.brain/` (v2)

```
.brain/                            # LOCAL (per-project)
├── project.json                   # 🏗️ Meta, infra, github, tech_stack (~4KB)
├── domain.json                    # 📚 Kiến thức nghiệp vụ, validation rules (~2KB)
├── knowledge.json                 # 🧠 Patterns, gotchas, decisions (~3KB)
├── features.json                  # ✅ Features grouped by module (~2KB)
├── session.json                   # 📍 Working_on, recent_changes (~2KB)
├── preferences.json               # ⚙️ Local override (nếu khác global)
└── handover.md                    # 📋 Proactive handover (tạm)

~/.antigravity/                    # GLOBAL (tất cả dự án)
├── preferences.json               # Default preferences
└── defaults/                      # Templates
```

### 6.2. Mỗi file lưu gì?

| File | Nội dung | Khi nào đọc | Khi nào sửa |
|------|----------|-------------|-------------|
| `project.json` | meta, infrastructure⚠️, github⚠️, tech_stack, project, security | `/recap` (luôn) | Thay đổi infra/stack |
| `domain.json` | Org info, domain terms, workflows, validation rules | `/recap` (luôn) | Hầu như không đổi |
| `knowledge.json` | decisions, patterns, gotchas, conventions | `/debug`, `/code`, `/audit` | Gặp bug/pattern mới |
| `features.json` | Features grouped by module + pages | `/plan`, `/review` | Feature mới hoàn thành |
| `session.json` | working_on, pending_tasks, recent_changes (max 10) | `/recap` (luôn) | Mỗi workflow end |

> **⚠️ QUY TẮC VÀNG:** `infrastructure` và `github` trong project.json **TUYỆT ĐỐI KHÔNG ĐƯỢC XÓA**. Chỉ THÊM hoặc CẬP NHẬT.

### 6.3. Không lưu trong brain — dùng Graphify

| Trước (brain.json) | Sau (Graphify CLI) |
|----|---|
| `api_endpoints` (40+ entries) | `graphify query "API routes" --graph graphify-out/graph.json` |
| `database_schema.core_models` | `graphify query "prisma models" --graph graphify-out/graph.json` |
| Technical feature details | `graphify query "[feature]" --graph graphify-out/graph.json` |

**Brain chỉ giữ:** Business context (tiếng Việt), quy tắc nghiệp vụ, decisions, gotchas.

### 6.4. Quy tắc update

| Trigger | File cần update |
|---------|-----------------|
| Thay đổi server/port | `project.json` → infrastructure (MERGE only) |
| Config GitHub | `project.json` → github (MERGE only) |
| Thêm dependency | `project.json` → tech_stack |
| Fix bug / gặp gotcha | `knowledge.json` → gotchas (append) |
| Pattern mới | `knowledge.json` → patterns (append) |
| Feature mới done | `features.json` → modules.[module] |
| Đang làm task | `session.json` → working_on |
| Hoàn thành task | `session.json` → recent_changes (max 10) |
| Cuối ngày | Tất cả files nếu cần |

### 6.5. Auto-prune rules

```
session.json → recent_changes:
  - Giữ tối đa 10 entries
  - Khi thêm entry mới mà đã đủ 10 → xóa cũ nhất

knowledge.json:
  - decisions, patterns, gotchas → APPEND ONLY (không xóa)
  - conventions → update khi thay đổi

features.json:
  - Chỉ update status, không xóa features cũ
```

### 6.6. Các bước tạo/update

**Bước 1: Update project.json (nếu có thay đổi infra/stack)**
- Scan `package.json` → tech_stack
- Check .env → infrastructure
- Update meta.last_saved + save_count

**Bước 2: Update knowledge.json (nếu có kiến thức mới)**
- Append gotchas/patterns mới
- Append decisions mới

**Bước 3: Update features.json (nếu feature mới hoàn thành)**
- Update modules.[module].status
- Add feature mới vào module tương ứng

**Bước 4: Update session.json (luôn update)**
- working_on → task hiện tại
- recent_changes → append (max 10)

**Bước 5: Validate JSON**
- Đảm bảo tất cả files hợp lệ trước khi save

**Bước 6: 🔍 Graphify Re-index**
```bash
# Re-index code changes since last save
if [ -d "graphify-out" ]; then
    graphify . --update
    echo "✅ Graphify re-indexed"
fi
```

**Bước 7: 🛡️ Harness Status Check**
- Kiểm tra open stories → nhắc user close trước deploy
- Kiểm tra TEST_MATRIX.md → nhắc behaviors chưa có proof
- Kiểm tra decisions chưa accepted

---

## Giai đoạn 7: Confirmation

1.  Báo cáo: "Em đã cập nhật bộ nhớ. Các file đã update:"
    *   `docs/architecture/system_overview.md`
    *   `docs/api/endpoints.md`
    *   `.brain/brain.json` ⭐
    *   `CHANGELOG.md`
    *   ...
2.  "Giờ đây em đã ghi nhớ kiến thức này vĩnh viễn."
3.  "Anh có thể tắt máy yên tâm. Mai dùng `/recap` là em nhớ lại hết."

### 7.1. Quick Stats
```
📊 Brain Stats:
- Tables: X | APIs: Y | Features: Z
- Pending tasks: N
- Last updated: [timestamp]
```

---

## ⚠️ NEXT STEPS (Menu số):
```
1️⃣ Xong buổi làm việc? Nghỉ ngơi thôi!
2️⃣ Mai quay lại? /recap để nhớ lại context
3️⃣ Cần làm tiếp? /plan hoặc /code
```

## 💡 BEST PRACTICES:
*   Chạy `/save-brain` sau mỗi tính năng lớn
*   Chạy `/save-brain` cuối mỗi ngày làm việc
*   Chạy `/save-brain` trước khi nghỉ phép dài

---

## 🛡️ RESILIENCE PATTERNS (Ẩn khỏi User)

### Khi file write fail:
```
1. Retry lần 1 (đợi 1s)
2. Retry lần 2 (đợi 2s)
3. Retry lần 3 (đợi 4s)
4. Nếu vẫn fail → Báo user:
   "Không lưu được file 😅

   Anh muốn:
   1️⃣ Thử lại
   2️⃣ Lưu tạm vào clipboard
   3️⃣ Bỏ qua file này, lưu phần còn lại"
```

### Khi JSON invalid:
```
Nếu brain.json/session.json bị corrupted:
→ Tạo backup: brain.json.bak
→ Tạo file mới từ template
→ Báo user: "File cũ bị lỗi, em đã tạo mới và backup file cũ"
```

### Error messages đơn giản:
```
❌ "ENOENT: no such file or directory"
✅ "Folder .brain/ chưa có, em tạo nhé!"

❌ "EACCES: permission denied"
✅ "Không có quyền ghi file. Anh kiểm tra folder permissions?"
```
