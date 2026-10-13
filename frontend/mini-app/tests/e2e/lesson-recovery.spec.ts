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



test('mobile lesson preserves selected answer when server returns 500', async ({ page }) => {
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
      status: 500, contentType: 'application/json',
      body: JSON.stringify({ detail: 'Temporary error' }),
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
  await expect(page.getByText('The server is unavailable or taking too long. Your answer was not confirmed; try again later.')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'First question' })).toBeVisible();
  await expect(page.getByRole('radio', { name: 'Correct' })).toHaveAttribute('aria-checked', 'true');
  expect(checks).toBe(1);
});

test('mobile lesson reload restores the server-authoritative exercise cursor', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));

  const questions = [
    { type: 'choice', question: 'First question', options: ['Correct', 'Wrong'], answer: 'Correct' },
    { type: 'choice', question: 'Second question', options: ['Next', 'Other'], answer: 'Next' },
  ];
  let serverCursor = 0;
  let reloadStarted = false;
  await page.route('**/api/lesson/77?*', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({
      id: 77, level: 'A1', topic: 'Practice',
      content: { title: 'Practice', examples: ['Hallo!'], exercises: questions },
    }),
  }));
  await page.route('**/api/lesson/start', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({
      session_id: 'saved-session',
      resumed: reloadStarted,
      next_exercise_index: serverCursor,
    }),
  }));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await expect(page.getByRole('heading', { name: 'First question' })).toBeVisible();

  // Simulate a committed first answer before the WebView is closed/reloaded.
  // On reopening, the server cursor must override any stale local draft.
  serverCursor = 1;
  reloadStarted = true;
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Second question' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'First question' })).toHaveCount(0);
});
