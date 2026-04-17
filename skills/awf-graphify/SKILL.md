---
name: awf-graphify
description: Code Intelligence via Graphify knowledge graph. Auto-activates during /refactor, /review, /debug, /audit, /recap, /code on large projects. Provides impact analysis, process tracing, safe refactoring, and codebase overview. Uses CLI (Python, cross-platform).
---

# AWF Skill: Graphify Code Intelligence (CLI Mode)

## Mô tả
Graphify xây dựng **knowledge graph** cho codebase — theo dõi mọi function, class, import, call chain, dependency. Hỗ trợ **multimodal**: code, docs, images, PDF, video/audio. Cung cấp cho AI agent khả năng:
- **Impact Analysis** — biết function nào bị ảnh hưởng khi sửa code
- **Process Tracing** — theo dõi execution flow từ entry point (`graphify path`)
- **Safe Refactoring** — phân tích blast radius chính xác
- **360° Context** — xem tất cả incoming/outgoing relationships của 1 symbol
- **God Node Detection** — tìm các concepts trung tâm trong codebase
- **Community Clustering** — nhóm code theo chức năng (Leiden algorithm)

## Tại sao Graphify?
- **Multimodal:** Code + Docs + Images + Video + PDF → 1 knowledge graph
- **25 ngôn ngữ:** Python, JS, TS, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia, Verilog, SystemVerilog, Vue, Svelte, Dart
- **AST-based:** Code được phân tích bằng tree-sitter AST — không cần LLM cho code files
- **Portable:** `pip install graphifyy` — hoạt động trên mọi platform
- **Token-efficient:** ~71x fewer tokens per query so với đọc raw files
- **Interactive visualization:** `graph.html` — click nodes, search, filter by community

## Trigger
Skill này tự động kích hoạt khi:
- `/recap` — đọc GRAPH_REPORT.md để hiểu toàn bộ cấu trúc dự án
- `/refactor` — blast radius analysis, trace dependencies
- `/review` — overview toàn bộ codebase, god nodes, communities
- `/debug` — trace call chains tìm bug, path between symbols
- `/audit` — kiểm tra dead code, circular deps, API surface
- `/code` — context lookup trước khi code, detect changes sau khi code

## Workflow ↔ Graphify CLI Mapping

| Workflow | CLI Command | Mục đích |
|----------|------------|----------|
| `/recap` | Đọc `GRAPH_REPORT.md` | Hiểu tổng quan cấu trúc |
| `/refactor` | `graphify query "..."` | Blast radius + tìm dependencies |
| `/review` | `graphify query "overview"` | Phân tích code quality |
| `/debug` | `graphify path "A" "B"` | Trace call chains |
| `/audit` | `graphify query "..."` | Dead code + security scan |
| `/code` | `graphify query "..."` | Context trước code + verify sau |

## Điều kiện
- **Dự án phải được index trước**: Chạy `graphify .` trong thư mục dự án
- **Python >= 3.10** (pip install graphifyy)
- Không cần API key cho code extraction (AST-based)
- LLM extraction cho docs/images dùng API key của platform hiện tại

## Cách kiểm tra đã index chưa

```bash
# Kiểm tra thư mục output
ls graphify-out/

# Nếu chưa index → chạy graphify
graphify .

# Nếu index cũ (files đã thay đổi)
graphify . --update
```

## Sử dụng trong Workflow (CLI Commands)

### 1. Trước khi sửa code (Impact Analysis)

Khi AI chuẩn bị sửa một function/class quan trọng:

```bash
# Query knowledge graph
cd [project_root] && graphify query "[function/class cần check]" --graph graphify-out/graph.json
```

**Kết quả:** Nodes liên quan, edges (EXTRACTED/INFERRED), confidence scores, source files.

### 2. Trace path giữa 2 symbols

```bash
cd [project_root] && graphify path "SymbolA" "SymbolB"
```

**Kết quả:** Shortest path giữa 2 nodes trong graph, kèm edge types.

### 3. Giải thích 1 symbol

```bash
cd [project_root] && graphify explain "ClassName"
```

**Kết quả:** Plain-language explanation của node, relationships, community membership.

### 4. Xem tổng quan dự án

```bash
# Đọc report tổng quan (god nodes, communities, surprising connections)
cat [project_root]/graphify-out/GRAPH_REPORT.md
```

**Kết quả:** God nodes, community clusters, surprising connections, suggested questions.

### 5. Re-index khi code thay đổi

```bash
# Incremental update (chỉ files đã thay đổi, dùng SHA256 cache)
cd [project_root] && graphify . --update

# Full re-index
cd [project_root] && graphify .

# Auto-sync (chạy background, tự rebuild khi file thay đổi)
cd [project_root] && graphify . --watch
```

## Hướng dẫn cho AI Agent

Khi workflow trigger Graphify, AI PHẢI:

1. **Kiểm tra `graphify-out/` tồn tại** trước khi chạy bất kỳ command nào
2. **Đọc `GRAPH_REPORT.md`** cho high-level overview (god nodes, communities)
3. **Chạy CLI qua `run_command`** tool với `SafeToAutoRun: true` (read-only, an toàn)
4. **Parse output** và trích xuất thông tin hữu ích
5. **Hiển thị kết quả** gọn gàng cho user

### Template cho run_command:

```
run_command({
  CommandLine: "cd [project_root] && graphify query \"[search term]\" --graph graphify-out/graph.json",
  Cwd: "[project_root]",
  SafeToAutoRun: true,
  WaitMsBeforeAsync: 10000
})
```

## Kết hợp với brain.json

| `.brain/brain.json` | Graphify |
|---------------------|----------|
| Overview tổng quan (models, APIs, features) | Knowledge graph (functions, calls, imports, concepts) |
| Cập nhật manual (`/save-brain`) | Auto re-index (`graphify . --update`) |
| Đọc text | Query CLI / đọc GRAPH_REPORT.md |
| **Dùng cho**: Planning, recap (high-level) | **Dùng cho**: All workflows (symbol-level + semantic) |

> Hai cái **bổ trợ nhau**, không thay thế.
> - `/recap` = brain.json (project overview) + Graphify (cấu trúc code + god nodes)
> - `/code`, `/debug`, `/refactor` = Graphify là primary intelligence

## Nâng cấp lên MCP (Tùy chọn)

Nếu platform hỗ trợ MCP, chạy Graphify MCP server:
```json
{
  "mcpServers": {
    "graphify": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```
Khi MCP available, AI có thể dùng native MCP tools (`query_graph`, `get_node`, `get_neighbors`, `shortest_path`).

## Lưu ý
- Output lưu trong `graphify-out/` (nên thêm vào .gitignore)
- Lần index đầu mất vài phút tùy project size (code = instant AST, docs = LLM extraction)
- Re-index nhanh (SHA256 cache, chỉ re-process changed files)
- `--watch` mode tự rebuild khi code thay đổi
- Interactive graph tại `graphify-out/graph.html` — mở trong browser
- Package PyPI tên `graphifyy` (2 chữ y), CLI command là `graphify`
