---
description: ⛔ Shared Gates cho Graphify + Harness (BẮT BUỘC cho /code, /refactor, /debug, /audit)
---

# Shared Gates — Graphify + Harness

> **File này là BẮT BUỘC.** Mọi workflow có tag `⚠️ IMPORT: _shared_gates.md` PHẢI đọc và tuân thủ.

---

## ⛔ GATE 1: Graphify Context (TRƯỚC KHI CODE)

> **Khi nào:** Trước khi viết/sửa bất kỳ file nào trong `/code`, `/refactor`, `/debug`

### Hard Checklist (PHẢI tick hết):

```
□ 1. Kiểm tra graphify-out/ tồn tại
     Nếu KHÔNG → chạy: graphify update .
     Nếu CÓ    → đọc GRAPH_REPORT.md cho overview

□ 2. Query context liên quan
     graphify query "[module/function liên quan]" --graph graphify-out/graph.json

□ 3. Nếu SỬA function/class đã có:
     graphify explain "[function cần sửa]"
     → Đọc blast radius trước khi code

□ 4. Log kết quả cho user:
     "🔍 Graphify: [X] nodes liên quan, blast radius: [Y] files"
```

### Bypass Rule:
- **Tiny task** (thêm comment, sửa typo, CSS-only): Có thể skip Gate 1
- **Mọi task khác**: KHÔNG ĐƯỢC skip

---

## ⛔ GATE 2: Harness Intake (TRƯỚC KHI CODE)

> **Khi nào:** Khi project có `docs/FEATURE_INTAKE.md` hoặc `docs/HARNESS.md`

### Hard Checklist (PHẢI tick hết):

```
□ 1. Classify input type:
     New spec | Spec slice | Change request | Maintenance | Harness improvement

□ 2. Run risk checklist (đếm flags):
     □ Auth?           □ Authorization?      □ Data model?
     □ Audit/security? □ External systems?   □ Public contracts?
     □ Cross-platform? □ Existing behavior?  □ Weak proof?
     □ Multi-domain?

□ 3. Choose lane:
     0-1 flags → tiny  (code trực tiếp)
     2-3 flags → normal (tạo story file)
     4+ flags  → high-risk (tạo story folder + hỏi user)

□ 4. Tạo artifacts (nếu normal+):
     □ Story:    cp docs/templates/story.md → docs/stories/US-XXX-title.md
     □ Decision: cp docs/templates/decision.md → docs/decisions/DR-XXXX-title.md (nếu architecture change)

□ 5. Log cho user:
     "🛡️ HARNESS: Lane=[lane], Flags=[N], Story=[path]"
```

### Bypass Rule:
- **Dự án KHÔNG có** `docs/FEATURE_INTAKE.md`: Skip Gate 2 hoàn toàn
- **Tiny lane**: Không cần story/decision file

---

## ⛔ GATE 3: Phase Checkpoint (SAU MỖI PHASE)

> **Khi nào:** Sau khi hoàn thành mỗi phase trong `/code`, `/code all`, `/code all-phases`

### Hard Checklist (PHẢI tick hết, KHÔNG ĐƯỢC skip):

```
□ 1. graphify update .                          # Re-index code mới
□ 2. Update story status (nếu có story file)    # planned → in_progress → done
□ 3. Update docs/TEST_MATRIX.md (nếu có)        # Thêm behaviors mới
□ 4. Update decision record (nếu có)            # planned → accepted
□ 5. git add . && git commit -m "phase-XX"      # Checkpoint commit
□ 6. Update .brain/session.json                 # current_phase → next
```

### Đặc biệt cho `/code all`:
- Checkpoint chạy **TỰ ĐỘNG** sau mỗi phase, KHÔNG CẦN confirm
- Nếu graphify fail → log warning, KHÔNG dừng pipeline
- Nếu git commit fail → log warning, tiếp tục

---

## ⛔ GATE 4: Save Gate (SAU KHI HOÀN TẤT)

> **Khi nào:** Khi `/save-brain` hoặc cuối `/code all`

### Hard Checklist:

```
□ 1. graphify update .                    # Final re-index
□ 2. Kiểm tra open stories               # Nhắc user close
□ 3. Kiểm tra TEST_MATRIX.md             # Nhắc behaviors chưa có proof
□ 4. Kiểm tra decisions chưa accepted    # Nhắc user
□ 5. Update .brain/ files                 # brain.json, session.json, handover.md
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│  AWF GATE SEQUENCE                              │
│                                                 │
│  /code [task]                                   │
│    ├── ⛔ Gate 1: Graphify Context               │
│    ├── ⛔ Gate 2: Harness Intake                  │
│    ├── 💻 Code phase                             │
│    ├── ⛔ Gate 3: Phase Checkpoint                │
│    │     ├── graphify update .                   │
│    │     ├── Update story/TEST_MATRIX            │
│    │     └── git commit checkpoint               │
│    ├── 💻 Next phase...                          │
│    ├── ⛔ Gate 3: Phase Checkpoint                │
│    └── ⛔ Gate 4: Save Gate (if /save-brain)      │
│                                                 │
│  BYPASS: tiny task = skip Gate 1+2               │
│  BYPASS: no FEATURE_INTAKE.md = skip Gate 2      │
└─────────────────────────────────────────────────┘
```

---

## Graphify CLI Quick Reference (v2.x)

```bash
# Index lần đầu hoặc re-index
graphify update .

# Query context
graphify query "search term" --graph graphify-out/graph.json

# Explain symbol
graphify explain "ClassName"

# Shortest path
graphify path "A" "B"

# Watch mode (auto rebuild)
graphify watch .
```

> **⚠️ KHÔNG dùng** `graphify .` hay `graphify . --update` — syntax cũ đã bị xóa.
