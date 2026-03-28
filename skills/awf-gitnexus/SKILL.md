---
name: awf-gitnexus
description: Code Intelligence via GitNexus knowledge graph. Auto-activates during /refactor, /review, /debug, /audit on large projects. Provides impact analysis, process tracing, safe refactoring, and codebase overview.
---

# AWF Skill: GitNexus Code Intelligence

## Mô tả
GitNexus xây dựng **knowledge graph** cho codebase — theo dõi mọi function, class, import, call chain, dependency. Cung cấp cho AI agent khả năng:
- **Impact Analysis** — biết function nào bị ảnh hưởng khi sửa code
- **Process Tracing** — theo dõi execution flow từ entry point
- **Safe Refactoring** — rename multi-file chính xác
- **360° Context** — xem tất cả incoming/outgoing relationships của 1 symbol

## Trigger
Skill này tự động kích hoạt khi:
- `/recap` — query graph overview để hiểu toàn bộ cấu trúc dự án
- `/refactor` — impact analysis trước khi refactor, safe rename
- `/review` — overview toàn bộ codebase, cluster analysis
- `/debug` — trace call chains tìm bug, context lookup
- `/audit` — kiểm tra dependencies, dead code, security surface
- `/code` — context lookup trước khi code, detect changes sau khi code

## Workflow ↔ GitNexus Tool Mapping

| Workflow | GitNexus Tools | Mục đích |
|----------|---------------|----------|
| `/recap` | `query("overview")`, `cypher(clusters)` | Hiểu tổng quan cấu trúc |
| `/refactor` | `impact()`, `rename()`, `detect_changes()` | Blast radius + safe rename |
| `/review` | `query()`, `cypher(stats)` | Phân tích code quality |
| `/debug` | `context()`, `query()` | Trace call chains |
| `/audit` | `cypher(dependencies)`, `query(security)` | Dependency + security scan |
| `/code` | `context()`, `detect_changes()` | Context trước code + verify sau |

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

## Sử dụng trong Workflow

### 1. Trước khi sửa code (Impact Analysis)

Khi AI chuẩn bị sửa một function/class quan trọng:

```
# Gọi MCP tool: impact
impact({
  target: "KnowledgeBlock",     # Tên function/class cần check
  direction: "upstream",         # upstream = ai depend vào nó, downstream = nó depend vào ai
  minConfidence: 0.7
})
```

**Kết quả:** Danh sách functions sẽ bị break khi sửa target.

### 2. Tìm code liên quan (Query)

```
# Gọi MCP tool: query
query({
  query: "authentication middleware"
})
```

**Kết quả:** Functions liên quan, grouped theo process/execution flow.

### 3. Xem 360° của 1 symbol (Context)

```
# Gọi MCP tool: context
context({
  name: "handleAddBlock"
})
```

**Kết quả:** Symbol info + incoming calls + outgoing calls + processes liên quan.

### 4. Phát hiện thay đổi (Pre-commit Check)

```
# Gọi MCP tool: detect_changes
detect_changes({
  scope: "all"
})
```

**Kết quả:** Changed symbols, affected processes, risk level.

### 5. Safe Rename (Multi-file)

```
# Gọi MCP tool: rename
rename({
  symbol_name: "collectLeafBlocks",
  new_name: "flattenBlockTree",
  dry_run: true              # true = chỉ xem, false = thực hiện
})
```

### 6. Cypher Query (Advanced)

```
# Gọi MCP tool: cypher
cypher({
  query: "MATCH (f:Symbol {kind: 'Function'})-[:CALLS]->(g) WHERE f.filePath CONTAINS 'api/' RETURN f.name, g.name LIMIT 20"
})
```

## Re-index khi code thay đổi

```bash
# Quick re-index (chỉ files đã thay đổi)
npx gitnexus analyze

# Full re-index (force)
npx gitnexus analyze --force

# Index + generate skills per module
npx gitnexus analyze --skills
```

## MCP Server Setup

GitNexus expose MCP server qua stdio. Để thêm vào editor:

### Cho Antigravity/Gemini (manual config):
Thêm MCP server config nếu hệ thống hỗ trợ:
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

### Cho Cursor:
```bash
npx gitnexus setup
```

## Kết hợp với brain.json

| `.brain/brain.json` | GitNexus |
|---------------------|----------|
| Overview tổng quan (models, APIs, features) | Symbol-level graph (functions, calls, imports) |
| Cập nhật manual (`/save-brain`) | Auto re-index (`analyze`) |
| Đọc text | Query MCP tools |
| **Dùng cho**: Planning, recap (high-level) | **Dùng cho**: All workflows (symbol-level) |

> Hai cái **bổ trợ nhau**, không thay thế.
> - `/recap` = brain.json (project overview) + GitNexus (cấu trúc code)
> - `/code`, `/debug`, `/refactor` = GitNexus là primary intelligence

## Lưu ý
- Index lưu trong `.gitnexus/` (gitignored tự động)
- Lần index đầu mất 30s-2min tùy project size
- Re-index nhanh hơn (chỉ update changed files)
- Wiki generation cần OPENAI_API_KEY hoặc tương đương
