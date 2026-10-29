import { test, expect } from '@playwright/test';

test('mobile lesson reload restores the server cursor rather than a stale local draft', async ({ page }) => {
  const lessonId = 910;
  let starts = 0;
  await page.route('**/api/lesson/910?**', async route => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({
      id: lessonId, title: 'Resume regression', topic: 'connectors', level: 'B1',
      content: { exercises: [
        { type: 'choose', question: 'FIRST EXERCISE MARKER', answer: 'obwohl', options: ['obwohl', 'weil'] },
        { type: 'choose', question: 'SECOND EXERCISE MARKER', answer: 'weil', options: ['weil', 'obwohl'] },
      ] },
    }) });
  });
  await page.route('**/api/lesson/start', async route => {
    starts += 1;
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({
      session_id: 'resume-session-910', resumed: true, next_exercise_index: 1,
    }) });
  });
  // A stale local draft claims the first exercise is current, but the backend
  // has already accepted it. Server progress must win after an app restart.
  await page.addInitScript(() => {
    localStorage.setItem('deutschiq-lesson-draft-9001-910', JSON.stringify({
      sessionId: 'resume-session-910',
      step: 2,
      answer: 'obwohl',
      checked: true,
      feedback: { correct: true },
      savedAt: Date.now() - 60_000,
    }));
  });
  await page.goto('/lesson/910');
  await expect(page.getByText('SECOND EXERCISE MARKER')).toBeVisible();
  await expect(page.getByText('FIRST EXERCISE MARKER')).toHaveCount(0);
  await page.reload();
  await expect(page.getByText('SECOND EXERCISE MARKER')).toBeVisible();
  await expect(page.getByText('FIRST EXERCISE MARKER')).toHaveCount(0);
  expect(starts).toBeGreaterThanOrEqual(2);
});

test('accepted answer with lost confirmation recovers without resubmitting', async ({ page }) => {
  let startCalls = 0;
  let answerCalls = 0;
  await page.route('**/api/lesson/77?**', async route => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({
      id: 77, title: 'Network recovery', topic: 'Practice', level: 'A1',
      content: { title: 'Practice', examples: ['Hallo!'], exercises: [
        { type: 'choice', question: 'NETWORK FIRST MARKER', answer: 'obwohl', options: ['obwohl', 'weil'] },
        { type: 'choice', question: 'NETWORK SECOND MARKER', answer: 'weil', options: ['weil', 'obwohl'] },
      ] },
    }) });
  });
  await page.route('**/api/lesson/start', async route => {
    startCalls += 1;
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({
      session_id: 'network-recovery-77', resumed: startCalls > 1,
      next_exercise_index: startCalls > 1 ? 1 : 0,
    }) });
  });
  await page.route('**/api/lesson/check-answer', async route => {
    answerCalls += 1;
    await route.abort('failed');
  });
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));

  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await expect(page.getByText('NETWORK FIRST MARKER')).toBeVisible();
  await page.getByRole('radio', { name: 'obwohl' }).click();
  await page.getByRole('button', { name: /^(Check|Prüfen|Проверить)$/ }).click();
  await expect(page.getByText('NETWORK SECOND MARKER')).toBeVisible();
  expect(startCalls).toBeGreaterThanOrEqual(2);
  expect(answerCalls).toBe(1);
});
