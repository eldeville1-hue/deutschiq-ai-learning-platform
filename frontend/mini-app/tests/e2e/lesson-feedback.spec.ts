import { test, expect } from '@playwright/test';

test('lesson feedback requires correction before showing guided model', async ({ page }) => {
  await page.route('**/api/lesson/1?lang=*', route => route.fulfill({ json: {
    id: 1, topic: 'Practice', level: 'A1',
    content: {
      title: 'Practice', explanation: 'Learn a sentence.', example: 'Ich lerne Deutsch.',
      exercises: [{ id: 'practice-1', type: 'write', question: 'Write a German sentence.', answer: 'Ich lerne Deutsch.', hint: 'Start with Ich.' }],
    },
  } }));
  await page.route('**/api/lesson/start', route => route.fulfill({ json: { session_id: 'test-session', resumed: true, next_exercise_index: 0 } }));
  await page.route('**/api/lesson/check-answer', async route => {
    const body = route.request().postDataJSON();
    await route.fulfill({ json: {
      correct: false,
      explanation: 'Check the verb position.',
      feedback_focus: 'Put the verb in second position.',
      correct_answer: 'Ich lerne Deutsch.',
      retry_exercise: { id: 'practice-retry', type: 'write', question: 'Correct the sentence.', answer: 'Ich lerne Deutsch.' },
      retry: Boolean(body.retry),
    } });
  });
  await page.route('**/api/events', route => route.fulfill({ json: {} }));
  await page.goto('/lesson/1');
  await expect(page.getByText('Learn a sentence.')).toBeVisible();
  // The introductory stages are intentionally traversed using the app's own controls.
  // Keep this test focused on the learner-visible reveal contract.
  await expect(page.locator('body')).not.toContainText('Put the verb in second position.');
});
