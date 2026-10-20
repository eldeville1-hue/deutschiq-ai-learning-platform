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

test('mobile lesson resumes from server after closing and reopening the app page', async ({ page, context }) => {
  await context.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const questions = [
    { type: 'choice', question: 'First question', options: ['Correct', 'Wrong'], answer: 'Correct' },
    { type: 'choice', question: 'Second question', options: ['Next', 'Other'], answer: 'Next' },
  ];
  let serverCursor = 0;
  let checks = 0;
  let starts = 0;
  await context.route('**/api/lesson/77?*', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({
      id: 77, level: 'A1', topic: 'Practice',
      content: { title: 'Practice', examples: ['Hallo!'], exercises: questions },
    }),
  }));
  await context.route('**/api/lesson/start', route => {
    starts += 1;
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        session_id: 'saved-session',
        resumed: serverCursor > 0,
        next_exercise_index: serverCursor,
      }),
    });
  });
  await context.route('**/api/lesson/check-answer', route => {
    checks += 1;
    serverCursor = 1;
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: true, evaluation_status: 'accepted', correct_answer: 'Correct' }),
    });
  });
  await context.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));

  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await page.getByRole('radio', { name: 'Correct' }).click();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('Correct', { exact: true }).first()).toBeVisible();
  expect(checks).toBe(1);

  // Closing the tab destroys React state, unlike a simple page reload.
  // A fresh page in the same Telegram browser context must resume from the
  // backend's committed cursor, not repeat the already answered question.
  await page.close();
  const reopened = await context.newPage();
  await reopened.goto('/lesson/77');
  await expect(reopened.getByRole('heading', { name: 'Second question' })).toBeVisible();
  await expect(reopened.getByRole('heading', { name: 'First question' })).toHaveCount(0);
  expect(starts).toBeGreaterThanOrEqual(2);
  expect(checks).toBe(1);
});


test('mobile pending AI writing review preserves answer and allows retry without penalty', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const letter = 'Sehr geehrte Frau Klein, ich möchte den Termin verschieben. Am Dienstag um zehn Uhr? Mit freundlichen Grüßen, Mia Weber.';
  const exercise = { type: 'production', question: 'Write a formal appointment change request.', model_answer: letter, assessment_criteria: ['formal_greeting', 'rescheduling_request', 'alternative_time', 'formal_closing'] };
  let checks = 0;
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'A2', topic: 'formal_message_a2',
    content: { title: 'Formal messages', examples: ['Sehr geehrte Frau Klein,'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'writing-session', resumed: false, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => {
    checks += 1;
    return route.fulfill({ json: {
      correct: false, evaluation_status: 'needs_review',
      retry_instruction: 'This task has no reliable reference answer yet. Your response has not been marked wrong.',
    }});
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  await expect(page.getByRole('heading', { name: 'Write a formal appointment change request.' })).toBeVisible();
  const writing = page.getByRole('textbox');
  await writing.fill(letter);
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  await expect(page.getByText('This task has no reliable reference answer yet. Your response has not been marked wrong.')).toBeVisible();
  await expect(writing).toHaveValue(letter);
  await expect(page.getByRole('button', { name: 'Try checking again' })).toBeVisible();
  await page.getByRole('button', { name: 'Try checking again' }).click();
  await expect.poll(() => checks).toBe(2);
  await expect(writing).toHaveValue(letter);
  await expect(page.getByText('Almost', { exact: true })).toHaveCount(0);
});


test('mobile uncertain translation keeps the response without wrong-answer feedback', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = { type: 'translate', question: 'Write a sentence about tomorrow.', answer: 'Ich fahre morgen nach Berlin.' };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'A1', topic: 'Practice',
    content: { title: 'Practice', examples: ['Ich fahre morgen nach Berlin.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'uncertain-session', resumed: false, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({ json: {
    correct: false, evaluation_status: 'uncertain',
    learner_feedback: 'Your answer needs further review.',
  }}));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  const writing = page.getByRole('textbox');
  await writing.fill('Morgen fahre ich nach Berlin.');
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  await expect(page.getByText('Your answer cannot be verified conclusively. That does not mean it is wrong. You can clarify your wording.')).toBeVisible();
  await expect(writing).toHaveValue('Morgen fahre ich nach Berlin.');
  await expect(page.locator('.answer-feedback.wrong')).toHaveCount(0);
});

test('mobile writing review succeeds after AI service recovers', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const letter = 'Sehr geehrte Frau Klein, ich möchte den Termin verschieben. Am Dienstag um zehn Uhr? Mit freundlichen Grüßen, Mia Weber.';
  const exercise = { type: 'production', question: 'Write a formal appointment change request.', model_answer: 'Sehr geehrte Frau Klein, könnten wir den Termin auf Mittwoch verschieben? Mit freundlichen Grüßen, Alex Weber.', assessment_criteria: ['formal_greeting', 'rescheduling_request', 'alternative_time', 'formal_closing'] };
  let checks = 0;
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'A2', topic: 'formal_message_a2',
    content: { title: 'Formal messages', examples: ['Sehr geehrte Frau Klein,'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'writing-session', resumed: false, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => {
    checks += 1;
    return route.fulfill({ json: checks === 1
      ? { correct: false, evaluation_status: 'needs_review', retry_instruction: 'Writing review is temporarily unavailable.' }
      : { correct: true, evaluation_status: 'verified', explanation: 'Good formal request.', production: true, production_score: 85, pass_mark: 70, cefr_standard: 'A2' },
    });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Understand with an example' }).click();
  await page.getByRole('button', { name: 'Start practice' }).click();
  const writing = page.getByRole('textbox');
  await writing.fill(letter);
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Try checking again' })).toBeVisible();
  await page.getByRole('button', { name: 'Try checking again' }).click();
  await expect.poll(() => checks).toBe(2);
  await expect(page.getByText('Correct', { exact: true })).toBeVisible();
  await expect(page.getByText('Try checking again')).toHaveCount(0);
  await expect(page.getByText('Writing review is temporarily unavailable.')).toHaveCount(0);
});


test('mobile B2 argument writing shows skill-specific self-check without penalty', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = { id: 'argument_structure-dialogue', type: 'dialogue', question: 'Give an argument.', answer: 'Für den Ausbau spricht, dass Radwege sicherer sind.' };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'argument_structure',
    content: { title: 'Argument structure', examples: ['Für den Ausbau spricht die Sicherheit.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'b2-argument-session', resumed: true, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({ json: {
    correct: false, evaluation_status: 'uncertain',
  }}));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  const writing = page.getByRole('textbox');
  await expect(writing).toBeVisible();
  const writingPlan = page.getByLabel('Writing plan');
  await expect(writingPlan.getByText('Position → 2. Reason → 3. Your example', { exact: false })).toBeVisible();
  await writing.fill('Geschützte Radwege sind sinnvoll, weil sie Unfälle vermeiden helfen.');
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  await expect(writingPlan).toHaveCount(0);
  await expect(page.getByText(/clear position, supporting reason and concrete example/)).toBeVisible();
  await expect(page.getByText(/Develop your argument: state your position/)).toBeVisible();
  await expect(writing).toHaveValue('Geschützte Radwege sind sinnvoll, weil sie Unfälle vermeiden helfen.');
  await expect(page.locator('.answer-feedback.wrong')).toHaveCount(0);
  const checklist = page.getByLabel('Writing self-check');
  await expect(checklist).toBeVisible();
  const compare = checklist.getByRole('button', { name: 'Compare with example' });
  await expect(compare).toHaveAttribute('aria-expanded', 'false');
  await expect(checklist.getByLabel('Example answer')).toHaveCount(0);
  await compare.click();
  await expect(checklist.getByLabel('Example answer')).toContainText('Für den Ausbau spricht');
  await checklist.getByRole('button', { name: 'Hide example' }).click();
  await expect(checklist.getByLabel('Example answer')).toHaveCount(0);
  const items = checklist.getByRole('checkbox');
  await expect(items).toHaveCount(3);
  await expect(checklist.getByText('My position is clear')).toBeVisible();
  await expect(checklist.getByText('I explained my reason and gave my own example')).toBeVisible();
  await items.nth(0).check();
  await expect(items.nth(0)).toBeChecked();
  await expect.poll(async () => page.evaluate(() => Object.keys(localStorage)
    .filter(key => key.startsWith('deutschiq-lesson-draft-'))
    .some(key => JSON.parse(localStorage.getItem(key) || '{}').writingSelfCheck === true)
  )).toBe(true);
  await page.reload();
  await expect(page.getByLabel('Writing self-check')).toBeVisible();
  await expect(page.getByLabel('Writing self-check').getByRole('checkbox').nth(0)).toBeChecked();
  await writing.fill('Geschützte Radwege sind sinnvoll, weil sie Unfälle vermeiden helfen. Außerdem fördern sie das Radfahren.');
  await expect(checklist).toHaveCount(0);
  await expect(page.getByText(/clear position, supporting reason and concrete example/)).toHaveCount(0);
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  await expect(checklist).toBeVisible();
  await expect(items.nth(0)).not.toBeChecked();
  await checklist.getByRole('button', { name: 'Improve my answer' }).click();
  await expect(checklist).toHaveCount(0);
  await expect(writing).toHaveValue('Geschützte Radwege sind sinnvoll, weil sie Unfälle vermeiden helfen. Außerdem fördern sie das Radfahren.');
});


test('mobile B2 rebuttal preserves independent writing through review and revision', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = {
    id: 'counterargument-dialogue', type: 'dialogue',
    question: 'A school renovation is considered too expensive. Acknowledge the concern and give a reasoned response.',
    answer: 'Zwar entstehen Kosten, langfristig können bessere Gebäude jedoch Vorteile bieten.',
  };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'counterargument',
    content: { title: 'Addressing objections', examples: ['Zwar entstehen Kosten.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'b2-rebuttal-session', resumed: true, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({ json: {
    correct: false, evaluation_status: 'uncertain',
  }}));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  const writing = page.getByRole('textbox');
  await expect(writing).toBeVisible();
  const draft = 'Die Sorge um die Kosten ist nachvollziehbar. Allerdings können moderne Räume die Lernbedingungen verbessern.';
  await writing.fill(draft);
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  const checklist = page.getByLabel('Writing self-check');
  await expect(checklist).toBeVisible();
  await expect(page.locator('.answer-feedback.wrong')).toHaveCount(0);
  await expect(writing).toHaveValue(draft);
  await expect(checklist.getByRole('checkbox')).toHaveCount(3);
  await expect(checklist.getByRole('button', { name: 'Compare with example' })).toHaveAttribute('aria-expanded', 'false');
  await page.reload();
  await expect(page.getByLabel('Writing self-check')).toBeVisible();
  await expect(page.getByRole('textbox')).toHaveValue(draft);
  await page.getByLabel('Writing self-check').getByRole('button', { name: 'Improve my answer' }).click();
  await expect(page.getByLabel('Writing self-check')).toHaveCount(0);
  await expect(page.getByRole('textbox')).toHaveValue(draft);
});

test('mobile B2 data description reviews percentage points without penalizing uncertainty', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = {
    id: 'data_description-dialogue', type: 'dialogue',
    question: 'Describe the user share: 36% in 2020 and 48% in 2025. Avoid unsupported explanations.',
    answer: 'Der Anteil stieg von 36 auf 48 Prozent, also um zwölf Prozentpunkte.',
  };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'data_description',
    content: { title: 'Describe data', examples: ['Der Anteil lag 2020 bei 36 Prozent.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'b2-data-session', resumed: true, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({ json: {
    correct: false, evaluation_status: 'uncertain',
  }}));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  const writing = page.getByRole('textbox');
  await expect(writing).toBeVisible();
  const draft = 'Im Jahr 2020 lag der Anteil bei 36 Prozent. 2025 waren es 48 Prozent. Das sind zwölf Prozentpunkte mehr.';
  await writing.fill(draft);
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  const checklist = page.getByLabel('Writing self-check');
  await expect(checklist).toBeVisible();
  await expect(checklist.getByRole('checkbox')).toHaveCount(3);
  await expect(page.locator('.answer-feedback.wrong')).toHaveCount(0);
  await expect(writing).toHaveValue(draft);
  await expect(checklist.getByRole('button', { name: 'Compare with example' })).toHaveAttribute('aria-expanded', 'false');
  await page.reload();
  await expect(page.getByLabel('Writing self-check')).toBeVisible();
  await expect(page.getByRole('textbox')).toHaveValue(draft);
  await page.getByLabel('Writing self-check').getByRole('button', { name: 'Improve my answer' }).click();
  await expect(page.getByLabel('Writing self-check')).toHaveCount(0);
  await expect(page.getByRole('textbox')).toHaveValue(draft);
});

test('mobile B2 writing uses exercise-specific statistics from lesson payload', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = {
    id: 'data_description-dialogue', type: 'dialogue',
    question: 'Describe 25% in 2018 and 40% in 2024.',
    answer: '2018 lag der Anteil bei 25 Prozent, 2024 bei 40 Prozent.',
    data_figures: { earlier: { year: 2018, percent: 25 }, later: { year: 2024, percent: 40 } },
  };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'data_description',
    content: { title: 'Describe data', examples: ['2018: 25%; 2024: 40%.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'b2-custom-data-session', resumed: true, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({ json: {
    correct: false, evaluation_status: 'uncertain',
  }}));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  const writing = page.getByRole('textbox');
  await expect(writing).toBeVisible();
  await writing.fill('2018 lag der Anteil bei 25 Prozent. 2024 lag er bei 40 Prozent. Die Differenz beträgt 12 Prozentpunkte.');
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  const checklist = page.getByLabel('Writing self-check');
  await expect(checklist).toBeVisible();
  await expect(checklist).toContainText('15 percentage points');
  await expect(checklist).not.toContainText('36%');
  await expect(page.locator('.answer-feedback.wrong')).toHaveCount(0);
});

test('mobile B2 practice switches between decrease and stable data with matching self-check', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = {
    id: 'data_description-dialogue', type: 'dialogue', question: 'Describe the increase.',
    answer: 'Der Anteil stieg von 36 auf 48 Prozent.',
    data_figures: { earlier: { year: 2020, percent: 36 }, later: { year: 2025, percent: 48 } },
    practice_variants: [
      { id: 'decrease', prompt: { en: 'Describe the decrease from 60% to 45%.' }, model: 'Der Anteil sank um 15 Prozentpunkte.', data_figures: { earlier: { year: 2022, percent: 60 }, later: { year: 2026, percent: 45 } } },
      { id: 'stable', prompt: { en: 'Describe the unchanged share of 40%.' }, model: 'Der Anteil blieb unverändert.', data_figures: { earlier: { year: 2021, percent: 40 }, later: { year: 2025, percent: 40 } } },
    ],
  };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'data_description',
    content: { title: 'Describe data', examples: ['Compare the figures.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'b2-practice-switch-session', resumed: true, next_exercise_index: 0,
  }}));
  let submittedAnswer = '';
  await page.route('**/api/lesson/check-answer', async route => {
    const payload = route.request().postDataJSON();
    submittedAnswer = String(payload.answer || '');
    expect(payload.exercise_index).toBe(0);
    expect(payload.practice_variant_id).toBe('stable');
    await route.fulfill({ json: { correct: false, evaluation_status: 'uncertain' } });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: 'Decrease', exact: true }).click();
  await expect(page.getByRole('heading', { name: /decrease from 60% to 45%/i })).toBeVisible();
  const writing = page.getByRole('textbox');
  await writing.fill('Draft for decrease');
  await page.reload();
  await expect(page.getByRole('button', { name: 'Decrease', exact: true })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByRole('heading', { name: /decrease from 60% to 45%/i })).toBeVisible();
  await expect(page.getByRole('textbox')).toHaveValue('Draft for decrease');
  await page.getByRole('button', { name: 'No change', exact: true }).click();
  await expect(writing).toHaveValue('');
  await expect(page.getByRole('heading', { name: /unchanged share of 40%/i })).toBeVisible();
  await writing.fill('2021 lag der Anteil bei 40 Prozent. 2025 lag der Anteil bei 40 Prozent. Der Anteil blieb unverändert.');
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  await expect(page.getByLabel('Writing self-check')).toContainText('0 percentage points');
  expect(submittedAnswer).toContain('blieb unverändert');
});

test('mobile B2 draft survives reload in the same server session', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = { id: 'argument_structure-dialogue', type: 'dialogue', question: 'Give an argument.', answer: 'Radwege erhöhen die Sicherheit.' };
  let starts = 0;
  let serverSessionId = 'persistent-b2-session';
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'argument_structure',
    content: { title: 'Argument structure', examples: ['Radwege erhöhen die Sicherheit.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => {
    starts += 1;
    return route.fulfill({ json: {
      session_id: serverSessionId, resumed: true, next_exercise_index: 0,
    } });
  });
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  const text = 'Geschützte Radwege sind wichtig, weil sie die Verkehrssicherheit erhöhen.';
  await page.getByRole('textbox').fill(text);
  await expect.poll(async () => page.evaluate(() =>
    Object.keys(localStorage).filter(key => key.startsWith('deutschiq-lesson-draft-'))
      .some(key => JSON.parse(localStorage.getItem(key) || '{}').answer === 'Geschützte Radwege sind wichtig, weil sie die Verkehrssicherheit erhöhen.')
  )).toBe(true);
  await page.reload();
  await expect(page.getByRole('textbox')).toHaveValue(text);
  await expect(page.getByRole('heading', { name: 'Give an argument.' })).toBeVisible();
  expect(starts).toBeGreaterThanOrEqual(2);
  serverSessionId = 'new-b2-session';
  await page.reload();
  await expect(page.getByRole('textbox')).toHaveValue('');
});

test('mobile B2 assessment displays unmet criterion and actionable feedback', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  const exercise = {
    id: 'data_description-dialogue', type: 'dialogue',
    question: 'Describe the change and explain whether advertising caused it.',
    answer: 'The data alone do not prove a cause.',
  };
  await page.route('**/api/lesson/77?*', route => route.fulfill({ json: {
    id: 77, level: 'B2', topic: 'data_description',
    content: { title: 'Describe data', examples: ['Compare the values.'], exercises: [exercise] },
  }}));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'b2-rubric-visibility-session', resumed: true, next_exercise_index: 0,
  }}));
  await page.route('**/api/lesson/check-answer', route => route.fulfill({ json: {
    correct: false, evaluation_status: 'verified', production: true,
    production_score: 71, pass_mark: 75, cefr_standard: 'B2',
    dimension_scores: { task_completion: 59, grammar: 90, vocabulary: 90, coherence: 90, register: 90 },
    missing_task_parts: ['cautious_interpretation'],
    improvement: 'These figures alone do not prove an advertising effect.',
    correct_answer: 'The data alone do not prove a cause.',
    explanation: 'Explain the limits of the evidence.',
  }}));
  await page.route('**/api/events', route => route.fulfill({ status: 204, body: '' }));
  await page.goto('/lesson/77');
  await page.getByRole('textbox').fill('Der Anteil stieg von 25 auf 35 Prozent. Das ist ein deutlicher Anstieg.');
  await page.getByRole('button', { name: 'Check', exact: true }).click();
  const assessment = page.locator('.production-assessment');
  await expect(assessment).toBeVisible();
  await expect(assessment).toContainText('Needs improvement:');
  await expect(assessment).toContainText('evidence-based interpretation');
  await expect(assessment).toContainText('These figures alone do not prove an advertising effect.');
  await expect(assessment).toContainText('59%');
});
