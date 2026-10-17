import { test, expect } from '@playwright/test';
import { getB2WritingReviewHints } from '../../src/learning/b2WritingReview';

test('B2 argument hints recognize alternative reasoning and evidence', () => {
  const complete = 'Aufgrund der besseren Sicherheit ist der Ausbau sinnvoll. Konkret profitieren Schulkinder davon.';
  expect(getB2WritingReviewHints('argument_structure-dialogue', complete, 'en')).toEqual([]);
  const incomplete = getB2WritingReviewHints('argument_structure-dialogue', 'Ich bin für Radwege.', 'en');
  expect(incomplete).toHaveLength(2);
});

test('B2 rebuttal hints recognize acknowledgment and response without fixed phrases', () => {
  const complete = 'Die Sorge ist nachvollziehbar. Langfristig spart die Modernisierung Energie.';
  expect(getB2WritingReviewHints('counterargument-dialogue', complete, 'en')).toEqual([]);
  expect(getB2WritingReviewHints('counterargument-dialogue', 'Das ist zu teuer.', 'en')).toHaveLength(2);
});

test('B2 figures require whole numbers and do not confuse 36 with 136', () => {
  const complete = '2020 lag der Anteil bei 36 Prozent, 2025 bei 48 Prozent. Das sind 12 Prozentpunkte mehr.';
  expect(getB2WritingReviewHints('data_description-dialogue', complete, 'en')).toEqual([]);
  const partial = getB2WritingReviewHints('data_description-dialogue', '2020: 136 Prozent, 2025: 48 Prozent. Differenz: 12.', 'en');
  expect(partial.some(hint => hint.includes('36'))).toBe(true);
});

test('unknown writing tasks never receive guessed B2 criteria', () => {
  expect(getB2WritingReviewHints('unknown-dialogue', 'Any answer', 'en')).toEqual([]);
});
