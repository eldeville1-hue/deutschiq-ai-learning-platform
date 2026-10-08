# DeutschIQ v88 — Independent linguistic review protocol

**Status: NOT REVIEWED. Production v87 stays deployed.**

## Prepare the blind packet
From the backend directory:

```bash
python -m tests.review_evaluation_benchmark export-curated tests/fixtures/evaluation_v88_curated_review_packet.csv
```

The curated packet has 480 development examples (120 per A1, A2, B1 and B2). They are **not an independent holdout** and cannot alone establish generalization or release readiness. For independent release validation, collect at least 100 genuinely independent, separately sourced and reviewed examples per CEFR level, avoid near duplicates and leakage, and keep a locked holdout.

## Reviewer instructions
Assign qualified German-language reviewers who did not write the items or evaluator. Distribute the CSV **without predictions, provisional labels, or expected error categories**. Reviewers must assess the prompt and learner answer, including accepted valid alternatives, and fill in `decision` (correct/incorrect/uncertain), `error_types` (semicolon-separated when incorrect), `reviewer` and `notes`. Disagreements must be adjudicated independently; retain provenance and original decisions. A second reviewer should independently inspect disputed and critical false-acceptance cases.

Import after review:

```bash
python -m tests.review_evaluation_benchmark import-curated completed_reviews.csv tests/fixtures/evaluation_v88_curated_reviewed.jsonl
```

Import only records reviewer claims as **pending_independence_verification**; it does not grant independent-review status automatically. Verify reviewer identity, independence, provenance, holdout separation and disagreement resolution before computing release metrics.

## Release gates
- >=100 independently reviewed examples **per CEFR level** from a valid holdout
- Per-level accuracy >=95%, definitive coverage >=95%
- Diagnosis precision and recall >=90%; zero critical false acceptances
- Deterministic evaluation p95 <200 ms; AI-assisted p95 <2.5 s; failure rate <1%
- Backend, frontend and mobile E2E green; no XP/mastery for uncertain answers
- Human signoff, deployment smoke test and rollback plan

A green development benchmark or CI does **not** satisfy these gates. Do not deploy v88 until all are met.

## Targeted uncertainty review (development triage only)

The release-evidence workflow exports `uncertain_review_v88.csv` and `uncertain_review_manifest_v88.json` from the current evaluator. The CSV intentionally hides evaluator predictions and provisional labels. A reviewer may complete the decision, error_types, reviewer and notes columns.

After receiving a completed packet, from `backend/` run:

```bash
python -m tests.import_uncertain_review_v88 completed_uncertain.csv reviewed_uncertain.jsonl uncertain_review_manifest_v88.json
```

The importer checks that the manifest identifies the exact current uncertain cases and that CSV content has not been changed. Imported decisions remain `pending_independence_verification` and **cannot** be counted as an independent holdout or release signoff. Re-export if the evaluator or development set changes. Never auto-apply reviewer corrections to the production evaluator.

## Compare completed reviews with evaluator judgments

After importing the targeted packet, run from `backend/`:

```bash
python -m tests.triage_review_disagreements_v88 reviewed_uncertain.jsonl review_disagreements_v88.json
```

The report prioritizes potential false acceptances, then false rejections, then correct answers left unverified. It also tracks incorrect answers left unverified. Every finding remains provisional until reviewer provenance and independence are verified. Do not interpret these development comparisons as independent accuracy, do not auto-update the evaluator, and do not unblock v88 based on this report.
