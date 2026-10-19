import { test, expect } from '@playwright/test';
import { getB2WritingReviewHints } from '../../src/learning/b2WritingReview';

test('B2 argument hints recognize alternative reasoning and evidence', () => {
  const complete = 'Aufgrund der besseren Sicherheit ist der Ausbau sinnvoll. Konkret profitieren Schulkinder davon, weil sie sicherer zur Schule fahren können.';
  expect(getB2WritingReviewHints('argument_structure-dialogue', complete, 'en')).toEqual([expect.stringContaining('actually support your reason')]);
  const incomplete = getB2WritingReviewHints('argument_structure-dialogue', 'Ich bin für Radwege.', 'en');
  expect(incomplete).toHaveLength(1);
  expect(incomplete[0]).toContain('state your position');
  const expanded = 'Ich unterstütze Radwege in der Stadt, weil sie die Sicherheit für alle verbessern. Deshalb sollten wir diese Lösung wählen.';
  expect(getB2WritingReviewHints('argument_structure-dialogue', expanded, 'en')).toHaveLength(1);

  expect(getB2WritingReviewHints('argument_structure-dialogue', 'Ich bin für mehr Radwege in der Stadt, denn das ist für viele Menschen wichtig.', 'en')).toHaveLength(1);
});

test('B2 rebuttal hints recognize acknowledgment and response without fixed phrases', () => {
  const complete = 'Die Sorge ist nachvollziehbar und die Kosten sind wichtig. Langfristig spart die Modernisierung Energie und verbessert die Lernbedingungen.';
  expect(getB2WritingReviewHints('counterargument-dialogue', complete, 'en')).toEqual([expect.stringContaining('represented fairly')]);
  expect(getB2WritingReviewHints('counterargument-dialogue', 'Das ist zu teuer.', 'en')[0]).toContain('acknowledge the cost concern');
});

test('B2 rebuttal does not mistake generic natürlich for acknowledging an objection', () => {
  const generic = 'Natürlich ist eine gute Schule für alle Kinder wichtig. Aber wir sollten die Gebäude modernisieren, weil neue Räume bessere Lernbedingungen schaffen.';
  expect(getB2WritingReviewHints('counterargument-dialogue', generic, 'en').some(hint => hint.includes('acknowledged the objection'))).toBe(true);
  const acknowledged = 'Die Sorge um die Kosten ist nachvollziehbar. Aber wir sollten die Gebäude modernisieren, weil neue Räume bessere Lernbedingungen schaffen.';
  expect(getB2WritingReviewHints('counterargument-dialogue', acknowledged, 'en').some(hint => hint.includes('acknowledged the objection'))).toBe(false);
});

test('short B2 statistical drafts receive a task-specific revision step', () => {
  const hints = getB2WritingReviewHints('data_description-dialogue', 'Die Statistik zeigt einen Anstieg.', 'en');
  expect(hints).toHaveLength(1);
  expect(hints[0]).toContain('2020 (36%)');
  expect(hints[0]).toContain('increase (12 percentage points)');
});

test('short B2 drafts provide revision goals without leaking a model answer', () => {
  const tasks = [
    ['argument_structure-dialogue', 'own concrete example'],
    ['counterargument-dialogue', 'own counterargument'],
    ['data_description-dialogue', 'increase (12 percentage points)'],
  ];
  for (const [exerciseId, goal] of tasks) {
    const [hint] = getB2WritingReviewHints(exerciseId, 'Kurz.', 'en');
    expect(hint).toContain(goal);
    expect(hint).not.toContain('Beispiel:');
    expect(hint).not.toContain('Example:');
  }
});

test('B2 short-draft guidance is localized and avoids prewritten German sentences', () => {
  for (const lang of ['ru', 'de', 'en'] as const) {
    for (const exerciseId of ['argument_structure-dialogue', 'counterargument-dialogue', 'data_description-dialogue']) {
      const [hint] = getB2WritingReviewHints(exerciseId, 'Kurz.', lang);
      expect(hint.length).toBeGreaterThan(30);
      expect(hint).not.toContain('Ich bin für sichere Radwege');
      expect(hint).not.toContain('Die Sorge um die Kosten ist verständlich');
      expect(hint).not.toContain('Der Anteil stieg von');
    }
  }
});

test('B2 figures require whole numbers and do not confuse 36 with 136', () => {
  const complete = '2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Das sind 12 Prozentpunkte mehr.';
  expect(getB2WritingReviewHints('data_description-dialogue', complete, 'en')).toEqual([expect.stringContaining('which conclusion the data supports')]);
  const partial = getB2WritingReviewHints('data_description-dialogue', 'Im Jahr 2020 lag der Anteil bei 136 Prozent und im Jahr 2025 bei 48 Prozent. Die Differenz beträgt 12 Prozentpunkte.', 'en');
  expect(partial.some(hint => hint.includes('36'))).toBe(true);
});

test('B2 data review distinguishes percentage points from percentages', () => {
  const correct = 'Im Jahr 2020 lag der Anteil bei 36 Prozent und im Jahr 2025 bei 48 Prozent. Der Anstieg beträgt 12 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en')).toEqual([expect.stringContaining('which conclusion the data supports')]);
  const incorrectUnit = 'Im Jahr 2020 lag der Anteil bei 36 Prozent und im Jahr 2025 bei 48 Prozent. Der Anstieg beträgt 12 Prozent.';
  expect(getB2WritingReviewHints('data_description-dialogue', incorrectUnit, 'en').some(hint => hint.includes('percentage points'))).toBe(true);
});

test('B2 data review flags a wrong twelve-percent change even if points appear elsewhere', () => {
  const draft = '2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Der Anstieg beträgt 12 Prozent. An anderer Stelle werden Prozentpunkte erwähnt.';
  const hints = getB2WritingReviewHints('data_description-dialogue', draft, 'en');
  expect(hints.some(hint => hint.includes('Correct the change unit'))).toBe(true);
  const correct = '2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Der Anstieg beträgt 12 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en').some(hint => hint.includes('Correct the change unit'))).toBe(false);
});

test('B2 difference and percentage-point unit must refer to the same quantity', () => {
  const unrelated = 'Im Jahr 2020 waren es 36 Prozent, im Jahr 2025 waren es 48 Prozent. Es gibt 12 Gruppen und viele Prozentpunkte Unterschied.';
  expect(getB2WritingReviewHints('data_description-dialogue', unrelated, 'en').some(hint => hint.includes('12 percentage points'))).toBe(true);
  const explicit = 'Im Jahr 2020 waren es 36 Prozent, im Jahr 2025 waren es 48 Prozent. Die Differenz beträgt 12 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', explicit, 'en').some(hint => hint.includes('12 percentage points'))).toBe(false);
});

test('B2 data review flags explicitly swapped year-value pairs', () => {
  const reversed = 'Die Statistik zeigt: 2020: 48 %, 2025: 36 %. Insgesamt sind das 12 Prozentpunkte Unterschied bei den Nutzern.';
  expect(getB2WritingReviewHints('data_description-dialogue', reversed, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(true);
  const correct = 'Die Statistik zeigt: 2020: 36 %, 2025: 48 %. Insgesamt sind das 12 Prozentpunkte Unterschied bei den Nutzern.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(false);
});

test('B2 data review calculates percentage-point differences for custom figures', () => {
  const figures = { earlier: { year: 2018, percent: 25 }, later: { year: 2024, percent: 40 } };
  const wrong = '2018 lag der Anteil bei 25 Prozent, 2024 bei 40 Prozent. Die Differenz beträgt 12 Prozentpunkte.';
  const hints = getB2WritingReviewHints('data_description-dialogue', wrong, 'en', figures);
  expect(hints.some(hint => hint.includes('15 percentage points'))).toBe(true);
  const correct = '2018 lag der Anteil bei 25 Prozent, 2024 bei 40 Prozent. Die Differenz beträgt 15 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en', figures).some(hint => hint.includes('Check the difference:'))).toBe(false);
});

test('B2 custom data feedback never suggests the default twelve-point increase', () => {
  const figures = { earlier: { year: 2018, percent: 25 }, later: { year: 2024, percent: 40 } };
  const draft = '2018 lag der Anteil bei 25 Prozent, 2024 bei 40 Prozent. Der Anteil ist gesunken. Die Differenz beträgt 15 Prozentpunkte.';
  const hints = getB2WritingReviewHints('data_description-dialogue', draft, 'en', figures);
  expect(hints.some(hint => hint.includes('increased from 25% to 40%'))).toBe(true);
  expect(hints.join(' ')).not.toContain('36%');
  expect(hints.join(' ')).not.toContain('12 percentage points');
});

test('B2 year-value checks accept exercise-specific figures', () => {
  const figures = { earlier: { year: 2018, percent: 25 }, later: { year: 2024, percent: 40 } };
  const draft = '2018 lag der Anteil bei 40 Prozent. Im Jahr 2024 lag er bei 25 Prozent. Die Ergebnisse sollten verglichen werden.';
  const hints = getB2WritingReviewHints('data_description-dialogue', draft, 'en', figures);
  expect(hints[0]).toContain('25% in 2018 and 40% in 2024');
  expect(hints.some(hint => hint.includes('2020'))).toBe(false);
});

test('B2 data review handles explicit value-first year pairs without false alarms', () => {
  const reversed = 'Die Statistik zeigt 48 Prozent im Jahr 2020 und 36 Prozent im Jahr 2025. Die Differenz beträgt zwölf Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', reversed, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(true);
  const correct = 'Die Statistik zeigt 36 Prozent im Jahr 2020 und 48 Prozent im Jahr 2025. Die Differenz beträgt zwölf Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(false);
});

test('B2 data review detects reversed year-first clauses with an intervening verb', () => {
  const wrong = '2020 lag der Anteil bei 48 Prozent. 2025 lag der Anteil bei 36 Prozent. Die Differenz beträgt zwölf Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', wrong, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(true);
  const correct = '2020 lag der Anteil bei 36 Prozent. 2025 lag der Anteil bei 48 Prozent. Die Differenz beträgt zwölf Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(false);
});

test('B2 self-review limits data feedback to three prioritized revision steps', () => {
  const draft = 'Die Statistik beschreibt eine Veränderung über mehrere Jahre. Leider fehlen in dieser Beschreibung noch die konkreten Zahlen und ein klarer Vergleich zwischen beiden Zeitpunkten.';
  const hints = getB2WritingReviewHints('data_description-dialogue', draft, 'en');
  expect(hints).toHaveLength(3);
  expect(hints[0]).toContain('percentage points');
  expect(hints[1]).toContain('2020');
  expect(hints[2]).toContain('2025');
});

test('B2 data errors outrank omitted figures when feedback is capped', () => {
  const draft = 'Die Zahlen zeigen einen Unterschied zwischen zwei Jahren. In der Statistik steht 2020: 48 %. Die Veränderung beträgt 12 Prozent, und der Vergleich ist wichtig.';
  const hints = getB2WritingReviewHints('data_description-dialogue', draft, 'en');
  expect(hints).toHaveLength(3);
  expect(hints[0]).toContain('year-to-value pairing');
  expect(hints[1]).toContain('percentage points');
  expect(hints[2]).toContain('2025');
});

test('B2 feedback accepts equivalent statistical phrasing and keeps distinct errors visible', () => {
  const equivalent = '2020 betrug der Anteil 36 Prozent. Im Jahr 2025 lag er bei 48 Prozent. Dies entspricht einer Zunahme um zwölf Prozentpunkte.';
  const goodHints = getB2WritingReviewHints('data_description-dialogue', equivalent, 'en');
  expect(goodHints).toEqual([expect.stringContaining('which conclusion the data supports')]);

  const wrongUnitAndMissingYear = 'Die Statistik zeigt 2020: 48 Prozent. Der Anstieg beträgt 12 Prozent. Die Daten müssen noch genauer erläutert werden.';
  const hints = getB2WritingReviewHints('data_description-dialogue', wrongUnitAndMissingYear, 'en');
  expect(hints).toHaveLength(3);
  expect(hints[0]).toContain('year-to-value pairing');
  expect(hints[1]).toContain('Correct the change unit');
  expect(hints[2]).toContain('2025');
});

test('B2 data review flags explicit false decline without penalizing correct increase', () => {
  const wrong = 'Im Jahr 2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Der Anteil ist gesunken, um 12 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', wrong, 'en').some(hint => hint.includes('direction of change'))).toBe(true);
  const right = 'Im Jahr 2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Der Anteil ist gestiegen, um 12 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', right, 'en').some(hint => hint.includes('direction of change'))).toBe(false);
});

test('B2 argument review does not mistake approximate numbers for examples', () => {
  const approximate = 'Ich befürworte sichere Radwege, weil die Sicherheit wichtig ist. Etwa 20 Prozent der Menschen nutzen schon das Fahrrad in der Stadt.';
  const hints = getB2WritingReviewHints('argument_structure-dialogue', approximate, 'en');
  expect(hints.some(hint => hint.includes('concrete example'))).toBe(true);
  const example = 'Ich befürworte sichere Radwege, weil die Sicherheit wichtig ist. Zum Beispiel könnten Kinder dadurch sicherer zur Schule fahren.';
  expect(getB2WritingReviewHints('argument_structure-dialogue', example, 'en').some(hint => hint.includes('concrete example'))).toBe(false);
});

test('B2 data review detects false growth and false stability for falling figures', () => {
  const figures = { earlier: { year: 2022, percent: 60 }, later: { year: 2026, percent: 45 } };
  const wrong = '2022 lag der Anteil bei 60 Prozent, 2026 bei 45 Prozent. Der Anteil ist gestiegen, um 15 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', wrong, 'en', figures).some(hint => hint.includes('decreased from 60% to 45%'))).toBe(true);
  const stable = '2022 lag der Anteil bei 60 Prozent, 2026 bei 45 Prozent. Der Anteil blieb stabil, mit 15 Prozentpunkten Unterschied.';
  expect(getB2WritingReviewHints('data_description-dialogue', stable, 'en', figures).some(hint => hint.includes('direction of change'))).toBe(true);
  const right = '2022 lag der Anteil bei 60 Prozent, 2026 bei 45 Prozent. Der Anteil ist gesunken, um 15 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', right, 'en', figures).some(hint => hint.includes('direction of change'))).toBe(false);
});

test('B2 data review detects invented change for unchanged figures', () => {
  const figures = { earlier: { year: 2022, percent: 40 }, later: { year: 2026, percent: 40 } };
  const wrong = '2022 lag der Anteil bei 40 Prozent, 2026 bei 40 Prozent. Der Anteil ist gestiegen, um 10 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', wrong, 'en', figures).some(hint => hint.includes('remained unchanged'))).toBe(true);
  const right = '2022 lag der Anteil bei 40 Prozent, 2026 bei 40 Prozent. Der Anteil blieb stabil, es gab keine Veränderung.';
  expect(getB2WritingReviewHints('data_description-dialogue', right, 'en', figures).some(hint => hint.includes('direction of change'))).toBe(false);
});

test('B2 short-draft guidance uses actual exercise figures for all trend directions', () => {
  const cases = [
    { earlier: { year: 2018, percent: 25 }, later: { year: 2024, percent: 40 }, trend: 'increase', points: '15 percentage points' },
    { earlier: { year: 2022, percent: 60 }, later: { year: 2026, percent: 45 }, trend: 'decrease', points: '15 percentage points' },
    { earlier: { year: 2021, percent: 40 }, later: { year: 2025, percent: 40 }, trend: 'unchanged', points: '0 percentage points' },
  ];
  for (const figures of cases) {
    const hints = getB2WritingReviewHints('data_description-dialogue', 'Der Anteil', 'en', figures);
    expect(hints).toHaveLength(1);
    expect(hints[0]).toContain(figures.trend);
    expect(hints[0]).toContain(figures.points);
    expect(hints[0]).toContain(String(figures.earlier.year));
    expect(hints[0]).toContain(String(figures.later.year));
    expect(hints[0]).not.toContain('36%');
  }
});

test('unknown writing tasks never receive guessed B2 criteria', () => {
  expect(getB2WritingReviewHints('unknown-dialogue', 'Any answer', 'en')).toEqual([]);
});

test('B2 decline unit guidance is localized and avoids false positives', () => {
  const figures = { earlier: { year: 2022, percent: 60 }, later: { year: 2026, percent: 45 } };
  const wrong = '2022 lag der Anteil bei 60 Prozent und 2026 bei 45 Prozent. Der Rückgang beträgt 15 Prozent.';
  const right = '2022 lag der Anteil bei 60 Prozent und 2026 bei 45 Prozent. Der Rückgang beträgt 15 Prozentpunkte.';
  for (const [language, expected] of [['ru', '15 процентных пунктов'], ['de', '15 Prozentpunkte, nicht 15 %'], ['en', '15 percentage points, not 15%']] as const) {
    const wrongHints = getB2WritingReviewHints('data_description-dialogue', wrong, language, figures);
    expect(wrongHints.join(' ')).toContain(expected);
    const rightHints = getB2WritingReviewHints('data_description-dialogue', right, language, figures);
    expect(rightHints.join(' ')).not.toContain(expected);
  }
});

test('B2 stable figures accept an explicit no-change statement without zero-point wording', () => {
  const figures = { earlier: { year: 2021, percent: 40 }, later: { year: 2025, percent: 40 } };
  const correct = 'Im Jahr 2021 lag der Anteil bei 40 Prozent und im Jahr 2025 ebenfalls bei 40 Prozent. Der Anteil blieb unverändert.';
  for (const language of ['ru', 'de', 'en'] as const) {
    const hints = getB2WritingReviewHints('data_description-dialogue', correct, language, figures);
    expect(hints.some(hint => hint.includes('0 процентных пунктов') || hint.includes('0 Prozentpunkte') || hint.includes('0 percentage points'))).toBe(false);
  }
  const missingTrend = 'Im Jahr 2021 lag der Anteil bei 40 Prozent und im Jahr 2025 ebenfalls bei 40 Prozent. Die Statistik zeigt zwei Werte.';
  expect(getB2WritingReviewHints('data_description-dialogue', missingTrend, 'en', figures).some(hint => hint.includes('0 percentage points'))).toBe(true);
});

test('B2 review recognizes natural German trend descriptions', () => {
  const decrease = { earlier: { year: 2022, percent: 60 }, later: { year: 2026, percent: 45 } };
  const stable = { earlier: { year: 2021, percent: 40 }, later: { year: 2025, percent: 40 } };
  const decreaseRight = 'Im Jahr 2022 lag die Quote bei 60 Prozent und 2026 bei 45 Prozent. Die Quote ging zurück, und zwar um 15 Prozentpunkte.';
  const decreaseWrong = 'Im Jahr 2022 lag die Quote bei 60 Prozent und 2026 bei 45 Prozent. Die Quote nahm zu, und zwar um 15 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', decreaseRight, 'en', decrease).some(h => h.includes('direction of change'))).toBe(false);
  expect(getB2WritingReviewHints('data_description-dialogue', decreaseWrong, 'en', decrease).some(h => h.includes('direction of change'))).toBe(true);
  const stableRight = 'Im Jahr 2021 lag die Quote bei 40 Prozent und im Jahr 2025 ebenfalls bei 40 Prozent. Die Quote blieb auf demselben Niveau.';
  expect(getB2WritingReviewHints('data_description-dialogue', stableRight, 'en', stable).some(h => h.includes('0 percentage points'))).toBe(false);
});
