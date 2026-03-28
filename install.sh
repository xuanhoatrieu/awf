#!/bin/bash
# AWF Installer for Mac/Linux — xuanhoatrieu fork v4.1
# Includes: Workflows + Skills + GitNexus Code Intelligence

REPO_URL="https://raw.githubusercontent.com/xuanhoatrieu/awf/main"

WORKFLOWS=(
    "plan.md" "code.md" "visualize.md" "deploy.md"
    "debug.md" "refactor.md" "test.md" "run.md"
    "init.md" "recap.md" "rollback.md" "save_brain.md"
    "audit.md" "review.md" "brainstorm.md" "design.md"
    "help.md" "next.md" "customize.md" "awf-update.md"
    "README.md"
)

SKILLS=(
    "awf-adaptive-language"
    "awf-auto-save"
    "awf-context-help"
    "awf-error-translator"
    "awf-gitnexus"
    "awf-onboarding"
    "awf-session-restore"
)

# Detect paths
ANTIGRAVITY_GLOBAL="$HOME/.gemini/antigravity/global_workflows"
ANTIGRAVITY_SKILLS="$HOME/.gemini/antigravity/skills"
GEMINI_MD="$HOME/.gemini/GEMINI.md"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🚀 AWF - Antigravity Workflow Framework v4.1            ║"
echo "║  📦 By xuanhoatrieu (forked + customized)                ║"
echo "║  🔍 Includes: GitNexus Code Intelligence                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ==============================
# 1. Install Workflows
# ==============================
mkdir -p "$ANTIGRAVITY_GLOBAL"
echo "📂 Workflows → $ANTIGRAVITY_GLOBAL"
echo ""

echo "⏳ Đang tải workflows..."
wf_success=0
for wf in "${WORKFLOWS[@]}"; do
    if curl -f -s -o "$ANTIGRAVITY_GLOBAL/$wf" "$REPO_URL/workflows/$wf"; then
        echo "   ✅ $wf"
        ((wf_success++))
    else
        echo "   ❌ $wf"
    fi
done
echo ""

# ==============================
# 2. Install Skills
# ==============================
echo "⏳ Đang tải skills..."
skill_success=0
for skill in "${SKILLS[@]}"; do
    mkdir -p "$ANTIGRAVITY_SKILLS/$skill"
    if curl -f -s -o "$ANTIGRAVITY_SKILLS/$skill/SKILL.md" "$REPO_URL/skills/$skill/SKILL.md"; then
        echo "   ✅ $skill"
        ((skill_success++))
    else
        echo "   ❌ $skill"
    fi
done
echo ""

# ==============================
# 3. Install GitNexus (Global)
# ==============================
echo "⏳ Cài đặt GitNexus Code Intelligence..."
if command -v npm &> /dev/null; then
    npm install -g gitnexus@latest 2>/dev/null
    if command -v gitnexus &> /dev/null || npx gitnexus --version &> /dev/null; then
        echo "   ✅ GitNexus installed globally"
    else
        echo "   ⚠️  GitNexus sẽ dùng npx (không cần install global)"
    fi
else
    echo "   ⚠️  npm không có. GitNexus cần Node.js >= 18"
    echo "   💡 Cài Node.js: https://nodejs.org/"
fi
echo ""

# ==============================
# 4. Update Global Rules
# ==============================
AWF_INSTRUCTIONS='
# AWF - Antigravity Workflow Framework v4.1

## CRITICAL: Command Recognition
Khi user gõ các lệnh bắt đầu bằng `/` dưới đây, đây là AWF WORKFLOW COMMANDS.
Đọc file workflow tương ứng trong ~/.gemini/antigravity/global_workflows/:

## Commands:
- /init, /plan, /design, /visualize, /brainstorm
- /code, /run, /debug, /test, /refactor, /review, /audit
- /deploy, /rollback, /save-brain, /recap, /next, /help, /customize

## Skills (auto-trigger):
- awf-gitnexus: Code Intelligence via GitNexus (auto on /refactor, /review, /debug, /audit, /recap, /code)
- awf-session-restore: Context restore at session start
- awf-auto-save: Auto-save on workflow end
- awf-adaptive-language: Adjust language to user level
- awf-error-translator: Human-friendly errors
- awf-onboarding: First-time guidance
- awf-context-help: Smart help

## PERSISTENT DATA:
Mục `infrastructure` và `github` trong .brain/brain.json TUYỆT ĐỐI KHÔNG ĐƯỢC XÓA.
Luôn HỎI trước khi commit/push lên GitHub.
'

mkdir -p "$HOME/.gemini"
if [ ! -f "$GEMINI_MD" ]; then
    echo "$AWF_INSTRUCTIONS" > "$GEMINI_MD"
    echo "✅ Đã tạo Global Rules (GEMINI.md)"
else
    # Remove old AWF block and add new one
    if grep -q "AWF - Antigravity Workflow Framework" "$GEMINI_MD"; then
        # Create temp file without old AWF block
        sed '/# AWF - Antigravity Workflow Framework/,/^# [^A]/{ /^# [^A]/!d; }' "$GEMINI_MD" > "$GEMINI_MD.tmp"
        echo "$AWF_INSTRUCTIONS" >> "$GEMINI_MD.tmp"
        mv "$GEMINI_MD.tmp" "$GEMINI_MD"
        echo "✅ Đã cập nhật Global Rules (GEMINI.md)"
    else
        echo "$AWF_INSTRUCTIONS" >> "$GEMINI_MD"
        echo "✅ Đã thêm AWF vào Global Rules (GEMINI.md)"
    fi
fi

# ==============================
# 5. Save AWF Version
# ==============================
echo "4.1.0" > "$HOME/.gemini/awf_version"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 HOÀN TẤT!"
echo ""
echo "   📋 Workflows: $wf_success/${#WORKFLOWS[@]}"
echo "   🧩 Skills:    $skill_success/${#SKILLS[@]}"
echo "   🔍 GitNexus:  $(command -v gitnexus &> /dev/null && echo 'Installed' || echo 'Via npx')"
echo "   📌 Version:   4.1.0"
echo ""
echo "👉 Dùng ngay ở BẤT KỲ project nào!"
echo "👉 Gõ '/plan' để test. Gõ '/recap' để xem context."
echo ""
echo "🔍 Để index codebase với GitNexus:"
echo "   cd your-project && npx gitnexus analyze"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
