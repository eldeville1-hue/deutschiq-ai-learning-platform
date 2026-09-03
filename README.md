# DeutschIQ

## v14 Cloud Webhook

DeutschIQ can now run independently of a developer PC and ngrok. Production uses a signed Telegram webhook inside the FastAPI service, while local development keeps the existing polling workflow. The repository includes a multi-stage Docker image, Cloud Run deployment script, secret-safe configuration, health reporting, and GitHub Actions CI.

- [Permanent deployment guide](docs/DEPLOYMENT.md)
- `Dockerfile` builds the React Mini App and Python API into one container.
- `DEPLOY-CLOUD-RUN.ps1` deploys from Windows without committing credentials.
- Telegram webhook requests and scheduled reminder calls use separate secrets.
- Generated environments, builds, caches and local `.env` files are excluded from Git.

<!-- deutschiq-screenshots -->
## Product Preview

![DeutschIQ вЂ” adaptive German learning inside Telegram](docs/screenshots/deutschiq-cover.png)

<p align="center">
  <img src="docs/screenshots/01-home.png" width="230" alt="DeutschIQ personalized home screen">
  <img src="docs/screenshots/02-diagnostic.png" width="230" alt="DeutschIQ adaptive diagnostic">
  <img src="docs/screenshots/03-lesson.png" width="230" alt="DeutschIQ interactive lesson">
</p>

<p align="center">
  <img src="docs/screenshots/04-plan.png" width="230" alt="DeutschIQ personalized learning plan">
  <img src="docs/screenshots/05-analytics.png" width="230" alt="DeutschIQ mastery analytics">
  <img src="docs/screenshots/06-ai-tutor.png" width="230" alt="DeutschIQ AI tutor">
</p>

<p align="center">
  <img src="docs/screenshots/07-profile.png" width="230" alt="DeutschIQ learner profile">
</p>

The interface runs as a Telegram Mini App and is optimized for mobile WebView environments. Screenshots show the actual application running inside Telegram on iOS.



## v13 Precision Design

This release replaces the previous page compositions instead of applying another cosmetic layer. Home is a learning command center, Analysis is a knowledge instrument, Profile is an identity sheet, Plan is a route map, Tutor is a conversation canvas, and Diagnostic/Lesson remain distraction-free. The serif display face is removed in favor of a bundled system sans-serif stack that renders reliably inside Telegram on Windows, iOS and Android.

## v12 Obsidian Editorial

Every Mini App surface now has its own visual role inside one detailed design system: cinematic onboarding, an action-first dashboard cover, instrument-like analytics, a vertical learning route, a true messenger tutor, quiet account settings, fullscreen diagnostic and lesson focus modes, and a celebratory result reveal. The redesign adds complete dark/light tokens, safe-area handling, keyboard focus, small-screen tuning, staged motion and reduced-motion behavior without changing the v11 learning engine.

## v11 Curriculum Core

The 30-day path now gives every lesson its own communicative goal, authentic error contrast and production target. Free German sentences receive structured AI feedback when OpenAI is available, with a deterministic offline fallback. Independent retrieval is used for scheduled review, curriculum validation checks all learning stages, and the bot prevents duplicate local polling processes.

## v10 Learning Content Quality

The complete 30-day roadmap is upgraded to a consistent evidence-informed sequence: explicit goal, concise rule, German listening at normal/slow speed, correct-vs-common-error contrast, retrieval pause, guided practice, independent word ordering and a productive sentence task. Content is normalized at the API boundary and validated before installation.

## v9 Product Intelligence

Every lesson now has a server-owned learning session. Attempts, score, pass/fail, XP and analytics are isolated to that session, preventing historical answers from corrupting a new result. The learning algorithm is extracted into tested pure functions for session scoring, confidence-weighted mastery and expanding review intervals.

## v8 Adaptive Learning

Lessons now use mastery gates rather than completion-by-click. Wrong answers are retried once inside the same session, the backend calculates accuracy from actual attempts, lessons require 70% to pass, XP is awarded only after demonstrated learning, and the result screen explains score, topic mastery and the next action.

## v7 Better Learning

This cumulative version adds a retention-first learning engine: every exercise attempt records correctness, confidence and response time; topic mastery updates after each answer; due reviews are scheduled adaptively; the 30-day plan prioritizes weak and overdue knowledge; review requires active recall; and Analytics separates retained mastery from simple lesson completion.

## v6 Strong Design

This cumulative build introduces the Editorial Learning OS design direction while preserving Telegram authentication, protected diagnostics, backend answer checks, personalized planning, tutor history, mistakes and review flows.

- Dashboard: action-first lesson poster
- Analytics: high-contrast knowledge instrument
- Plan: vertical learning route
- Tutor: focused messenger layout
- Profile: quiet account ledger
- Diagnostic and Lesson: fullscreen focus modes
- Floating navigation dock, responsive safe areas and reduced-motion support

## UX v2.1

- Backend-driven bootstrap through `GET /api/user/state/{telegram_id}`.
- Separate onboarding and returning-user intro screens.
- Diagnostic route guard; retakes require `?retake=true` and are available only from Profile.
- Backend-persisted RU/DE interface language.
- Semantic topic labels hide internal slugs such as `haben_conjugation`.
- Compact Overview, Analysis, Learning Plan, Tutor and Profile screens.
- Step-based mobile lesson flow: rule, example, three exercises, result.
- Shared visual tokens, reusable navigation styles and unique functional icons.

## UI/UX v3

- Permanent Telegram chat menu button opens the Mini App like BotFather's OPEN button.
- Bot messages, progress, keyboard and help follow the user's RU/DE preference.
- Diagnostic questions no longer reveal correctness before the final result.
- Lesson answer comparison ignores trailing punctuation, extra spaces and letter case.
- Retaking the diagnostic requires explicit confirmation from Profile.
- Diagnostic results are compact, localized and show semantic topic labels.
- Dashboard weaknesses use readable rows instead of clipped horizontal tags.
- Unified one-shot motion system with reduced-motion accessibility support.

DeutschIQ is a Telegram Mini App for personalized German learning. It combines an adaptive diagnostic test, skill analytics, a 30-day curriculum, interactive exercises, an AI tutor, gamification, referrals, and native Telegram Stars payments.

## Product highlights

- Adaptive A1вЂ“B2 diagnostic with immediate explanations
- Personalized grammar and vocabulary skill analysis
- 30-day roadmap with 30 lessons and 90 starter exercises
- AI tutor with daily free limits and session history
- XP, streaks, achievements, referrals, and Pro access
- Russian and German interface
- Telegram-native navigation, sharing, reminders, and payments

## Architecture

```mermaid
flowchart LR
    U[Telegram user] --> B[Aiogram bot]
    U --> M[React Mini App]
    B --> A[FastAPI]
    M --> A
    A --> P[(PostgreSQL)]
    A --> O[OpenAI API]
```

## Technology

| Layer | Stack |
| --- | --- |
| Mini App | React, TypeScript, Vite, React Router |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Telegram bot | aiogram 3 |
| Data | PostgreSQL, Redis-ready configuration |
| AI | OpenAI-compatible tutor service |
| Payments | Telegram Stars invoices |

## Project structure

```text
DeutschIQ/
в”њв”Ђв”Ђ backend/
в”‚   в”њв”Ђв”Ђ app/api/endpoints/   # FastAPI routes
в”‚   в”њв”Ђв”Ђ app/bot/             # Telegram bot and reminders
в”‚   в”њв”Ђв”Ђ app/models/          # SQLAlchemy models
в”‚   в”њв”Ђв”Ђ app/services/        # diagnostics and learning logic
в”‚   в”њв”Ђв”Ђ init_db.py
в”‚   в””в”Ђв”Ђ seed_30_day_plan.py
в”њв”Ђв”Ђ frontend/mini-app/       # React Telegram Mini App
в””в”Ђв”Ђ docker-compose.yml       # PostgreSQL and Redis
```

## Local setup

Requirements: Python 3.11+, Node.js 20+, Docker Desktop, and an HTTPS tunnel for Telegram development.

Create a root `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql://user:postgres@localhost:5432/deutschiq
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
WEBAPP_URL=https://your-public-host.example
SECRET_KEY=replace-with-a-random-secret
```

Start PostgreSQL and initialize the content:

```powershell
docker compose up -d postgres
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
python seed_30_day_plan.py
```

Build and run the Mini App:

```powershell
cd ..\frontend\mini-app
npm install
npm run build
cd ..\..\backend
uvicorn app.main:app --reload
```

Run the bot in a second terminal:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m app.bot.main
```

## Main user flow

1. Open DeutschIQ from the Telegram bot.
2. Complete the diagnostic test.
3. Review the level, mistakes, and skill analysis.
4. Follow the personalized 30-day plan.
5. Use the AI tutor for explanations and extra practice.

## Production checklist

- Replace the development tunnel with permanent HTTPS hosting.
- Configure production PostgreSQL and secrets.
- Add payment event reconciliation and refund handling.
- Add monitoring, analytics, privacy policy, terms, and German Impressum.
- Run API, payment, and end-to-end tests before accepting real payments.

## Security

Never commit `.env`, bot tokens, API keys, production database credentials, user data, or generated virtual environments.
