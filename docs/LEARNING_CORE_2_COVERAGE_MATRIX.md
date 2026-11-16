# Learning Core 2.0 — evidence coverage matrix (initial inventory)

Date: 2026-11-16. Scope: issue #253. **Partial** means a relevant test exists, not that the full end-to-end requirement has been verified.

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

## Next evidence gate

Build one executable B1 first-time reference journey spanning diagnostic, today recommendation, wrong answer, distinct repair, independent transfer, persistence/reload, delayed review and checkpoint. Then repeat for returning B1 and A1/A2/B2, and add RU/DE mobile/Telegram checks. Mark a row Verified only with linked test and CI evidence for its complete scope.
