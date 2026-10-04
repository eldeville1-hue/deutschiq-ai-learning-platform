# DeutschIQ technical testing report

## Automated coverage

- Backend unit and integration tests
- Database migration-head validation and Python compilation
- React production build, ESLint and bundle budget
- Mobile Playwright journeys in Chromium and WebKit
- New learner, returning learner, diagnostic, lesson, review, recovery, beta access and commercial-preview flows
- Production API, database, frontend shell and immutable asset-cache smoke checks
- Freshness-limited Telegram Mini App signatures, tamper rejection and future-date rejection
- Security headers, restricted CORS methods/headers and HTTPS HSTS
- A launch-readiness curriculum audit covering 80 lessons, 400 exercises and RU/DE/EN copy
- Read-only bounded concurrency smoke for health, version and frontend endpoints
- Production dependency audit; high and moderate frontend advisories block release

## Release protocol

Every production change follows the same sequence:

1. Run backend and frontend checks.
2. Push the reviewed commit to `main`.
3. Require the GitHub Actions backend, frontend and mobile E2E jobs to pass.
4. Wait for the existing Render service to report `live`.
5. Run `python backend/scripts/smoke_test.py https://deutschiq.onrender.com`.
6. Run `python backend/scripts/load_smoke.py https://deutschiq.onrender.com`.
7. Scan deployment logs for build/application errors and production requests for HTTP 5xx responses.

## Database recovery gate

Before paid launch, create a Neon branch from the latest production restore point, connect it as an isolated restore target, apply `alembic upgrade head`, and run the production smoke checks against a temporary service wired only to that branch. Never test restoration by overwriting the production branch. Record the restore-point time, temporary branch, migration head and verification result, then delete the isolated branch after the evidence is retained.

The closed beta remains payment-disabled until this isolated restore drill and the seller/legal checklist are complete.

## Scope boundary

Automation can verify software behavior across scripted learner personas, devices, network recovery and failure states. It cannot manufacture independent human comprehension, usefulness or willingness-to-pay evidence; those signals are collected during the free soft launch.
