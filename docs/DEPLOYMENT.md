# Deploy DeutschIQ on Render + Neon

The production application runs as one Docker web service. Docker builds the React Mini App, serves it through FastAPI, applies Alembic migrations, and registers the Telegram webhook. Your computer and ngrok are not involved after deployment.

## Architecture

- **Render Web Service:** FastAPI, compiled React frontend, Telegram webhook
- **Neon:** persistent PostgreSQL database
- **Telegram:** Mini App entry point and signed user identity
- **OpenAI:** optional tutor responses; deterministic fallback remains available

## Required Render environment variables

Add these under **Render > deutschiq > Environment**. Never paste them into GitHub.

| Key | Value |
|---|---|
| `BOT_TOKEN` | Fresh token from BotFather |
| `DATABASE_URL` | Neon pooled PostgreSQL URL with `sslmode=require` |
| `OPENAI_API_KEY` | Fresh OpenAI key, or leave empty for fallback mode |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `BOT_MODE` | `webhook` |
| `WEBAPP_URL` | `https://deutschiq.onrender.com` |
| `TELEGRAM_WEBHOOK_PATH` | `/api/telegram/webhook` |
| `SECRET_KEY` | Long random value |
| `TELEGRAM_WEBHOOK_SECRET` | 16-256 letters, digits, `_` or `-` |
| `TASK_SECRET` | Random value of at least 24 characters |
| `DEBUG` | `false` |

The included `render.yaml` documents the service settings. Existing Render services can continue using Dashboard-managed variables.

## Deploy

1. Push or merge a commit into GitHub `main`.
2. Render builds the Dockerfile automatically.
3. `backend/start.sh` runs `alembic upgrade head` before starting Uvicorn.
4. The API startup registers the permanent Telegram webhook and Mini App menu button.

No `init_db.py`, seed script, Render shell, Google Cloud CLI, or local ngrok tunnel is required for normal updates. Content seeding remains a deliberate administrative operation and must not run on every restart.

## Verify after deployment

- `https://deutschiq.onrender.com/api/health/live` — process is running
- `https://deutschiq.onrender.com/api/health` — database and migration state
- `https://deutschiq.onrender.com/privacy` — public legal route

Or run from the repository root:

```powershell
python backend/scripts/smoke_test.py https://deutschiq.onrender.com
```

Then send `/start` to [@DeutschIQ_bot](https://t.me/DeutschIQ_bot) and complete one real learning flow.

## Local development

Keep your local `.env` untracked and use `BOT_MODE=polling`. From `backend`:

```powershell
.\venv\Scripts\Activate.ps1
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Run `python -m app.bot.main` in a second terminal. Webhook and polling must not run simultaneously for the same bot.

## Rollback

If a new Render deployment fails, Render continues serving the previous successful image. Fix the commit and redeploy. The v15 baseline migration has a deliberately non-destructive downgrade because it adopts databases created by earlier DeutschIQ versions.

## Free-tier limitation

Render's free service can sleep after inactivity, so the first bot launch may be slow. A paid always-on instance reduces cold starts; it is not required for a portfolio demonstration.
