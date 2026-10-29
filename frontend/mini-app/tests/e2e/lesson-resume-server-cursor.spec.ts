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
