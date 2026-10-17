import { test, expect } from '@playwright/test';
import { getB2WritingReviewHints } from '../../src/learning/b2WritingReview';

test('B2 argument hints recognize alternative reasoning and evidence', () => {
  const complete = 'Aufgrund der besseren Sicherheit ist der Ausbau sinnvoll. Konkret profitieren Schulkinder davon, weil sie sicherer zur Schule fahren können.';
  expect(getB2WritingReviewHints('argument_structure-dialogue', complete, 'en')).toEqual([]);
  const incomplete = getB2WritingReviewHints('argument_structure-dialogue', 'Ich bin für Radwege.', 'en');
  expect(incomplete).toHaveLength(1);
  expect(incomplete[0]).toContain('too brief');
  const expanded = 'Ich unterstütze Radwege in der Stadt, weil sie die Sicherheit für alle verbessern. Deshalb sollten wir diese Lösung wählen.';
  expect(getB2WritingReviewHints('argument_structure-dialogue', expanded, 'en')).toHaveLength(1);

  expect(getB2WritingReviewHints('argument_structure-dialogue', 'Ich bin für mehr Radwege in der Stadt, denn das ist für viele Menschen wichtig.', 'en')).toHaveLength(1);
});

test('B2 rebuttal hints recognize acknowledgment and response without fixed phrases', () => {
  const complete = 'Die Sorge ist nachvollziehbar und die Kosten sind wichtig. Langfristig spart die Modernisierung Energie und verbessert die Lernbedingungen.';
  expect(getB2WritingReviewHints('counterargument-dialogue', complete, 'en')).toEqual([]);
  expect(getB2WritingReviewHints('counterargument-dialogue', 'Das ist zu teuer.', 'en')[0]).toContain('too brief');
});

test('B2 figures require whole numbers and do not confuse 36 with 136', () => {
  const complete = '2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Das sind 12 Prozentpunkte mehr.';
  expect(getB2WritingReviewHints('data_description-dialogue', complete, 'en')).toEqual([]);
  const partial = getB2WritingReviewHints('data_description-dialogue', 'Im Jahr 2020 lag der Anteil bei 136 Prozent und im Jahr 2025 bei 48 Prozent. Die Differenz beträgt 12 Prozentpunkte.', 'en');
  expect(partial.some(hint => hint.includes('36'))).toBe(true);
});

test('B2 data review distinguishes percentage points from percentages', () => {
  const correct = 'Im Jahr 2020 lag der Anteil bei 36 Prozent und im Jahr 2025 bei 48 Prozent. Der Anstieg beträgt 12 Prozentpunkte.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en')).toEqual([]);
  const incorrectUnit = 'Im Jahr 2020 lag der Anteil bei 36 Prozent und im Jahr 2025 bei 48 Prozent. Der Anstieg beträgt 12 Prozent.';
  expect(getB2WritingReviewHints('data_description-dialogue', incorrectUnit, 'en').some(hint => hint.includes('percentage points'))).toBe(true);
});

test('B2 data review flags explicitly swapped year-value pairs', () => {
  const reversed = 'Die Statistik zeigt: 2020: 48 %, 2025: 36 %. Insgesamt sind das 12 Prozentpunkte Unterschied bei den Nutzern.';
  expect(getB2WritingReviewHints('data_description-dialogue', reversed, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(true);
  const correct = 'Die Statistik zeigt: 2020: 36 %, 2025: 48 %. Insgesamt sind das 12 Prozentpunkte Unterschied bei den Nutzern.';
  expect(getB2WritingReviewHints('data_description-dialogue', correct, 'en').some(hint => hint.includes('year-to-value pairing'))).toBe(false);
});

test('B2 self-review limits data feedback to three prioritized revision steps', () => {
  const draft = 'Die Statistik beschreibt eine Veränderung über mehrere Jahre. Leider fehlen in dieser Beschreibung noch die konkreten Zahlen und ein klarer Vergleich zwischen beiden Zeitpunkten.';
  const hints = getB2WritingReviewHints('data_description-dialogue', draft, 'en');
  expect(hints).toHaveLength(3);
  expect(hints[0]).toContain('2020');
  expect(hints[1]).toContain('2025');
  expect(hints[2]).toContain('36');
});

test('unknown writing tasks never receive guessed B2 criteria', () => {
  expect(getB2WritingReviewHints('unknown-dialogue', 'Any answer', 'en')).toEqual([]);
});
