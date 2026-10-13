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

test('mobile learner completes a lesson and sees the server-saved result', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  let checks = 0;
  let completions = 0;
  await page.route('**/api/lesson/77?*', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({
      id: 77, level: 'A1', topic: 'Practice',
      content: {
        title: 'Practice', examples: ['Hallo!'],
        exercises: [{ type: 'choice', question: 'First question', options: ['Correct', 'Wrong'], answer: 'Correct' }],
      },
    }),
  }));
  await page.route('**/api/lesson/start', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ session_id: 'saved-session', resumed: false, next_exercise_index: 0 }),
  }));
  await page.route('**/api/lesson/check-answer', async route => {
    checks += 1;
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: true, evaluation_status: 'accepted', correct_answer: 'Correct' }),
    });
  });
  await page.route('**/api/lesson/complete', async route => {
    completions += 1;
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        passed: true, score: 100, mastery: 100, xp_gained: 15,
        exercise_count: 1, first_try_correct: 1,
      }),
    });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('Correct', { exact: true }).first()).toBeVisible();
  await page.getByRole('button', { name: 'Next' }).click();
  await expect(page.getByRole('heading', { name: 'This is your German now' })).toBeVisible();
  await expect(page.getByText('+15 XP')).toBeVisible();
  expect(checks).toBe(1);
  expect(completions).toBe(1);
});

test('mobile lesson recovers a saved result after a lost completion response', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  let completions = 0;
  await page.route('**/api/lesson/77?*', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({
      id: 77, level: 'A1', topic: 'Practice',
      content: {
        title: 'Practice', examples: ['Hallo!'],
        exercises: [{ type: 'choice', question: 'First question', options: ['Correct', 'Wrong'], answer: 'Correct' }],
      },
    }),
  }));
  await page.route('**/api/lesson/start', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ session_id: 'saved-session', resumed: false, next_exercise_index: 0 }),
  }));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ correct: true, evaluation_status: 'accepted', correct_answer: 'Correct' }),
  }));
  await page.route('**/api/lesson/complete', async route => {
    completions += 1;
    if (completions === 1) {
      // Simulate a response lost after the backend committed the completion.
      await route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ detail: 'Connection lost' }) });
    } else {
      await route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({
          status: 'passed', passed: true, score: 100, mastery: 100,
          xp_gained: 0, already_completed: true, recovered: true,
          exercise_count: 1, first_try_correct: 1,
        }),
      });
    }
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await page.getByRole('button', { name: 'Next' }).click();
  await expect(page.getByRole('heading', { name: 'This is your German now' })).toHaveCount(0);
  await page.getByRole('button', { name: 'Save again' }).click();
  await expect(page.getByRole('heading', { name: 'This is your German now' })).toBeVisible();
  await expect(page.locator('.mission-xp')).toHaveCount(0);
  expect(completions).toBe(2);
});

test('mobile plan fetches fresh server progress when the WebView becomes visible', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  let planReads = 0;
  let dashboardReads = 0;
  let journeyReads = 0;
  let completed = false;

  await page.route('**/api/plan/9001?*', route => {
    planReads += 1;
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify([{
        id: 77, level: 'A1', topic: 'Practice', title: 'First lesson',
        week: 1, completed, attempts: completed ? 1 : 0,
      }, {
        id: 78, level: 'A1', topic: 'Practice', title: 'Second lesson',
        week: 1, completed: false, attempts: 0,
      }]),
    });
  });
  await page.route('**/api/dashboard/9001', route => {
    dashboardReads += 1;
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ level: 'A1', targetLevel: 'A2', xp: completed ? 15 : 0 }),
    });
  });
  await page.route('**/api/plan/journey/9001', route => {
    journeyReads += 1;
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ current_level: 'A1', levels: [] }),
    });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/plan');
  await expect(page.getByRole('heading', { name: 'First lesson' })).toBeVisible();
  const before = { planReads, dashboardReads, journeyReads };
  completed = true;
  // A Telegram WebView can resume while the Plan component remains mounted.
  // The new requests must bypass the otherwise valid 30-second API cache.
  await page.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
  await expect.poll(() => planReads).toBeGreaterThan(before.planReads);
  await expect.poll(() => dashboardReads).toBeGreaterThan(before.dashboardReads);
  await expect.poll(() => journeyReads).toBeGreaterThan(before.journeyReads);
  await expect(page.getByRole('heading', { name: 'Second lesson' })).toBeVisible();
});
