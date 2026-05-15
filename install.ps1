# AWF - Antigravity Workflow Framework v4.3
# Installer for Windows (PowerShell)
# By xuanhoatrieu (forked + customized)
# Includes: Workflows + Skills + Graphify + Harness Integration

$RepoUrl = "https://raw.githubusercontent.com/xuanhoatrieu/awf/main"

$Workflows = @(
    "plan.md", "code.md", "visualize.md", "deploy.md",
    "debug.md", "refactor.md", "test.md", "run.md",
    "init.md", "recap.md", "rollback.md", "save_brain.md",
    "audit.md", "review.md", "brainstorm.md", "design.md",
    "help.md", "next.md", "customize.md", "awf-update.md",
    "cloudflare-tunnel.md", "export.md", "textbook.md",
    "pptx.md", "question.md", "video.md",
    "README.md"
)

# Skills: name only (SKILL.md always downloaded)
$SkillNames = @(
    "awf-adaptive-language",
    "awf-auto-save",
    "awf-context-help",
    "awf-error-translator",
    "awf-graphify",
    "awf-onboarding",
    "awf-session-restore",
    "awf-textbook",
    "awf-question-gen",
    "awf-pptx",
    "awf-video"
)

# Extra files per skill (beyond SKILL.md)
$SkillFiles = @{
    "awf-pptx" = @(
        "scripts/pptx_generator.py",
        "scripts/tts_client.py",
        "scripts/voice_list.py",
        "scripts/batch_tts_bai03.py",
        "scripts/batch_tts_bai03_engvi.py"
    )
    "awf-video" = @(
        "scripts/render_video.py",
        "scripts/scan_3b1b.py",
        "templates/common_styles.py",
        "templates/gradient_descent.py",
        "templates/linear_regression.py",
        "templates/loss_landscape.py",
        "templates/neural_network.py",
        "templates/cross_entropy.py",
        "templates/test_latex.py",
        "templates/omnivoice_service.py"
    )
}

# Harness template files
$HarnessFiles = @(
    "docs/FEATURE_INTAKE.md",
    "docs/HARNESS.md",
    "docs/ARCHITECTURE.md",
    "docs/TEST_MATRIX.md",
    "docs/GLOSSARY.md",
    "docs/HARNESS_BACKLOG.md",
    "docs/README.md",
    "docs/product/README.md",
    "docs/stories/README.md",
    "docs/stories/backlog.md",
    "docs/decisions/README.md",
    "docs/decisions/0001-harness-first-development.md",
    "docs/decisions/0002-post-spec-product-lifecycle.md",
    "docs/decisions/0003-generic-spec-intake-harness.md",
    "docs/templates/story.md",
    "docs/templates/decision.md",
    "docs/templates/spec-intake.md",
    "docs/templates/validation-report.md",
    "docs/templates/high-risk-story/overview.md",
    "docs/templates/high-risk-story/design.md",
    "docs/templates/high-risk-story/execplan.md",
    "docs/templates/high-risk-story/validation.md",
    "scripts-README.md"
)

# Detect paths
$AntigravityGlobal = "$env:USERPROFILE\.gemini\antigravity\global_workflows"
$AntigravitySkills = "$env:USERPROFILE\.gemini\antigravity\skills"
$AntigravityHarness = "$env:USERPROFILE\.gemini\antigravity\harness"
$GeminiMd = "$env:USERPROFILE\.gemini\GEMINI.md"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  AWF - Antigravity Workflow Framework v4.3                     " -ForegroundColor Cyan
Write-Host "  By xuanhoatrieu (forked + customized)                         " -ForegroundColor Cyan
Write-Host "  Graphify + PPTX + Video + Question-Gen + Harness              " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# ==============================
# 1. Install Workflows
# ==============================
if (-not (Test-Path $AntigravityGlobal)) {
    New-Item -ItemType Directory -Force -Path $AntigravityGlobal | Out-Null
    Write-Host "Created: $AntigravityGlobal" -ForegroundColor Green
} else {
    Write-Host "Found: $AntigravityGlobal" -ForegroundColor Green
}

Write-Host "Downloading workflows..." -ForegroundColor Cyan
$wfSuccess = 0
foreach ($wf in $Workflows) {
    try {
        Invoke-WebRequest -Uri "$RepoUrl/workflows/$wf" -OutFile "$AntigravityGlobal\$wf" -ErrorAction Stop -UseBasicParsing
        Write-Host "   OK  $wf" -ForegroundColor Green
        $wfSuccess++
    } catch {
        Write-Host "   FAIL  $wf" -ForegroundColor Red
    }
}
Write-Host ""

# ==============================
# 2. Install Skills
# ==============================
Write-Host "Downloading skills..." -ForegroundColor Cyan
$skillSuccess = 0
$skillFileCount = 0

foreach ($skill in $SkillNames) {
    $skillDir = "$AntigravitySkills\$skill"
    if (-not (Test-Path $skillDir)) {
        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
    }

    # Always download SKILL.md
    try {
        Invoke-WebRequest -Uri "$RepoUrl/skills/$skill/SKILL.md" -OutFile "$skillDir\SKILL.md" -ErrorAction Stop -UseBasicParsing
        Write-Host "   OK  $skill/SKILL.md" -ForegroundColor Green
        $skillSuccess++
        $skillFileCount++
    } catch {
        Write-Host "   FAIL  $skill/SKILL.md" -ForegroundColor Red
        continue
    }

    # Download extra files if defined
    if ($SkillFiles.ContainsKey($skill)) {
        foreach ($file in $SkillFiles[$skill]) {
            # Create subdirectory if needed
            $subdir = Split-Path $file -Parent
            if ($subdir) {
                $fullSubdir = "$skillDir\$subdir"
                if (-not (Test-Path $fullSubdir)) {
                    New-Item -ItemType Directory -Force -Path $fullSubdir | Out-Null
                }
            }

            try {
                $fileUrl = "$RepoUrl/skills/$skill/$($file -replace '\\','/')"
                Invoke-WebRequest -Uri $fileUrl -OutFile "$skillDir\$file" -ErrorAction Stop -UseBasicParsing
                Write-Host "      $file" -ForegroundColor DarkGreen
                $skillFileCount++
            } catch {
                Write-Host "      $file (skipped)" -ForegroundColor Yellow
            }
        }
    }
}
Write-Host ""

# ==============================
# 3. Install Graphify
# ==============================
Write-Host "Installing Graphify Code Intelligence..." -ForegroundColor Cyan
$pipCmd = Get-Command pip3 -ErrorAction SilentlyContinue
if (-not $pipCmd) { $pipCmd = Get-Command pip -ErrorAction SilentlyContinue }
if ($pipCmd) {
    & $pipCmd.Source install graphifyy 2>$null
    $graphifyCmd = Get-Command graphify -ErrorAction SilentlyContinue
    if ($graphifyCmd) {
        Write-Host "   OK  Graphify installed" -ForegroundColor Green
    } else {
        Write-Host "   WARN  Graphify installed but not in PATH" -ForegroundColor Yellow
        Write-Host "   TIP: pip install graphifyy" -ForegroundColor DarkGray
    }
} else {
    Write-Host "   WARN  pip not found. Graphify needs Python >= 3.10" -ForegroundColor Yellow
    Write-Host "   TIP: https://www.python.org/downloads/" -ForegroundColor DarkGray
}
Write-Host ""

# ==============================
# 4. Download Harness Templates
# ==============================
Write-Host "Downloading Harness templates..." -ForegroundColor Cyan
if (-not (Test-Path $AntigravityHarness)) {
    New-Item -ItemType Directory -Force -Path $AntigravityHarness | Out-Null
}
$harnessSuccess = 0
foreach ($hf in $HarnessFiles) {
    $subdir = Split-Path $hf -Parent
    if ($subdir) {
        $fullSubdir = "$AntigravityHarness\$subdir"
        if (-not (Test-Path $fullSubdir)) {
            New-Item -ItemType Directory -Force -Path $fullSubdir | Out-Null
        }
    }
    try {
        $fileUrl = "$RepoUrl/harness/$($hf -replace '\\','/')"
        Invoke-WebRequest -Uri $fileUrl -OutFile "$AntigravityHarness\$hf" -ErrorAction Stop -UseBasicParsing
        Write-Host "   OK  $hf" -ForegroundColor Green
        $harnessSuccess++
    } catch {
        Write-Host "   FAIL  $hf" -ForegroundColor Red
    }
}
Write-Host ""

# ==============================
# 4. Update Global Rules (GEMINI.md)
# ==============================
$AwfInstructions = @"

# AWF - Antigravity Workflow Framework v4.3

## CRITICAL: Command Recognition
Khi user go cac lenh bat dau bang ``/`` duoi day, day la AWF WORKFLOW COMMANDS.
Doc file workflow tuong ung trong ~/.gemini/antigravity/global_workflows/:

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
Khi du an co docs/FEATURE_INTAKE.md hoac docs/HARNESS.md, agent PHAI:
- Phan loai risk (tiny/normal/high-risk) truoc khi code
- Tao story file cho normal+ tasks
- Cap nhat docs/TEST_MATRIX.md khi them/sua test
- Ghi decision record cho quyet dinh kien truc quan trong

## PERSISTENT DATA:
Muc ``infrastructure`` va ``github`` trong .brain/brain.json TUYET DOI KHONG DUOC XOA.
Luon HOI truoc khi commit/push len GitHub.
"@

if (-not (Test-Path "$env:USERPROFILE\.gemini")) {
    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini" | Out-Null
}
if (-not (Test-Path $GeminiMd)) {
    Set-Content -Path $GeminiMd -Value $AwfInstructions -Encoding UTF8
    Write-Host "OK  Created Global Rules (GEMINI.md)" -ForegroundColor Green
} else {
    $content = Get-Content $GeminiMd -Raw
    if ($content -match "AWF - Antigravity Workflow Framework") {
        # Replace old AWF block
        $newContent = $content -replace "(?s)# AWF - Antigravity Workflow Framework.*?(?=\n# [^A]|\z)", ""
        Set-Content -Path $GeminiMd -Value ($newContent + $AwfInstructions) -Encoding UTF8
        Write-Host "OK  Updated Global Rules (GEMINI.md)" -ForegroundColor Green
    } else {
        Add-Content -Path $GeminiMd -Value $AwfInstructions -Encoding UTF8
        Write-Host "OK  Added AWF to Global Rules (GEMINI.md)" -ForegroundColor Green
    }
}

# ==============================
# 5. Save AWF Version
# ==============================
Set-Content -Path "$env:USERPROFILE\.gemini\awf_version" -Value "4.3.0"

# ==============================
# 6. Harness Integration Notice
# ==============================
Write-Host ""
Write-Host "Harness Integration" -ForegroundColor Cyan
Write-Host "   Harness templates are cached locally." -ForegroundColor White
Write-Host "   Use /init to create a project with Harness auto-installed." -ForegroundColor White
Write-Host ""

# ==============================
# Summary
# ==============================
Write-Host "================================================================" -ForegroundColor DarkGray
Write-Host "  DONE!" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Workflows: $wfSuccess/$($Workflows.Count)" -ForegroundColor White
Write-Host "   Skills:    $skillSuccess/$($SkillNames.Count) ($skillFileCount files)" -ForegroundColor White
$graphifyStatus = if (Get-Command graphify -ErrorAction SilentlyContinue) { "Installed" } else { "Not installed" }
Write-Host "   Graphify:  $graphifyStatus" -ForegroundColor White
Write-Host "   Harness:   $harnessSuccess/$($HarnessFiles.Count) templates cached" -ForegroundColor White
Write-Host "   Version:   4.3.0" -ForegroundColor White
Write-Host ""
Write-Host "  Use AWF in ANY project right now!" -ForegroundColor Cyan
Write-Host "  Type /init to create a project (auto-installs Harness)" -ForegroundColor White
Write-Host "  Type /plan to plan features. Type /recap for context." -ForegroundColor White
Write-Host ""
Write-Host "  To index codebase with Graphify:" -ForegroundColor White
Write-Host "  cd your-project; graphify update ." -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor DarkGray
