---
description: Shared gates cho mọi workflow có code change. IMPORT file này thay vì duplicate logic.
---

# Shared Gates — Graphify & Harness Integration

> **File này được IMPORT bởi:** `/code`, `/debug`, `/refactor`, `/deploy`, `/save_brain`
> **KHÔNG BAO GIỜ bỏ qua các gates này khi dự án có `graphify-out/` hoặc `docs/FEATURE_INTAKE.md`.**

---

## Gate 1: 🔍 Graphify — Pre-Code Context

**Khi nào:** TRƯỚC KHI viết/sửa code
**Điều kiện:** `graphify-out/` tồn tại trong project root

```bash
# 1. Kiểm tra graphify đã cài chưa
if ! command -v graphify &> /dev/null; then
    pip install graphifyy
fi

# 2. Kiểm tra đã index chưa
if [ ! -d "graphify-out" ]; then
    graphify .   # Index lần đầu
fi

# 3. Query context liên quan đến task hiện tại
graphify query "[module/function liên quan]" --graph graphify-out/graph.json

# 4. Nếu sửa function cụ thể — check blast radius
graphify explain "[function cần sửa]"
```

**Mục đích:**
- Hiểu incoming/outgoing relationships trước khi code
- Tránh tạo code trùng lặp với logic có sẵn
- Biết blast radius của thay đổi

---

## Gate 2: 🛡️ Harness — Risk Classification

**Khi nào:** TRƯỚC KHI viết/sửa code (sau Gate 1)
**Điều kiện:** `docs/FEATURE_INTAKE.md` tồn tại trong project

### Bước 1: Classify input type
- New spec / Spec slice / Change request / Maintenance / Harness improvement

### Bước 2: Run risk checklist
| Risk flag | Applies when touching |
|-----------|----------------------|
| Auth | login, logout, sessions, JWT, password, refresh token |
| Authorization | roles, permissions, tenant scope |
| Data model | schema, migrations, uniqueness, deletion |
| Audit/security | audit logs, privacy, sensitive data |
| External systems | email, payments, cloud services, provider SDKs, queues |
| Public contracts | API shape, response envelope, client-visible behavior |
| Cross-platform | desktop/mobile/browser split |
| Existing behavior | already implemented behavior changes |
| Weak proof | unclear or missing tests around affected area |
| Multi-domain | more than one product domain changes at once |

### Bước 3: Choose lane
```
0-1 flags → tiny (patch directly, no story needed)
2-3 flags → normal (create story file docs/stories/US-XXX.md)
4+ flags or hard gate → high-risk (create story folder + ask user confirm)
```

**Hard gates (auto high-risk):** Auth, Authorization, Data loss, Audit/security, External provider

### Bước 4: Create artifacts (nếu normal+)
```bash
# Story file
cp docs/templates/story.md docs/stories/US-XXX-short-title.md

# Decision record (nếu architecture change)
cp docs/templates/decision.md docs/decisions/DR-XXXX-short-title.md
```

### Bước 5: Display to user
```
🛡️ HARNESS INTAKE:
   Lane: normal
   Risk: Data model, Public contracts
   Story: docs/stories/US-011-feature-name.md
   → Tiếp tục code...
```

---

## Gate 3: 🔍 Graphify — Post-Code Re-index

**Khi nào:** SAU KHI code xong (mỗi phase hoặc mỗi task lớn)

```bash
graphify . --update   # Re-index changed files (SHA256 cache, fast)
```

---

## Gate 4: 🛡️ Harness — Post-Code Close

**Khi nào:** SAU KHI code + test xong (mỗi phase)
**Điều kiện:** Đã tạo story file ở Gate 2

1. **Update story status** → `done` trong story file
2. **Update TEST_MATRIX.md** nếu thêm/sửa test:
   ```markdown
   | Behavior | Proof | Status |
   |----------|-------|--------|
   | Feature X CRUD | Manual API test | ✅ |
   ```
3. **Update decision record** → status = `accepted` (nếu đã tạo)

---

## Phase Checkpoint (dùng cho `/code all`)

SAU MỖI PHASE trong `/code all`, BẮT BUỘC chạy tuần tự:

```
1. Gate 3: graphify . --update          (re-index code)
2. Gate 4: Close story/update TEST_MATRIX (nếu có)  
3. Commit: git add . && git commit -m "phase-XX: description"
4. Update session.json: current_phase → next phase
5. Log: "✅ Phase XX done. Graphify + Harness saved. → Phase YY..."
```

**Mục đích:** Nếu agent bị ngắt giữa chừng (quota, timeout, crash), phase trước đã được lưu hoàn chỉnh — session sau chỉ cần `/recap` là tiếp tục từ phase tiếp theo.
