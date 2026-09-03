param(
    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$Project = (Get-Location).Path

if (-not (Test-Path (Join-Path $Project "backend\app")) -or
    -not (Test-Path (Join-Path $Project "frontend\mini-app"))) {
    throw "Run this script from the DeutschIQ project root."
}

$Directories = @(
    "venv",
    ".venv",
    "backend\venv",
    "backend\.venv",
    "frontend\mini-app\node_modules",
    "frontend\mini-app\dist"
)

$Files = @(
    "DeutschIQ-all-code.txt",
    "tree.txt",
    "frontend\mini-app\src\App.css",
    "frontend\mini-app\src\index.css",
    "frontend\mini-app\src\assets\hero.png",
    "frontend\mini-app\src\assets\react.svg",
    "frontend\mini-app\src\assets\vite.svg",
    "frontend\mini-app\src\pages\Welcome.tsx"
)

$Targets = @()
foreach ($RelativePath in ($Directories + $Files)) {
    $FullPath = Join-Path $Project $RelativePath
    if (Test-Path -LiteralPath $FullPath) {
        $Targets += $FullPath
    }
}

$SourceRoots = @("backend\app", "backend\tests")
foreach ($SourceRoot in $SourceRoots) {
    $FullSourceRoot = Join-Path $Project $SourceRoot
    if (Test-Path -LiteralPath $FullSourceRoot) {
        $Targets += (Get-ChildItem -LiteralPath $FullSourceRoot -Directory -Filter "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue).FullName
        $Targets += (Get-ChildItem -LiteralPath $FullSourceRoot -File -Include "*.pyc", "*.pyo" -Recurse -Force -ErrorAction SilentlyContinue).FullName
    }
}
$Targets = $Targets | Sort-Object -Unique

if ($Targets.Count -eq 0) {
    Write-Host "Nothing to clean." -ForegroundColor Green
    exit 0
}

Write-Host "DeutschIQ cleanup preview:" -ForegroundColor Cyan
$Targets | ForEach-Object { Write-Host "  $_" }

if (-not $Apply) {
    Write-Host "Preview only. Run .\CLEAN-DEUTSCHIQ.ps1 -Apply to delete these items." -ForegroundColor Yellow
    exit 0
}

foreach ($Target in $Targets) {
    Remove-Item -LiteralPath $Target -Recurse -Force
}

Write-Host "Cleanup complete. Your .env files, database content and source files were preserved." -ForegroundColor Green
Write-Host "Recreate dependencies with: pip install -r backend\requirements.txt and npm ci --prefix frontend\mini-app"
