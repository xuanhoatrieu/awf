---
name: awf-gitnexus
description: Code Intelligence via GitNexus knowledge graph. Auto-activates during /refactor, /review, /debug, /audit on large projects. Provides impact analysis, process tracing, safe refactoring, and codebase overview. Uses CLI (cross-platform, no MCP config needed).
---

# AWF Skill: GitNexus Code Intelligence (CLI Mode)

## Mô tả
GitNexus xây dựng **knowledge graph** cho codebase — theo dõi mọi function, class, import, call chain, dependency. Cung cấp cho AI agent khả năng:
- **Impact Analysis** — biết function nào bị ảnh hưởng khi sửa code
- **Process Tracing** — theo dõi execution flow từ entry point
- **Safe Refactoring** — rename multi-file chính xác
- **360° Context** — xem tất cả incoming/outgoing relationships của 1 symbol

## Tại sao CLI thay vì MCP?
- **Portable:** AWF lưu trên GitHub → khi cài máy mới, CLI hoạt động ngay (chỉ cần `npx`)
- **Cross-platform:** Không phụ thuộc config MCP của từng editor/platform
- **Zero-config:** Không cần thêm settings vào Cursor/Claude/Antigravity

## Trigger
Skill này tự động kích hoạt khi:
- `/recap` — query graph overview để hiểu toàn bộ cấu trúc dự án
- `/refactor` — impact analysis trước khi refactor, safe rename
- `/review` — overview toàn bộ codebase, cluster analysis
- `/debug` — trace call chains tìm bug, context lookup
- `/audit` — kiểm tra dependencies, dead code, security surface
- `/code` — context lookup trước khi code, detect changes sau khi code

## Workflow ↔ GitNexus CLI Mapping

| Workflow | CLI Command | Mục đích |
|----------|------------|----------|
| `/recap` | `npx gitnexus status` | Hiểu tổng quan cấu trúc |
| `/refactor` | `npx gitnexus query "..."` | Blast radius + tìm dependencies |
| `/review` | `npx gitnexus query "overview"` | Phân tích code quality |
| `/debug` | `npx gitnexus query "..."` | Trace call chains |
| `/audit` | `npx gitnexus query "..."` | Dependency + security scan |
| `/code` | `npx gitnexus query "..."` | Context trước code + verify sau |

## Điều kiện
- **Dự án phải được index trước**: Chạy `npx gitnexus analyze` trong thư mục dự án
- **Node.js >= 18** (đã có trên hệ thống)
- Không cần API key (trừ wiki generation)

## Cách kiểm tra đã index chưa

```bash
# Kiểm tra trạng thái index
npx gitnexus status

# Nếu chưa index hoặc index cũ
npx gitnexus analyze
```

## Sử dụng trong Workflow (CLI Commands)

### 1. Trước khi sửa code (Impact Analysis)

Khi AI chuẩn bị sửa một function/class quan trọng:

```bash
# Chạy qua run_command tool
cd [project_root] && npx gitnexus query "tên function/class cần check"
```

**Kết quả:** Danh sách functions liên quan, grouped theo process/flow.

### 2. Tìm code liên quan (Query)

```bash
cd [project_root] && npx gitnexus query "authentication middleware"
```

**Kết quả:** Functions liên quan, grouped theo process/execution flow.

### 3. Xem tổng quan dự án

```bash
cd [project_root] && npx gitnexus status
cd [project_root] && npx gitnexus list
```

**Kết quả:** Index stats (nodes, edges, clusters) + repo list.

### 4. Phát hiện thay đổi (Pre-commit Check)

```bash
cd [project_root] && npx gitnexus query "recent changes"
```

### 5. Re-index khi code thay đổi

```bash
# Quick re-index (chỉ files đã thay đổi)
cd [project_root] && npx gitnexus analyze

# Full re-index (force)
cd [project_root] && npx gitnexus analyze --force

# Index + generate skills per module
cd [project_root] && npx gitnexus analyze --skills
```

## Hướng dẫn cho AI Agent

Khi workflow trigger GitNexus, AI PHẢI:

1. **Kiểm tra `.gitnexus/` tồn tại** trước khi chạy bất kỳ command nào
2. **Chạy CLI qua `run_command`** tool với `SafeToAutoRun: true` (read-only, an toàn)
3. **Parse output text** và trích xuất thông tin hữu ích
4. **Hiển thị kết quả** gọn gàng cho user

### Template cho run_command:

```
run_command({
  CommandLine: "cd [project_root] && npx gitnexus query \"[search term]\"",
  Cwd: "[project_root]",
  SafeToAutoRun: true,
  WaitMsBeforeAsync: 10000
})
```

## Kết hợp với brain.json

| `.brain/brain.json` | GitNexus |
|---------------------|----------|
| Overview tổng quan (models, APIs, features) | Symbol-level graph (functions, calls, imports) |
| Cập nhật manual (`/save-brain`) | Auto re-index (`analyze`) |
| Đọc text | Query CLI commands |
| **Dùng cho**: Planning, recap (high-level) | **Dùng cho**: All workflows (symbol-level) |

> Hai cái **bổ trợ nhau**, không thay thế.
> - `/recap` = brain.json (project overview) + GitNexus (cấu trúc code)
> - `/code`, `/debug`, `/refactor` = GitNexus là primary intelligence

## Nâng cấp lên MCP (Tùy chọn)

Nếu platform hỗ trợ MCP, thêm config để có performance tốt hơn:
```json
{
  "mcpServers": {
    "gitnexus": {
      "command": "npx",
      "args": ["-y", "gitnexus@latest", "mcp"]
    }
  }
}
```
Khi MCP available, AI có thể dùng native MCP tools thay vì CLI.

## Lưu ý
- Index lưu trong `.gitnexus/` (gitignored tự động)
- Lần index đầu mất 30s-2min tùy project size
- Re-index nhanh hơn (chỉ update changed files)
- Wiki generation cần OPENAI_API_KEY hoặc tương đương
- CLI query mất ~2-3s (khởi động Node), MCP gần như tức thì
