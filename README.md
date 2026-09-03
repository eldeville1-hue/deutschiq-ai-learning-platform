# DeutschIQ

<p align="center">
  <img src="docs/screenshots/deutschiq-cover.png" alt="DeutschIQ — adaptive German learning inside Telegram">
</p>

<p align="center">
  <a href="https://deutschiq.onrender.com/"><strong>Live Web App</strong></a>
  ·
  <a href="https://t.me/DeutschIQ_bot"><strong>Open Telegram Bot</strong></a>
  ·
  <a href="docs/DEPLOYMENT.md"><strong>Deployment Guide</strong></a>
</p>

<p align="center">
  <img alt="CI" src="https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/actions/workflows/ci.yml/badge.svg">
  <img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white">
  <img alt="React TypeScript" src="https://img.shields.io/badge/React-TypeScript-3178C6?logo=react&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white">
</p>

## About

DeutschIQ is an AI-assisted Telegram Mini App for adaptive German learning. It combines a protected level diagnostic, a personalized 30-day curriculum, mastery-based exercises, spaced review, progress analytics, and an AI tutor in a mobile-first learning flow.

The public application runs as a Docker service on Render with a signed Telegram webhook and managed PostgreSQL on Neon.

> The free Render instance can take up to a minute to wake after inactivity.

## Product preview

<p align="center">
  <img src="docs/screenshots/01-home.png" width="230" alt="Personalized home screen">
  <img src="docs/screenshots/02-diagnostic.png" width="230" alt="Adaptive German diagnostic">
  <img src="docs/screenshots/03-lesson.png" width="230" alt="Interactive German lesson">
</p>

<p align="center">
  <img src="docs/screenshots/04-plan.png" width="230" alt="Personalized learning plan">
  <img src="docs/screenshots/05-analytics.png" width="230" alt="Knowledge analytics">
  <img src="docs/screenshots/06-ai-tutor.png" width="230" alt="AI German tutor">
</p>

<p align="center">
  <img src="docs/screenshots/07-profile.png" width="230" alt="Learner profile">
  <img src="docs/screenshots/09-lesson-listening.png" width="230" alt="Listening exercise">
  <img src="docs/screenshots/10-lesson-feedback.png" width="230" alt="Learning feedback">
</p>

## Key features

- Telegram-authenticated onboarding and returning-user flow
- Adaptive A1–B2 diagnostic without exposing answers to the client
- Personalized 30-day roadmap with 30 lessons and 90 exercises
- Mastery gates, retry logic, confidence tracking, and spaced review
- Grammar, vocabulary, reading, listening, and productive activities
- Server-side answer validation and structured feedback
- AI tutor with backend-managed history and daily limits
- Progress analytics, mistakes, XP, streaks, and achievements
- Russian and German interface
- Mobile Telegram WebView design with reduced-motion support
- Signed webhook for permanent cloud operation

## Architecture

```mermaid
flowchart TD
    T[Telegram user] --> W[React Mini App]
    T --> B[Aiogram webhook]
    W --> A[FastAPI API]
    B --> A
    A --> D[(Neon PostgreSQL)]
    A --> O[OpenAI API]
```

| Layer | Technology |
| --- | --- |
| Mini App | React, TypeScript, Vite, React Router |
| Backend | Python 3.12, FastAPI, SQLAlchemy, Pydantic |
| Telegram | aiogram 3, signed webhook, Web App authentication |
| Learning | mastery scoring, adaptive review, structured diagnostics |
| Database | PostgreSQL on Neon |
| AI | OpenAI API with deterministic fallback |
| Delivery | Docker, Render, GitHub Actions |

## Repository structure

```text
DeutschIQ/
├── backend/
│   ├── app/api/endpoints/   # FastAPI routes
│   ├── app/bot/             # Telegram bot and webhook
│   ├── app/models/          # SQLAlchemy models
│   ├── app/services/        # Learning and diagnostic logic
│   ├── tests/
│   ├── init_db.py
│   └── seed_30_day_plan.py
├── frontend/mini-app/       # React Telegram Mini App
├── docs/screenshots/        # Product screenshots
├── Dockerfile
└── docker-compose.yml
```

## Local development

Requirements: Python 3.11+, Node.js 20+, Docker Desktop, and an HTTPS tunnel for Telegram testing.

```powershell
Copy-Item .env.example .env
docker compose up -d postgres

cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
python seed_30_day_plan.py
python validate_content.py

cd ..\frontend\mini-app
npm install
npm run build
```

Run the API and polling bot in separate terminals:

```powershell
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

```powershell
cd backend
python -m app.bot.main
```

## Production

- Live application: [deutschiq.onrender.com](https://deutschiq.onrender.com/)
- Telegram entry point: [@DeutschIQ_bot](https://t.me/DeutschIQ_bot)
- Health endpoint: [`/api/health`](https://deutschiq.onrender.com/api/health)
- Runtime: Render Docker Web Service
- Database: Neon pooled PostgreSQL
- Bot transport: signed Telegram webhook

Render rebuilds the service from GitHub when the production branch changes. Production credentials are stored as hosting environment variables, never in the repository.

## Testing

```powershell
cd backend
python -m pytest tests -v

cd ..\frontend\mini-app
npm ci
npm run build
```

The same checks run in GitHub Actions.

## Security

- Telegram `initData` is validated server-side.
- Webhook requests use Telegram's secret-token header.
- Diagnostic and lesson answers remain server-side.
- Local `.env` files, tokens, API keys, database credentials, virtual environments, dependencies, and builds are excluded from Git.

If a credential is exposed, revoke it immediately and replace it in the hosting environment.

## Author

Built as a full-stack portfolio project by [eldeville1-hue](https://github.com/eldeville1-hue), with AI-assisted development used as part of the engineering workflow.
