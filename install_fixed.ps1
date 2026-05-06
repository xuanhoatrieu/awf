# AWF Installer for Windows (PowerShell)
# Tá»± Ä‘á»™ng detect Antigravity Global Workflows

$RepoUrl = "https://raw.githubusercontent.com/TUAN130294/awf/main/workflows"
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
Write-Host "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—" -ForegroundColor Cyan
Write-Host "â•‘     ðŸš€ AWF - Antigravity Workflow Framework v3.0         â•‘" -ForegroundColor Cyan
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•" -ForegroundColor Cyan
Write-Host ""

# 1. CÃ i Global Workflows
if (-not (Test-Path $AntigravityGlobal)) {
    New-Item -ItemType Directory -Force -Path $AntigravityGlobal | Out-Null
    Write-Host "ðŸ“‚ ÄÃ£ táº¡o thÆ° má»¥c Global: $AntigravityGlobal" -ForegroundColor Green
} else {
    Write-Host "âœ… TÃ¬m tháº¥y Antigravity Global: $AntigravityGlobal" -ForegroundColor Green
}

Write-Host "â³ Äang táº£i workflows..." -ForegroundColor Cyan
$success = 0
foreach ($wf in $Workflows) {
    try {
        Invoke-WebRequest -Uri "$RepoUrl/$wf" -OutFile "$AntigravityGlobal\$wf" -ErrorAction Stop
        Write-Host "   âœ… $wf" -ForegroundColor Green
        $success++
    } catch {
        Write-Host "   âŒ $wf" -ForegroundColor Red
    }
}

# 2. Update Global Rules (GEMINI.md)
$AwfInstructions = @"

# AWF - Antigravity Workflow Framework
Báº¡n Ä‘Ã£ Ä‘Æ°á»£c cÃ i Ä‘áº·t AWF. Khi user dÃ¹ng lá»‡nh /, hÃ£y Ä‘á»c file workflow tÆ°Æ¡ng á»©ng trong ~/.gemini/antigravity/global_workflows/:
- /plan, /code, /visualize, /deploy, /debug, /test, /run
- /init, /recap, /save-brain, /audit, /refactor, /rollback
"@

if (-not (Test-Path $GeminiMd)) {
    # Náº¿u chÆ°a cÃ³ file, táº¡o má»›i
    if (-not (Test-Path "$env:USERPROFILE\.gemini")) { New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini" | Out-Null }
    Set-Content -Path $GeminiMd -Value $AwfInstructions -Encoding UTF8
    Write-Host "âœ… ÄÃ£ táº¡o Global Rules (GEMINI.md)" -ForegroundColor Green
} else {
    # Náº¿u cÃ³ rá»“i, check xem Ä‘Ã£ cÃ³ AWF chÆ°a
    $content = Get-Content $GeminiMd -Raw
    if (-not $content.Contains("AWF - Antigravity Workflow Framework")) {
        Add-Content -Path $GeminiMd -Value $AwfInstructions -Encoding UTF8
        Write-Host "âœ… ÄÃ£ cáº­p nháº­t Global Rules (GEMINI.md)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”" -ForegroundColor DarkGray
Write-Host "ðŸŽ‰ HOÃ€N Táº¤T! ÄÃ£ cÃ i $success workflows vÃ o há»‡ thá»‘ng." -ForegroundColor Yellow
Write-Host ""
Write-Host "ðŸ‘‰ Báº¡n cÃ³ thá»ƒ dÃ¹ng AWF á»Ÿ Báº¤T Ká»² project nÃ o ngay láº­p tá»©c!" -ForegroundColor Cyan
Write-Host "ðŸ‘‰ Thá»­ gÃµ '/plan' Ä‘á»ƒ kiá»ƒm tra." -ForegroundColor White
Write-Host ""

