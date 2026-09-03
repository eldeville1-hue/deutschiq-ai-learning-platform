param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,
    [string]$Region = "europe-west3",
    [string]$Service = "deutschiq"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    throw "Google Cloud CLI (gcloud) is not installed."
}
if ([string]::IsNullOrWhiteSpace($env:BOT_TOKEN)) {
    throw "Set BOT_TOKEN in this PowerShell session first."
}
if ([string]::IsNullOrWhiteSpace($env:DATABASE_URL)) {
    throw "Set DATABASE_URL to an external PostgreSQL database first."
}

function Set-CloudSecret {
    param([string]$Name, [string]$Value)
    $exists = gcloud secrets describe $Name --project $ProjectId 2>$null
    if ($LASTEXITCODE -ne 0) {
        gcloud secrets create $Name --replication-policy=automatic --project $ProjectId | Out-Null
    }
    $Value | gcloud secrets versions add $Name --data-file=- --project $ProjectId | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not update secret $Name" }
}

gcloud config set project $ProjectId | Out-Null
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com

$projectNumber = gcloud projects describe $ProjectId --format "value(projectNumber)"
if ([string]::IsNullOrWhiteSpace($projectNumber)) { throw "Could not resolve Google Cloud project number." }
$runtimeServiceAccount = "$projectNumber-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding $ProjectId `
    --member "serviceAccount:$runtimeServiceAccount" `
    --role "roles/secretmanager.secretAccessor" `
    --condition=None | Out-Null

$webhookSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 48 | ForEach-Object {[char]$_})
$taskSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 48 | ForEach-Object {[char]$_})
$appSecret = -join ((33..126) | Get-Random -Count 56 | ForEach-Object {[char]$_})

Set-CloudSecret "deutschiq-bot-token" $env:BOT_TOKEN
Set-CloudSecret "deutschiq-database-url" $env:DATABASE_URL
Set-CloudSecret "deutschiq-webhook-secret" $webhookSecret
Set-CloudSecret "deutschiq-task-secret" $taskSecret
Set-CloudSecret "deutschiq-app-secret" $appSecret

$secretBindings = "BOT_TOKEN=deutschiq-bot-token:latest,DATABASE_URL=deutschiq-database-url:latest,TELEGRAM_WEBHOOK_SECRET=deutschiq-webhook-secret:latest,TASK_SECRET=deutschiq-task-secret:latest,SECRET_KEY=deutschiq-app-secret:latest"
if (-not [string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) {
    Set-CloudSecret "deutschiq-openai-key" $env:OPENAI_API_KEY
    $secretBindings += ",OPENAI_API_KEY=deutschiq-openai-key:latest"
}

gcloud run deploy $Service `
    --source . `
    --region $Region `
    --allow-unauthenticated `
    --min-instances 0 `
    --max-instances 1 `
    --memory 512Mi `
    --cpu 1 `
    --set-env-vars "BOT_MODE=polling,WEBAPP_URL=https://example.com,DEBUG=false" `
    --set-secrets $secretBindings
if ($LASTEXITCODE -ne 0) { throw "Initial Cloud Run deployment failed." }

$serviceUrl = gcloud run services describe $Service --region $Region --format "value(status.url)"
if ([string]::IsNullOrWhiteSpace($serviceUrl)) { throw "Cloud Run service URL was not returned." }

gcloud run services update $Service `
    --region $Region `
    --update-env-vars "BOT_MODE=webhook,WEBAPP_URL=$serviceUrl,DEBUG=false"
if ($LASTEXITCODE -ne 0) { throw "Could not enable Telegram webhook mode." }

Write-Host "DeutschIQ is deployed: $serviceUrl" -ForegroundColor Green
Write-Host "Health check: $serviceUrl/api/health"
Write-Host "Initialize the production database once; see docs/DEPLOYMENT.md."
