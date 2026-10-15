import { expect, test } from '@playwright/test';

test('missed-card round submits retry evidence instead of first-attempt mastery', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const submissions: Array<{ retry: boolean; mode: string; answer: string }> = [];
  let session = 0;
  await page.route('**/api/learning/reviews/**', route => route.fulfill({
    json: { reviews: [{ lesson_id: 77, exercise_index: 0, topic: 'word_order', type: 'choice',
      question: 'Choose the right order', options: ['Wrong', 'Correct'] }] },
  }));
  await page.route('**/api/lesson/start', route => route.fulfill({
    json: { session_id: 'review-session-' + ++session },
  }));
  await page.route('**/api/lesson/check-answer', route => {
    const payload = route.request().postDataJSON();
    submissions.push({ retry: payload.retry, mode: payload.mode, answer: payload.answer });
    return route.fulfill({ json: {
      evaluation_status: 'verified', correct: submissions.length > 1,
      correct_answer: 'Correct', explanation: 'Check the word order.',
    } });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/review');
  await expect(page.getByRole('heading', { name: 'Choose the right order' })).toBeVisible();
  await page.getByRole('radio', { name: 'Wrong' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('Let’s reinforce it')).toBeVisible();
  await page.getByRole('button', { name: 'Finish' }).click();
  await expect(page.getByText('0 of 1 correct. Missed items remain due for review.')).toBeVisible();
  await page.getByRole('button', { name: 'Practice missed cards' }).click();
  await expect(page.getByRole('heading', { name: 'Choose the right order' })).toBeVisible();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('Correct', { exact: true }).first()).toBeVisible();
  await page.getByRole('button', { name: 'Finish' }).click();
  await expect(page.getByText('1 of 1 correct. Missed items remain due for review.')).toBeVisible();
  expect(submissions).toEqual([
    { retry: false, mode: 'review', answer: 'Wrong' },
    { retry: true, mode: 'review', answer: 'Correct' },
  ]);
  expect(session).toBe(2);
});

test('review keeps selected answer after temporary network failure and does not duplicate progress', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  let submissions = 0;
  let sessionStarts = 0;
  await page.route('**/api/learning/reviews/**', route => route.fulfill({
    json: { reviews: [{ lesson_id: 77, exercise_index: 0, topic: 'word_order',
      type: 'choice', question: 'Choose the right order', options: ['Wrong', 'Correct'] }] },
  }));
  await page.route('**/api/lesson/start', route => route.fulfill({
    json: { session_id: 'session-' + ++sessionStarts },
  }));
  await page.route('**/api/lesson/check-answer', route => {
    submissions += 1;
    if (submissions === 1) return route.fulfill({ status: 503, json: { detail: 'Temporary outage' } });
    return route.fulfill({ json: { evaluation_status: 'verified', correct: true,
      correct_answer: 'Correct', explanation: 'Correct order.' } });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/review');
  await expect(page.getByRole('heading', { name: 'Choose the right order' })).toBeVisible();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('Your answer was not sent. Check the connection and try again.')).toBeVisible();
  await expect(page.getByRole('radio', { name: 'Correct' })).toBeChecked();
  expect(submissions).toBe(1);
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByRole('button', { name: 'Finish' })).toBeVisible();
  expect(submissions).toBe(2);
  await page.getByRole('button', { name: 'Finish' }).click();
  await expect(page.getByText('1 of 1 correct. Missed items remain due for review.')).toBeVisible();
});

test('review session conflict requires reload rather than replaying an accepted answer', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  let submissions = 0;
  let loads = 0;
  await page.route('**/api/learning/reviews/**', route => {
    loads += 1;
    return route.fulfill({ json: { reviews: loads === 1 ? [{
      lesson_id: 77, exercise_index: 0, topic: 'word_order',
      type: 'choice', question: 'Choose the right order', options: ['Wrong', 'Correct'],
    }] : [] } });
  });
  await page.route('**/api/lesson/start', route => route.fulfill({ json: { session_id: 'session-1' } }));
  await page.route('**/api/lesson/check-answer', route => {
    submissions += 1;
    return route.fulfill({ status: 409, json: { detail: 'Exercise already completed' } });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/review');
  await expect(page.getByRole('heading', { name: 'Choose the right order' })).toBeVisible();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('The session changed. Reload reviews to continue.')).toBeVisible();
  expect(submissions).toBe(1);
  await page.getByRole('button', { name: 'Reload' }).click();
  await expect(page.getByRole('heading', { name: 'All done for today' })).toBeVisible();
  expect(submissions).toBe(1);
  expect(loads).toBe(2);
});
