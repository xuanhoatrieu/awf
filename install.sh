#!/usr/bin/env bash
# AWF - Antigravity Workflow Framework v4.3
# Installer for Linux/macOS
# By xuanhoatrieu (forked + customized)
# Includes: Workflows + Skills + Graphify + Harness Integration

set -euo pipefail

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

# Harness template files (downloaded into ~/.gemini/antigravity/harness/)
HARNESS_FILES=(
    "docs/FEATURE_INTAKE.md"
    "docs/HARNESS.md"
    "docs/ARCHITECTURE.md"
    "docs/TEST_MATRIX.md"
    "docs/GLOSSARY.md"
    "docs/HARNESS_BACKLOG.md"
    "docs/README.md"
    "docs/product/README.md"
    "docs/stories/README.md"
    "docs/stories/backlog.md"
    "docs/decisions/README.md"
    "docs/decisions/0001-harness-first-development.md"
    "docs/decisions/0002-post-spec-product-lifecycle.md"
    "docs/decisions/0003-generic-spec-intake-harness.md"
    "docs/templates/story.md"
    "docs/templates/decision.md"
    "docs/templates/spec-intake.md"
    "docs/templates/validation-report.md"
    "docs/templates/high-risk-story/overview.md"
    "docs/templates/high-risk-story/design.md"
    "docs/templates/high-risk-story/execplan.md"
    "docs/templates/high-risk-story/validation.md"
    "scripts-README.md"
)

# Detect paths
ANTIGRAVITY_GLOBAL="$HOME/.gemini/antigravity/global_workflows"
ANTIGRAVITY_SKILLS="$HOME/.gemini/antigravity/skills"
ANTIGRAVITY_HARNESS="$HOME/.gemini/antigravity/harness"
GEMINI_MD="$HOME/.gemini/GEMINI.md"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🚀 AWF - Antigravity Workflow Framework v4.3            ║"
echo "║  📦 By xuanhoatrieu (forked + customized)                ║"
echo "║  🔍 Graphify + PPTX + Video + Question-Gen + Harness     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ==============================
# 1. Install Workflows
# ==============================
mkdir -p "$ANTIGRAVITY_GLOBAL"
echo "📂 Workflows → $ANTIGRAVITY_GLOBAL"
echo ""

echo "⏳ Downloading workflows..."
wf_success=0
for wf in "${WORKFLOWS[@]}"; do
    if curl -f -s -o "$ANTIGRAVITY_GLOBAL/$wf" "$REPO_URL/workflows/$wf"; then
        echo "   ✅ $wf"
        wf_success=$((wf_success + 1))
    else
        echo "   ❌ $wf"
    fi
done
echo ""

# ==============================
# 2. Install Skills
# ==============================
echo "⏳ Downloading skills..."
skill_success=0
skill_file_count=0
for skill in "${SKILL_NAMES[@]}"; do
    mkdir -p "$ANTIGRAVITY_SKILLS/$skill"

    # Always download SKILL.md
    if curl -f -s -o "$ANTIGRAVITY_SKILLS/$skill/SKILL.md" "$REPO_URL/skills/$skill/SKILL.md"; then
        echo "   ✅ $skill/SKILL.md"
        skill_success=$((skill_success + 1))
        skill_file_count=$((skill_file_count + 1))
    else
        echo "   ❌ $skill/SKILL.md"
        continue
    fi

    # Download extra files if defined
    extra="${SKILL_FILES[$skill]:-}"
    if [ -n "$extra" ]; then
        for file in $extra; do
            # Create subdirectory if needed
            subdir=$(dirname "$file")
            if [ "$subdir" != "." ]; then
                mkdir -p "$ANTIGRAVITY_SKILLS/$skill/$subdir"
            fi

            if curl -f -s -o "$ANTIGRAVITY_SKILLS/$skill/$file" "$REPO_URL/skills/$skill/$file"; then
                echo "      📄 $file"
                skill_file_count=$((skill_file_count + 1))
            else
                echo "      ⚠️  $file (skipped)"
            fi
        done
    fi
done
echo ""

# ==============================
# 3. Install Graphify
# ==============================
echo "⏳ Installing Graphify Code Intelligence..."
PIP_CMD=""
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi

if [ -n "$PIP_CMD" ]; then
    $PIP_CMD install graphifyy 2>/dev/null || true
    if command -v graphify &> /dev/null; then
        echo "   ✅ Graphify installed ($(graphify --version 2>/dev/null || echo 'latest'))"
    else
        echo "   ⚠️  Graphify installed but not in PATH"
        echo "   💡 Try: pip3 install graphifyy"
    fi
else
    echo "   ⚠️  pip not found. Graphify needs Python >= 3.10"
    echo "   💡 Install Python: https://www.python.org/downloads/"
fi
echo ""

# ==============================
# 4. Download Harness Templates
# ==============================
echo "⏳ Downloading Harness templates..."
mkdir -p "$ANTIGRAVITY_HARNESS"
harness_success=0
for hf in "${HARNESS_FILES[@]}"; do
    # Create subdirectory if needed
    subdir=$(dirname "$hf")
    if [ "$subdir" != "." ]; then
        mkdir -p "$ANTIGRAVITY_HARNESS/$subdir"
    fi

    if curl -f -s -o "$ANTIGRAVITY_HARNESS/$hf" "$REPO_URL/harness/$hf"; then
        echo "   ✅ $hf"
        harness_success=$((harness_success + 1))
    else
        echo "   ❌ $hf"
    fi
done
echo ""

# ==============================
# 5. Update Global Rules (GEMINI.md)
# ==============================
AWF_INSTRUCTIONS='

# AWF - Antigravity Workflow Framework v4.3

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

## Harness Integration:
Khi dự án có docs/FEATURE_INTAKE.md hoặc docs/HARNESS.md, agent PHẢI:
- Phân loại risk (tiny/normal/high-risk) trước khi code
- Tạo story file cho normal+ tasks
- Cập nhật docs/TEST_MATRIX.md khi thêm/sửa test
- Ghi decision record cho quyết định kiến trúc quan trọng

## PERSISTENT DATA:
Mục `infrastructure` và `github` trong .brain/brain.json TUYỆT ĐỐI KHÔNG ĐƯỢC XÓA.
Luôn HỎI trước khi commit/push lên GitHub.
'

mkdir -p "$HOME/.gemini"
if [ ! -f "$GEMINI_MD" ]; then
    echo "$AWF_INSTRUCTIONS" > "$GEMINI_MD"
    echo "✅ Created Global Rules (GEMINI.md)"
else
    # Remove old AWF block and add new one
    if grep -q "AWF - Antigravity Workflow Framework" "$GEMINI_MD"; then
        # Create temp file without old AWF block
        sed '/# AWF - Antigravity Workflow Framework/,/^# [^A]/{ /^# [^A]/!d; }' "$GEMINI_MD" > "$GEMINI_MD.tmp"
        echo "$AWF_INSTRUCTIONS" >> "$GEMINI_MD.tmp"
        mv "$GEMINI_MD.tmp" "$GEMINI_MD"
        echo "✅ Updated Global Rules (GEMINI.md)"
    else
        echo "$AWF_INSTRUCTIONS" >> "$GEMINI_MD"
        echo "✅ Added AWF to Global Rules (GEMINI.md)"
    fi
fi

echo "4.3.0" > "$HOME/.gemini/awf_version"

# ==============================
# Summary
# ==============================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 DONE!"
echo ""
echo "   📋 Workflows: $wf_success/${#WORKFLOWS[@]}"
echo "   🧩 Skills:    $skill_success/${#SKILL_NAMES[@]} (${skill_file_count} files)"
echo "   🔍 Graphify:  $(command -v graphify &> /dev/null && echo 'Installed' || echo 'Not installed')"
echo "   🏗️  Harness:   $harness_success/${#HARNESS_FILES[@]} templates cached"
echo "   📌 Version:   4.3.0"
echo ""
echo "👉 Use AWF in ANY project right now!"
echo "👉 Type '/init' to create a project (auto-installs Harness)"
echo "👉 Type '/plan' to plan features. Type '/recap' for context."
echo ""
echo "🔍 To index codebase with Graphify:"
echo "   cd your-project && graphify update ."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
