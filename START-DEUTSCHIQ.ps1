param(
    [switch]$StartNgrok
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$Backend = Join-Path $ProjectRoot "backend"
$Python = Join-Path $Backend "venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Python environment not found: $Python"
}

$BackendReady = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if (-not $BackendReady) {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "Set-Location '$Backend'; & '$Python' -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    )
    Write-Host "Backend started on port 8000" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    try {
        $RunningVersion = (Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/version" -TimeoutSec 2).version
    } catch {
        throw "Port 8000 is occupied by another service. Stop it before starting DeutschIQ."
    }
    if ($RunningVersion -ne "13.0.0") {
        throw "An older DeutschIQ backend ($RunningVersion) is already running. Stop it and run this command again."
    }
    Write-Host "DeutschIQ 13.0.0 backend is already running" -ForegroundColor Yellow
}

$Health = $null
for ($Attempt = 1; $Attempt -le 10 -and -not $Health; $Attempt++) {
    try {
        $Health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/health" -TimeoutSec 2
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-not $Health -or $Health.version -ne "13.0.0") {
    throw "DeutschIQ backend did not become healthy. Check the backend PowerShell window."
}
Write-Host "Health: database=$($Health.database), AI feedback=$($Health.ai_feedback)" -ForegroundColor Cyan

$BotProcess = Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -match 'app\.bot\.main'
}
if (-not $BotProcess) {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "Set-Location '$Backend'; & '$Python' -m app.bot.main"
    )
    Write-Host "Telegram bot started" -ForegroundColor Green
} else {
    Write-Host "Telegram bot is already running; a duplicate was not started" -ForegroundColor Yellow
}

if ($StartNgrok) {
    $NgrokProcess = Get-Process ngrok -ErrorAction SilentlyContinue
    if (-not $NgrokProcess) {
        Start-Process powershell.exe -ArgumentList @("-NoExit", "-Command", "ngrok http 8000")
        Write-Host "ngrok started for port 8000" -ForegroundColor Green
    } else {
        Write-Host "ngrok is already running" -ForegroundColor Yellow
    }
}

Write-Host "DeutschIQ 13.0.0 startup complete" -ForegroundColor Cyan
