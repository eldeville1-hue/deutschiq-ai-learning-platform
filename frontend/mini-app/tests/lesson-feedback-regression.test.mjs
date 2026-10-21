import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

const source = readFileSync(new URL('../src/pages/Lesson.tsx', import.meta.url), 'utf8');

test('wrong-answer model is gated on retry', () => {
  assert.ok(source.includes('feedback?.correct_answer && Boolean(retried[exerciseIndex])'));
  assert.ok(!source.includes('model-reveal'));
  assert.ok(!source.includes('Возможный вариант:'));
});

test('guidance and correction action remain available', () => {
  assert.ok(source.includes('feedback?.feedback_focus'));
  assert.ok(source.includes('Исправить по словам'));
});
