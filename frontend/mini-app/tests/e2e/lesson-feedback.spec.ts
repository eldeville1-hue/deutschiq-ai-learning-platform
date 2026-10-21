import { test, expect } from '@playwright/test';

test('guided correction hides the model until the learner retries', async ({ page }) => {
  let checks = 0;
  const requests: boolean[] = [];
  await page.route('**/api/lesson/1?lang=*', route => route.fulfill({ json: {
    id: 1, topic: 'Practice', level: 'A1',
    content: {
      title: 'Practice', scenario: 'Practice German.', examples: ['Ich lerne Deutsch.'],
      can_do: 'Write a short sentence.', rule: 'The verb is second.',
      exercises: [{ id: 'practice-1', type: 'write', question: 'Write a German sentence.', answer: 'Ich lerne Deutsch.', hint: 'Start with Ich.' }],
    },
  } }));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'test-session', resumed: false, next_exercise_index: 0,
  } }));
  await page.route('**/api/lesson/check-answer', async route => {
    checks += 1;
    const body = route.request().postDataJSON();
    requests.push(Boolean(body.retry));
    await route.fulfill({ json: {
      correct: false,
      explanation: 'Check the verb position.',
      feedback_focus: 'Put the verb in second position.',
      correct_answer: 'Ich lerne Deutsch.',
      retry_exercise: { id: 'practice-retry', type: 'write', question: 'Correct the sentence.', answer: 'Ich lerne Deutsch.' },
    } });
  });
  await page.route('**/api/events', route => route.fulfill({ json: {} }));
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  await page.goto('/lesson/1');

  await page.locator('.dq-lesson-intro .dq-lesson-action').click();
  await page.locator('.dq-lesson-model .dq-lesson-action').click();
  await expect(page.getByText('Write a German sentence.')).toBeVisible();
  await page.locator('.exercise-text-answer textarea').fill('Ich Deutsch lerne.');
  await page.locator('.lesson-action-dock .primary-action').click();

  await expect(page.getByText('Put the verb in second position.')).toBeVisible();
  await expect(page.locator('.corrected-model')).toHaveCount(0);
  await page.locator('.answer-feedback > button').first().click();

  await expect(page.getByText('Correct the sentence.')).toBeVisible();
  await page.locator('.exercise-text-answer textarea').fill('Ich Deutsch lerne.');
  await page.locator('.lesson-action-dock .primary-action').click();

  await expect(page.locator('.corrected-model')).toBeVisible();
  await expect(page.locator('.corrected-model')).toContainText('Ich lerne Deutsch.');
  expect(checks).toBe(2);
  expect(requests).toEqual([false, true]);
});

test('fallback correction keeps the answer behind an explicit reveal', async ({ page }) => {
  const retryFlags: boolean[] = [];
  await page.route('**/api/lesson/1?lang=*', route => route.fulfill({ json: {
    id: 1, topic: 'Practice', level: 'A1',
    content: {
      title: 'Practice', scenario: 'Practice German.', examples: ['Ich lerne Deutsch.'],
      can_do: 'Write a short sentence.', rule: 'The verb is second.',
      exercises: [{ id: 'practice-1', type: 'write', question: 'Write a German sentence.', answer: 'Ich lerne Deutsch.' }],
    },
  } }));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'fallback-session', resumed: false, next_exercise_index: 0,
  } }));
  await page.route('**/api/lesson/check-answer', route => {
    retryFlags.push(Boolean(route.request().postDataJSON().retry));
    return route.fulfill({ json: {
    correct: false,
    feedback_focus: 'Put the verb in second position.',
    correct_answer: 'Ich lerne Deutsch.',
    retry_exercise: null,
  } });
  });
  await page.route('**/api/events', route => route.fulfill({ json: {} }));
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  await page.goto('/lesson/1');
  await page.locator('.dq-lesson-intro .dq-lesson-action').click();
  await page.locator('.dq-lesson-model .dq-lesson-action').click();
  await page.locator('.exercise-text-answer textarea').fill('Ich Deutsch lerne.');
  await page.locator('.lesson-action-dock .primary-action').click();

  const model = page.locator('details.corrected-model');
  await expect(model).toBeVisible();
  await expect(model).not.toHaveAttribute('open', '');
  await expect(model.locator('summary')).toHaveText('Show model');
  await model.locator('summary').click();
  await expect(model).toHaveAttribute('open', '');
  await expect(model.locator('strong')).toHaveText('Ich lerne Deutsch.');

  // A fallback has no server-issued retry task. The original exercise must be
  // submitted again without retry=true, avoiding a backend 409 conflict.
  await page.locator('.answer-feedback > button').first().click();
  await expect(page.getByText('Write a German sentence.')).toBeVisible();
  await page.locator('.exercise-text-answer textarea').fill('Ich Deutsch lerne.');
  await page.locator('.lesson-action-dock .primary-action').click();
  await expect(page.locator('details.corrected-model')).toBeVisible();
  expect(retryFlags).toEqual([false, false]);
});

test('uncertain evaluation does not mark a learner wrong or reveal the answer', async ({ page }) => {
  let checks = 0;
  await page.route('**/api/lesson/1?lang=*', route => route.fulfill({ json: {
    id: 1, topic: 'Practice', level: 'A1',
    content: {
      title: 'Practice', scenario: 'Practice German.', examples: ['Ich lerne Deutsch.'],
      can_do: 'Write a short sentence.', rule: 'The verb is second.',
      exercises: [{ id: 'practice-1', type: 'write', question: 'Write a German sentence.', answer: 'Ich lerne Deutsch.' }],
    },
  } }));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: {
    session_id: 'uncertain-session', resumed: false, next_exercise_index: 0,
  } }));
  await page.route('**/api/lesson/check-answer', route => {
    checks += 1;
    return route.fulfill({ json: {
      evaluation_status: 'uncertain', correct: false,
      correct_answer: 'Ich lerne Deutsch.',
    } });
  });
  await page.route('**/api/events', route => route.fulfill({ json: {} }));
  await page.goto('/lesson/1');
  await page.locator('.dq-lesson-intro .dq-lesson-action').click();
  await page.locator('.dq-lesson-model .dq-lesson-action').click();
  await page.locator('.exercise-text-answer textarea').fill('Ich Deutsch lerne.');
  await page.locator('.lesson-action-dock .primary-action').click();

  await expect(page.locator('.answer-feedback')).toHaveCount(0);
  await expect(page.locator('.corrected-model')).toHaveCount(0);
  await expect(page.locator('.exercise-text-answer textarea')).toBeVisible();
  await expect(page.locator('.lesson-action-dock .primary-action')).toBeEnabled();
  expect(checks).toBe(1);
});
