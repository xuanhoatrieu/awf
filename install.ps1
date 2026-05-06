# AWF Installer for Windows (PowerShell)
# Tự động detect Antigravity Global Workflows

$RepoUrl = "https://raw.githubusercontent.com/xuanhoatrieu/awf/main/workflows"
$Workflows = @(
    "plan.md", "code.md", "visualize.md", "deploy.md", 
    "debug.md", "refactor.md", "test.md", "run.md", 
    "init.md", "recap.md", "rollback.md", "save_brain.md", 
    "audit.md", "cloudflare-tunnel.md", "README.md"
)

# Detect Antigravity Global Path
$AntigravityGlobal = "$env:USERPROFILE\.gemini\antigravity\global_workflows"
$GeminiMd = "$env:USERPROFILE\.gemini\GEMINI.md"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🚀 AWF - Antigravity Workflow Framework v3.0         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Cài Global Workflows
if (-not (Test-Path $AntigravityGlobal)) {
    New-Item -ItemType Directory -Force -Path $AntigravityGlobal | Out-Null
    Write-Host "📂 Đã tạo thư mục Global: $AntigravityGlobal" -ForegroundColor Green
} else {
    Write-Host "✅ Tìm thấy Antigravity Global: $AntigravityGlobal" -ForegroundColor Green
}

Write-Host "⏳ Đang tải workflows..." -ForegroundColor Cyan
$success = 0
foreach ($wf in $Workflows) {
    try {
        Invoke-WebRequest -Uri "$RepoUrl/$wf" -OutFile "$AntigravityGlobal\$wf" -ErrorAction Stop
        Write-Host "   ✅ $wf" -ForegroundColor Green
        $success++
    } catch {
        Write-Host "   ❌ $wf" -ForegroundColor Red
    }
}

# 2. Update Global Rules (GEMINI.md)
$AwfInstructions = @"

# AWF - Antigravity Workflow Framework
Bạn đã được cài đặt AWF. Khi user dùng lệnh /, hãy đọc file workflow tương ứng trong ~/.gemini/antigravity/global_workflows/:
- /plan, /code, /visualize, /deploy, /debug, /test, /run
- /init, /recap, /save-brain, /audit, /refactor, /rollback
"@

if (-not (Test-Path $GeminiMd)) {
    # Nếu chưa có file, tạo mới
    if (-not (Test-Path "$env:USERPROFILE\.gemini")) { New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini" | Out-Null }
    Set-Content -Path $GeminiMd -Value $AwfInstructions -Encoding UTF8
    Write-Host "✅ Đã tạo Global Rules (GEMINI.md)" -ForegroundColor Green
} else {
    # Nếu có rồi, check xem đã có AWF chưa
    $content = Get-Content $GeminiMd -Raw
    if (-not $content.Contains("AWF - Antigravity Workflow Framework")) {
        Add-Content -Path $GeminiMd -Value $AwfInstructions -Encoding UTF8
        Write-Host "✅ Đã cập nhật Global Rules (GEMINI.md)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "🎉 HOÀN TẤT! Đã cài $success workflows vào hệ thống." -ForegroundColor Yellow
Write-Host ""
Write-Host "👉 Bạn có thể dùng AWF ở BẤT KỲ project nào ngay lập tức!" -ForegroundColor Cyan
Write-Host "👉 Thử gõ '/plan' để kiểm tra." -ForegroundColor White
Write-Host ""
