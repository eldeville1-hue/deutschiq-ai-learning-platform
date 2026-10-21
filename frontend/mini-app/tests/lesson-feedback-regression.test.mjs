import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

const source = readFileSync(new URL('../src/pages/Lesson.tsx', import.meta.url), 'utf8');

test('guided retry keeps the model hidden on first failure', () => {
  assert.ok(source.includes('feedback?.correct_answer && (retried[exerciseIndex] ? ('));
  assert.ok(source.includes('!feedback?.retry_exercise ? ('));
});

test('fallback model is user-revealed, not automatically displayed', () => {
  assert.ok(source.includes('<details className="corrected-model">'));
  assert.ok(source.includes('Показать образец'));
  assert.ok(!source.includes('Возможный вариант:'));
});

test('correction guidance remains available', () => {
  assert.ok(source.includes('feedback?.feedback_focus'));
  assert.ok(source.includes('Исправить по словам'));
});
