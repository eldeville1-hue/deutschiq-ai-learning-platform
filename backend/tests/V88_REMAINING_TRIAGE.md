# v88 — remaining development triage (2026-10-08)

Source: successful CI run 37805256390; 480 curated unreviewed cases; 248 backend tests passed. The audit reports 4 potential misdiagnoses and 160 intentionally deferred incorrect responses. These are **provisional** labels, not independently reviewed truth.

## Four flagged cases

1. `repair-A1-03` — `Ich möchte einen Wasser, bitte.` → `Ich möchte Wasser, bitte.` — provisional category: article; predicted: answer_mismatch. This involves removing a word; avoid inventing a one-token aligned diagnosis.
2. `repair-A1-13` — `Ich suche meinen Schlüssel.` → `Ich suche meine Schlüssel.` — provisional category: meaning; predicted: conjugation. Singular/plural number and determiner inflection change meaning; the classifier should not automatically assume a verb-conjugation error.
3. `repair-B1-07` — `Sie hat vor, sich für die Stelle bewerben.` → `Sie hat vor, sich um die Stelle zu bewerben.` — provisional category: infinitive; predicted: missing_words. This is a compound correction (preposition plus missing `zu`), so a single category is incomplete.
4. `repair-B2-16` — `Das Problem sollte von mehrere Perspektiven betrachtet werden.` → `Das Problem sollte aus mehreren Perspektiven betrachtet werden.` — provisional category: case; predicted: preposition + vocabulary. This changes both the preposition and adjective ending. Do not force a single label.

## Decision

Do not overfit the deterministic evaluator to the provisional single-label fixture. Keep all four cases in independent adjudication. The reviewer should be allowed to assign multiple error types, revise an ambiguous provisional label, and document whether a single error label is inappropriate.

## Blind packet

`cd backend && python -m tests.review_evaluation_benchmark export-curated`

This exports 480 blind development cases (120 per CEFR level), with predictions and provisional labels excluded. The CSV is a review aid, **not an independent holdout**. Follow `V88_LINGUISTIC_REVIEW_PROTOCOL.md` for reviewer independence, separately sourced holdout and release gates. Production stays on v87 until validation passes.
