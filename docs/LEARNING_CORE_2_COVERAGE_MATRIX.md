# Learning Core 2.0 — evidence coverage matrix (initial inventory)

Date: 2026-11-18 (updated evidence inventory). Scope: issue #253. **Partial** means a relevant test exists, not that the full end-to-end requirement has been verified.

| Acceptance scenario | Evidence inspected | Status | Missing proof |
| --- | --- | --- | --- |
| 1. Telegram onboarding → diagnostic → provisional placement | `frontend/mini-app/tests/e2e/reliability.spec.ts`; `backend/tests/test_diagnostic_learning_journey_sqlite.py`; `backend/tests/test_adaptive_learner_journeys.py` | Partial | Four levels × first-time/returning; real Telegram authentication |
| 2. Today recommendation → lesson goal/explanation → guided answer | `test_adaptive_learner_journeys.py`; `reliability.spec.ts` | Partial | Continuous per-level learner flow and content review |
| 3. Wrong answer → specific diagnosis → changed repair → independent transfer | `test_b1_persisted_journey.py`; `test_learning_effectiveness_evidence.py` | Partial | Distinct repair and transfer demonstrated at each level |
| 4. Separate score, mastery, retention, completion, CEFR estimate | `test_adaptive_learner_journeys.py`; `test_checkpoint_graduation.py` | Partial | UI and persistence evidence for each distinct metric |
| 5. Exit/reload/resume and no account bleed | `test_b1_persisted_journey.py`; `test_diagnostic_learning_journey_sqlite.py` | Partial | Mobile kill/reload and cross-account E2E for all levels |
| 6. Delayed correct/incorrect review adjusts stability/schedule | `test_adaptive_learner_journeys.py`; `test_spaced_review.py`; `test_b1_persisted_journey.py` | Partial | Multi-day persisted UI learner journeys |
| 7. Independent checkpoint gate; failure repairs, pass advances | `test_checkpoint_graduation.py`; `test_adaptive_learner_journeys.py` | Partial | Per-level E2E checkpoint and remediation |
| 8. RU/DE, 360×640 / 390×844, iPhone Telegram safe area | `reliability.spec.ts`; mobile CI | Partial | Explicit language/viewport/keyboard/safe-area assertions |

## Evidence limitations

- No row is fully verified from this inventory alone. Service tests do not prove complete learning journeys or educational effectiveness.
- `test_learning_effectiveness_evidence.py` checks that missing independent/transfer stages are reported; it does not certify the whole curriculum.
- `test_b1_persisted_journey.py` explicitly identifies itself as an API/service integration test, **not** a Telegram browser E2E test.
- Technical release baseline `d0454cd16454668a04a1ff33846fa9027acde2e0`: CI 43939304065, v88 Release Evidence 43940270499, Production smoke 43940345420 all passed; Render live. This does not establish CEFR or pedagogical validity.

## Evidence added since the initial inventory

These changes strengthen individual edge-case assertions, **not** full A1–B2 end-to-end coverage. Every acceptance row above remains **Partial**.

| Evidence | What it demonstrates | What it does not demonstrate |
| --- | --- | --- |
| [#315](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/315) | Persisted B1 wrong answer → guided retry → resume → due review → independent retrieval; checkpoint refuses insufficient independent evidence; account isolation | Browser-level full first-time B1 journey |
| [#317](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/317)–[#325](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/325) | Mobile Playwright B1 assessment/reload, guided repair, independent attempt, due review, duplicate-click prevention and HTTP 409 conflict recovery | A1/A2/B2, actual Telegram webview/safe-area on physical iPhone |
| [#326](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/326) | Successful B1 review replay returns HTTP 409 without duplicate mastery credit | Simultaneous HTTP requests or all review types |
| [#327](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/327) | Real PostgreSQL learner-row lock serialization with NOWAIT | Full endpoint behavior under concurrent writes |
| [#328](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/328) | Two overlapping `check_answer` function calls using independent PostgreSQL sessions: one correct result, one HTTP 409, one credited attempt | Real HTTP transport concurrency, interrupted-request recovery |
| [#329](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/329)–[#330](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/330) | Telegram initData duplicate-key rejection including percent-encoded aliases and blank values | Real Telegram onboarding on all target devices |

| [#332](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/332)–[#334](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/334) | Persisted B1 wrong-answer resume, completed-answer replay protection, and delayed review across fresh database sessions | Browser-level continuity, multi-day real-user retention, or other CEFR levels |
| [#335](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/335)–[#337](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/337) | First-time mobile B1 diagnostic placement → dashboard → recommended lesson → practice → saved 82% assessment visible after reload at 360×640 | Wrong-answer repair and delayed review in that same continuous browser journey; A1/A2/B2 |
| [#338](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/338)–[#339](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/339) | Fresh-database-session account isolation and lost-response server-committed answer recovery without duplicate mastery | Physical Telegram WebView or cross-account browser E2E |
| [#340](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/340)–[#343](https://github.com/eldeville1-hue/deutschiq-ai-learning-platform/pull/343) | Mobile Playwright lost-answer-response recovery, both committed and uncommitted server outcomes, and reload behavior without automatic duplicate grading | Full B1 first-time learner journey or proof of physical iPhone process-kill persistence |

The #328 exact release SHA `e18436348be2d3bf6f8408db459501a0ad513fae` had post-merge CI, release evidence, production smoke and Render Live confirmed. The #329 exact release SHA `7ff9ade45fd774dacee44584dc664ca4098383dd` had the same gates confirmed. These are technical release checks, not language-learning outcome evidence.

## Next evidence gate

Build one executable B1 first-time reference journey spanning diagnostic, today recommendation, wrong answer, distinct repair, independent transfer, persistence/reload, delayed review and checkpoint. Then repeat for returning B1 and A1/A2/B2, and add RU/DE mobile/Telegram checks. Mark a row Verified only with linked test and CI evidence for its complete scope.
