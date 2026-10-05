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

Completed on 2026-10-05 with the temporary Neon branch `restore-drill-2026-10-05`, created from `production`. Read-only verification confirmed migration head `20261003_0011` and restored learner, lesson, session, event, diagnostic and exercise-attempt records. Production was not modified, and the temporary branch was deleted after verification.

The closed beta remains payment-disabled until the seller/legal checklist and genuine learner-evidence gate are complete.

## Final v79 acceptance audit — 2026-10-05

- Production release: `79.0.0` / `beta-evidence-v20` / commit `d6e7b7a471b7`
- Local backend: 128/128 tests passed
- Curriculum gate: 80 lessons, 400 exercises and RU/DE/EN copy passed with no publication blockers
- Frontend: production build, ESLint, bundle budget and production dependency audit passed; 0 known production vulnerabilities
- GitHub Actions run `37229698240`: backend, frontend and all 62 Chromium/WebKit mobile journeys passed
- Scheduled production smoke run `37268268814`: passed on the deployed v79 commit
- Live verification: API version, database, migration head, frontend shell and versioned assets returned successfully
- Render deployment: `live`; recent error/critical logs: 0; recent HTTP 5xx responses: 0
- Bounded production load: 60/60 HTTP 200 responses and 0 request errors; p50 6.41 seconds, p95 9.30 seconds and maximum 9.65 seconds, failing the 2.5-second paid-launch latency gate
- Payments remained disabled and no production learner evidence was fabricated during the audit

The remaining infrastructure limitation is the free Render instance's cold start and concurrent-request queueing. In this audit, the first command-line request completed in about 24 seconds after an earlier 60-second timeout, and the warm bounded load probe remained above the release latency threshold. This is a hosting-capacity constraint, not an application assertion failure, and an always-on instance remains required before paid launch.

## Scope boundary

Automation can verify software behavior across scripted learner personas, devices, network recovery and failure states. It cannot manufacture independent human comprehension, usefulness or willingness-to-pay evidence; those signals are collected during the free soft launch.
