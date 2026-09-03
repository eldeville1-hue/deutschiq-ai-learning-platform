# Permanent cloud deployment

DeutschIQ supports two bot transports:

- `BOT_MODE=polling` for local development. Run the API and `python -m app.bot.main` as two processes.
- `BOT_MODE=webhook` for production. FastAPI receives signed Telegram updates, so no permanent polling process or ngrok tunnel is required.

## Recommended low-cost stack

Use Google Cloud Run for the container and a managed PostgreSQL provider with a free tier (for example Neon or Supabase). Cloud Run can scale to zero, so the first request after inactivity can be slower. No provider can honestly guarantee a permanently warm, production-grade service at zero cost.

## Prerequisites

1. A Google Cloud project with billing enabled.
2. `gcloud` installed and authenticated.
3. An external PostgreSQL connection string that accepts connections from Cloud Run.
4. A fresh Telegram token from BotFather and, optionally, an OpenAI API key.

Never commit these values. The deploy script stores them in Google Secret Manager.

## Deploy from Windows PowerShell

From the project root:

```powershell
$env:BOT_TOKEN = "NEW_TOKEN_FROM_BOTFATHER"
$env:DATABASE_URL = "postgresql://USER:PASSWORD@HOST/DB?sslmode=require"
$env:OPENAI_API_KEY = "OPTIONAL_OPENAI_KEY"

.\DEPLOY-CLOUD-RUN.ps1 -ProjectId "your-google-project-id"
```

The script builds the Docker image through Cloud Run source deployment, stores secrets, discovers the permanent HTTPS URL, and switches the service to signed webhook mode.

After the first deployment, initialize the database once from a trusted machine using the same production `DATABASE_URL`:

```powershell
cd backend
python init_db.py
python seed_30_day_plan.py
python validate_content.py
```

## Daily reminders

The production API exposes `POST /api/tasks/daily-reminders`. It requires the `X-Task-Secret` header. Trigger it once per day with Cloud Scheduler or another scheduler. Never expose `TASK_SECRET` in source code.

## Verification

```powershell
Invoke-RestMethod "https://YOUR_SERVICE_URL/api/health"
```

Expected fields include `status`, `version`, `database`, and `bot_mode: webhook`.

Then open the bot in Telegram, send `/start`, and launch the Mini App. The production URL no longer depends on a running PC or ngrok.

## Local development remains available

Set `BOT_MODE=polling` in `.env`, then run:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
python -m app.bot.main
```

Webhook and polling must not run for the same Telegram bot at the same time.
