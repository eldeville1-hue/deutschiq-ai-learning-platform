# v88 — Independent A1–B2 Holdout: Reviewer Handoff

**Status:** Collection and external human review required. This document is a protocol, **not** evidence that any review has occurred. v88 remains blocked.

## Goal

Recruit independent qualified German-language reviewers to assess **at least 100 distinct, independently authored and reviewed cases per level** (A1, A2, B1, B2), with a total of at least 400. Do not reuse the 480 curated development cases, their paraphrases, or any synthetic benchmark fixtures. Reviewers must not see DeutschIQ predictions or suggested diagnoses before committing their judgments.

## Roles and independence

1. A coordinator collects externally authored prompts, reference answers, learner responses, task type, CEFR level, and source attribution. Confirm lawful permission to use the material; anonymize learner information.
2. An independent reviewer (ideally a German teacher or qualified CEFR assessor) judges whether the learner answer is correct, incorrect, or genuinely ambiguous. For incorrect answers, record linguistic error categories; for uncertain answers, explain why. Record reviewer identity or an auditable pseudonymous identifier, review date/time, and protocol version.
3. A separate coordinator verifies that the reviewer did not generate or edit the evaluated examples, did not see the model's output, and that the sample was not derived from development data. Preserve external attestations securely; self-reported JSON flags are **not** independent proof.
4. Resolve disagreements with a second blind reviewer and an adjudicator, preserving original decisions. Do not rewrite outcomes to improve metrics.

## Required data contract

Save UTF-8 JSON Lines (one JSON object per line) as `external_holdout_v88.jsonl`. Each case needs:

- `id`: unique stable identifier, e.g. `external-A1-001`.
- `cefr`: `A1`, `A2`, `B1`, or `B2`.
- `objective`: task's learning objective.
- `exercise`: object with `type`, `question`, `answer`; add `accepted_answers` only if independently justified.
- `learner_answer`: response to evaluate.
- `source`: externally documented origin; never claim independent sourcing without verification.
- `split`: `holdout`.
- `human_review`: initially `{"status":"pending"}`. After independent review and provenance checks, include `status="approved"`, `decision`, `reviewer`, `reviewed_at` (ISO 8601 with timezone), `protocol_version`, `blind_to_prediction=true`, `independent_of_generation=true`, and `error_types` for incorrect answers or `notes` for uncertain answers.

**Schema illustration only — fabricated example, not holdout evidence:**

```json
{"id":"EXAMPLE-NOT-FOR-BENCHMARK","cefr":"A2","objective":"Dative after mit","exercise":{"type":"translation","question":"Translate: I travel with my sister.","answer":"Ich fahre mit meiner Schwester."},"learner_answer":"Ich fahre mit meine Schwester.","source":"EXAMPLE_ONLY_NOT_VERIFIED","split":"holdout","human_review":{"status":"pending"}}
```

Never import the illustration as a real holdout row. Do not commit personally identifiable student work or sensitive reviewer attestations to a public repository.

## Collection checklist

- [ ] External origin and permitted use documented for every case
- [ ] 100+ distinct cases in each A1, A2, B1, B2 group
- [ ] Variety across exercise families and correct, incorrect, ambiguous responses
- [ ] Blind human decisions and diagnoses collected
- [ ] Independence and reviewer provenance verified outside the JSON
- [ ] Duplicate/near-duplicate and development leakage checks passed
- [ ] All disagreements adjudicated without exposing predictions prematurely
- [ ] Benchmark run and failure gates inspected; no threshold exemptions
- [ ] Independent release signoff, real AI latency evidence, E2E, and production smoke gates separately satisfied

## Run the validator

From the `backend/` directory:

```bash
python -m tests.holdout_pipeline_v88 validate /secure/path/external_holdout_v88.jsonl
```

Exit code `2` and `release_gate: blocked` are expected while data is pending, incomplete, or before release signoff. An ingestion pass or passing GitHub CI **does not** authorize production deployment.

**Important:** The existing validator checks field-level provenance claims but cannot authenticate external independence. The coordinator must verify that independently and retain the evidence.
