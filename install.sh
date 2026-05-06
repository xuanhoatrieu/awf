#!/bin/bash
# AWF Installer for Mac/Linux — xuanhoatrieu fork v4.2
# Includes: Workflows + Skills (with scripts/templates) + Graphify Code Intelligence

REPO_URL="https://raw.githubusercontent.com/xuanhoatrieu/awf/main"

WORKFLOWS=(
    "plan.md" "code.md" "visualize.md" "deploy.md"
    "debug.md" "refactor.md" "test.md" "run.md"
    "init.md" "recap.md" "rollback.md" "save_brain.md"
    "audit.md" "review.md" "brainstorm.md" "design.md"
    "help.md" "next.md" "customize.md" "awf-update.md"
    "cloudflare-tunnel.md" "export.md" "textbook.md"
    "pptx.md" "question.md" "video.md"
    "README.md"
)

# Skills: name|subfiles (pipe-separated list of files relative to skill dir)
# SKILL.md is always downloaded; extra files listed after |
SKILL_NAMES=(
    "awf-adaptive-language"
    "awf-auto-save"
    "awf-context-help"
    "awf-error-translator"
    "awf-graphify"
    "awf-onboarding"
    "awf-session-restore"
    "awf-textbook"
    "awf-question-gen"
    "awf-pptx"
    "awf-video"
)

# Extra files per skill (beyond SKILL.md)
declare -A SKILL_FILES
SKILL_FILES["awf-pptx"]="scripts/pptx_generator.py scripts/tts_client.py scripts/voice_list.py scripts/batch_tts_bai03.py scripts/batch_tts_bai03_engvi.py"
SKILL_FILES["awf-video"]="scripts/render_video.py scripts/scan_3b1b.py templates/common_styles.py templates/gradient_descent.py templates/linear_regression.py templates/loss_landscape.py templates/neural_network.py templates/cross_entropy.py templates/test_latex.py templates/omnivoice_service.py"

# Detect paths
ANTIGRAVITY_GLOBAL="$HOME/.gemini/antigravity/global_workflows"
ANTIGRAVITY_SKILLS="$HOME/.gemini/antigravity/skills"
GEMINI_MD="$HOME/.gemini/GEMINI.md"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🚀 AWF - Antigravity Workflow Framework v4.2            ║"
echo "║  📦 By xuanhoatrieu (forked + customized)                ║"
echo "║  🔍 Includes: Graphify + PPTX + Video + Question-Gen     ║"
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
skill_file_count=0
for skill in "${SKILL_NAMES[@]}"; do
    mkdir -p "$ANTIGRAVITY_SKILLS/$skill"
    
    # Always download SKILL.md
    if curl -f -s -o "$ANTIGRAVITY_SKILLS/$skill/SKILL.md" "$REPO_URL/skills/$skill/SKILL.md"; then
        echo "   ✅ $skill/SKILL.md"
        ((skill_success++))
        ((skill_file_count++))
    else
        echo "   ❌ $skill/SKILL.md"
        continue
    fi
    
    # Download extra files if defined
    extra="${SKILL_FILES[$skill]}"
    if [ -n "$extra" ]; then
        for file in $extra; do
            # Create subdirectory if needed
            subdir=$(dirname "$file")
            if [ "$subdir" != "." ]; then
                mkdir -p "$ANTIGRAVITY_SKILLS/$skill/$subdir"
            fi
            
            if curl -f -s -o "$ANTIGRAVITY_SKILLS/$skill/$file" "$REPO_URL/skills/$skill/$file"; then
                echo "      📄 $file"
                ((skill_file_count++))
            else
                echo "      ⚠️  $file (skipped)"
            fi
        done
    fi
done
echo ""

# ==============================
# 3. Install Graphify (Global)
# ==============================
echo "⏳ Cài đặt Graphify Code Intelligence..."
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    PIP_CMD=$(command -v pip3 || command -v pip)
    $PIP_CMD install graphifyy 2>/dev/null
    if command -v graphify &> /dev/null; then
        echo "   ✅ Graphify installed ($(graphify --version 2>/dev/null || echo 'latest'))"
    else
        echo "   ⚠️  Graphify cài xong nhưng chưa thấy trong PATH"
        echo "   💡 Thử: pip3 install graphifyy"
    fi
else
    echo "   ⚠️  pip không có. Graphify cần Python >= 3.10"
    echo "   💡 Cài Python: https://www.python.org/downloads/"
fi
echo ""

# ==============================
# 4. Update Global Rules
# ==============================
AWF_INSTRUCTIONS='
# AWF - Antigravity Workflow Framework v4.2

## CRITICAL: Command Recognition
Khi user gõ các lệnh bắt đầu bằng `/` dưới đây, đây là AWF WORKFLOW COMMANDS.
Đọc file workflow tương ứng trong ~/.gemini/antigravity/global_workflows/:

## Commands:
- /init, /plan, /design, /visualize, /brainstorm
- /code, /run, /debug, /test, /refactor, /review, /audit
- /deploy, /rollback, /save-brain, /recap, /next, /help, /customize
- /export, /textbook, /pptx, /question, /video

## Skills (auto-trigger):
- awf-graphify: Code Intelligence via Graphify (auto on /refactor, /review, /debug, /audit, /recap, /code)
- awf-session-restore: Context restore at session start
- awf-auto-save: Auto-save on workflow end
- awf-adaptive-language: Adjust language to user level
- awf-error-translator: Human-friendly errors
- awf-onboarding: First-time guidance
- awf-context-help: Smart help
- awf-textbook: Ebook/textbook writing workflow
- awf-question-gen: Auto quiz generation (iSpring, Review, Moodle)
- awf-pptx: PPTX slide generation with TTS
- awf-video: ML animation with ManimCE + ManimGL

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
echo "4.2.0" > "$HOME/.gemini/awf_version"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 HOÀN TẤT!"
echo ""
echo "   📋 Workflows: $wf_success/${#WORKFLOWS[@]}"
echo "   🧩 Skills:    $skill_success/${#SKILL_NAMES[@]} (${skill_file_count} files)"
echo "   🔍 Graphify:  $(command -v graphify &> /dev/null && echo 'Installed' || echo 'Not installed')"
echo "   📌 Version:   4.2.0"
echo ""
echo "👉 Dùng ngay ở BẤT KỲ project nào!"
echo "👉 Gõ '/plan' để test. Gõ '/recap' để xem context."
echo ""
echo "🔍 Để index codebase với Graphify:"
echo "   cd your-project && graphify ."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
