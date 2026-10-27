# Learning Core 2.0 — A1–B2 evidence matrix

Status: **inventory only; not a passing E2E report**. Baseline: issue #253.

| Journey requirement | Existing automated evidence | A1 | A2 | B1 | B2 |
|---|---|---|---|---|---|
| Diagnostic → lesson attempt persisted | `backend/tests/test_diagnostic_learning_journey_sqlite.py` (A1 fixture) | partial | not verified | not verified | not verified |
| Mistake → supported retry → independent evidence | `backend/tests/test_adaptive_learner_journeys.py` (service-level) | partial | partial | partial | partial |
| Delayed retrieval → stability / scheduling | `backend/tests/test_adaptive_learner_journeys.py` (service-level) | partial | partial | partial | partial |
| Independent checkpoint evidence gate | `backend/tests/test_checkpoint_graduation.py` (service-level) | partial | partial | partial | partial |
| Guided → independent → transfer content structure | `backend/tests/test_learning_effectiveness_evidence.py` (synthetic fixtures) | partial | partial | partial | partial |
| Full real Telegram Mini App path on iPhone | no live interactive evidence gathered for this audit | not tested | not tested | not tested | not tested |
| Cross-account isolation and resume after restart in full journey | dedicated persistence tests exist; no complete cross-level end-to-end evidence reviewed | not verified | not verified | not verified | not verified |
| RU/DE instructions, keyboard and safe areas at 360×640 and 390×844 | dedicated checks must be reviewed and run in journey context | not verified | not verified | not verified | not verified |

**Legend:** partial = related lower-level coverage, **not** end-to-end verification; not verified = no sufficient evidence reviewed; not tested = test not performed in this audit.

## First reference scenario (B1)
1. New learner completes diagnostic; CEFR placement is clearly provisional.
2. Today recommends B1 skill based on evidence and prerequisites.
3. Learner makes an error; receives a specific explanation and a different repair item.
4. Supported correction does not grant independent mastery credit.
5. Learner answers a new-context transfer task independently; only verified evidence updates mastery.
6. Reload and reopen the lesson; previous attempts and recommendation persist.
7. Simulate delayed retrieval, both successful and failed; assert correct review rescheduling.
8. Checkpoint blocks weak dimension despite high average; failed learner receives a repair route.
9. Repeat with RU and DE, phone viewports, Telegram keyboard, and separate learner accounts.

## Exit gate
Do not call Learning Core 2.0 complete until every A1–B2 row has linked passing automated test evidence and representative manual linguistic/phone review. A passing smoke test is not proof of learning effectiveness.

## Next implementation
Extend existing tests rather than create competing evaluation engines. First automate the B1 reference journey using production endpoints and persisted state; then parameterize A1, A2 and B2. Record failures before proposing a shared renderer refactor. No monetization or redesign in this workstream.
