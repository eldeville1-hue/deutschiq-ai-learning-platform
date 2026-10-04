# DeutschIQ technical testing report

## Automated coverage

- Backend unit and integration tests
- Database migration-head validation and Python compilation
- React production build, ESLint and bundle budget
- Mobile Playwright journeys in Chromium and WebKit
- New learner, returning learner, diagnostic, lesson, review, recovery, beta access and commercial-preview flows
- Production API, database, frontend shell and immutable asset-cache smoke checks

## Release protocol

Every production change follows the same sequence:

1. Run backend and frontend checks.
2. Push the reviewed commit to `main`.
3. Require the GitHub Actions backend, frontend and mobile E2E jobs to pass.
4. Wait for the existing Render service to report `live`.
5. Run `python backend/scripts/smoke_test.py https://deutschiq.onrender.com`.
6. Scan deployment logs for build/application errors and production requests for HTTP 5xx responses.

## Scope boundary

Automation can verify software behavior across scripted learner personas, devices, network recovery and failure states. It cannot manufacture independent human comprehension, usefulness or willingness-to-pay evidence; those signals are collected during the free soft launch.
