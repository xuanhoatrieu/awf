---
name: awf-auto-save
description: >-
  Auto-save brain context based on file edit count and workflow completion.
  Triggers: workflow end, 15+ file edits, user leaving, before notify_user.
version: 2.0.0
---

# AWF Auto-Save v2.0 (CLI-Based)

Tự động lưu session để không bao giờ mất context.

## Brain v2 File Structure

```
.brain/
├── project.json      # Meta, infra, github, tech_stack (ít thay đổi)
├── domain.json       # Kiến thức nghiệp vụ (hầu như không đổi)
├── knowledge.json    # Patterns, gotchas, decisions (thêm dần)
├── features.json     # Features grouped by module (thêm dần)
└── session.json      # Working_on, recent_changes (thay đổi liên tục)
```

## Trigger Conditions

### 1. Workflow End (Auto — silent save)
Sau khi hoàn thành bất kỳ workflow nào (`/code`, `/debug`, `/refactor`, `/test`, `/deploy`):
- Update `session.json` → working_on, recent_changes
- **Silent** — không thông báo user

### 2. File Edit Threshold (Auto — notify)
AI tự đếm số file đã edit trong session:
```
if file_edit_count >= 5:
    → Silent save session.json

if file_edit_count >= 15:
    → Save session.json
    → Show: "💾 Đã auto-save (15+ files changed). Anh có muốn /save-brain đầy đủ không?"
```

### 3. User Leaving Detection
Pattern matching trong tin nhắn user:
```
patterns:
  - "bye", "tạm biệt", "tạm nghỉ"
  - "tôi đi", "đi ăn cơm", "nghỉ thôi"
  - "hết giờ", "mai làm tiếp", "save"
  - "đóng app", "tắt máy"
```
→ Full save: session.json + knowledge.json (nếu có decisions/gotchas mới)

### 4. Before notify_user (Auto — silent)
Trước mỗi lần gọi `notify_user` (kết thúc task view):
→ Silent save session.json

## Execution Logic

### Save Session (Lightweight — ~20 tokens)
```
Chỉ update session.json:
1. working_on → task hiện tại
2. recent_changes → append (max 10, xóa cũ nhất)
3. updated_at → timestamp
```

### Save Full (Khi user gọi /save-brain hoặc leaving)
```
1. session.json → working_on + recent_changes
2. knowledge.json → append gotchas/patterns mới (nếu có)
3. features.json → update status (nếu feature mới hoàn thành)
4. project.json → update meta.last_saved + save_count
```

## Hướng dẫn cho AI Agent

### Đếm file edits
AI PHẢI tự track trong context:
- Mỗi lần gọi `write_to_file`, `replace_file_content`, `multi_replace_file_content` → +1
- Khi count >= 5 → trigger silent save
- Khi count >= 15 → trigger save + notify

### Session.json update template
```json
{
  "updated_at": "[ISO timestamp]",
  "working_on": {
    "feature": "[tên feature]",
    "task": "[mô tả task hiện tại]",
    "status": "in_progress|completed",
    "notes": "[context quan trọng]"
  }
}
```

### recent_changes pruning
- Giữ tối đa **10 entries**
- Khi thêm entry mới mà đã đủ 10 → xóa entry cũ nhất
- Mỗi entry: `{ timestamp, type, description }` (không cần files array)

## Integration with Workflows

Mỗi workflow PHẢI có đoạn Post-Workflow cuối cùng:

```markdown
## Post-Workflow: Auto-Save
Sau khi hoàn thành:
1. Update session.json → working_on (status: completed)
2. Append recent_changes
3. Nếu có decisions/gotchas mới → append vào knowledge.json
```

## Error Handling

```
if save_fails:
    retry 1 time
    if still fails:
        → "⚠️ Không lưu được session. Kiểm tra quyền ghi file."
```

## Config (trong preferences.json)

```json
{
  "auto_save": {
    "enabled": true,
    "silent_threshold": 5,
    "notify_threshold": 15,
    "max_recent_changes": 10
  }
}
```
