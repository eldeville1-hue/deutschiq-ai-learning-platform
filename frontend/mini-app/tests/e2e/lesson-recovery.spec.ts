import { expect, test } from '@playwright/test';

test('mobile lesson recovers server cursor after duplicate answer conflict', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('deutschiq_lang', 'en');
  });

  const questions = [
    { type: 'choice', question: 'First question', options: ['Correct', 'Wrong'], answer: 'Correct' },
    { type: 'choice', question: 'Second question', options: ['Next', 'Other'], answer: 'Next' },
  ];
  let starts = 0;
  let checks = 0;
  await page.route('**/api/lesson/77?*', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({
      id: 77, level: 'A1', topic: 'Practice',
      content: { title: 'Practice', examples: ['Hallo!'], exercises: questions },
    }),
  }));
  await page.route('**/api/lesson/start', async route => {
    starts += 1;
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        session_id: 'saved-session', resumed: checks > 0,
        next_exercise_index: checks > 0 ? 1 : 0,
      }),
    });
  });
  await page.route('**/api/lesson/check-answer', async route => {
    checks += 1;
    await route.fulfill({
      status: 409, contentType: 'application/json',
      body: JSON.stringify({ detail: 'Exercise already completed' }),
    });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  const browserErrors: string[] = [];
  page.on('pageerror', error => browserErrors.push(error.message));
  page.on('console', message => {
    if (message.type() === 'error') browserErrors.push(message.text());
  });
  const navigation = await page.goto('/lesson/77');
  await page.waitForTimeout(1500);
  if (!(await page.getByRole('button', { name: 'Understand with an example' }).count())) {
    throw new Error(JSON.stringify({
      status: navigation?.status(),
      url: page.url(),
      body: (await page.locator('body').innerText()).slice(0, 1000),
      html: (await page.locator('body').innerHTML()).slice(0, 1000),
      browserErrors,
      starts,
    }));
  }
  await expect(page.getByRole('button', { name: 'Understand with an example' }),
    'Lesson screen did not load. Visible page: ' + (await page.locator('body').innerText()).slice(0, 1000)).toBeVisible();
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await expect(page.getByRole('heading', { name: 'First question' })).toBeVisible();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();

  await expect(page.getByRole('heading', { name: 'Second question' })).toBeVisible();
  expect(checks).toBe(1);
  expect(starts).toBeGreaterThanOrEqual(2);
  await expect(page.getByText('Reopen the lesson from your plan to continue.')).toHaveCount(0);
});
