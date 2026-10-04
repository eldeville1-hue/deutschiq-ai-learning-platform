# DeutschIQ — portfolio case study

## Problem

German learners often receive generic exercises without a clear connection between diagnosis, daily practice, mistakes and later recall. Telegram learners also need a fast mobile flow that survives interruptions and unreliable connections.

## Product

DeutschIQ is a Telegram Mini App for adaptive German learning from A1 to B2. A server-validated placement test estimates the starting level, creates a personalized route and connects review, instruction and active transfer in a daily session.

## Engineering contribution

- React, TypeScript and Vite mobile interface
- FastAPI and SQLAlchemy backend with PostgreSQL
- Signed Telegram authentication and webhook delivery
- Server-side diagnostic and exercise validation
- Retention-aware mastery, spaced review and misconception feedback
- AI tutor with recent learning context and deterministic fallback
- Privacy controls, multilingual UI and accessible reduced-motion behavior
- First-party analytics, contextual feedback and protected owner Quality Center
- Docker deployment on Render with migrations, health checks and GitHub Actions

## Product decisions

The paid launch is intentionally disabled during validation. Learners receive free A1–B2 and tutor access, can preview the future 700-Star offer, and provide structured feedback. The owner dashboard makes the launch decision auditable through explicit evidence thresholds rather than vanity traffic.

## Verification

The project is tested with backend automation, production frontend builds, linting, bundle limits, mobile Playwright journeys in Chromium and WebKit, database migration checks, production smoke tests and post-deploy log scans.
