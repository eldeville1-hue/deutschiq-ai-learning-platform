import { expect, Page, test } from '@playwright/test';

const userState = (completed: boolean, language = 'en') => ({ exists: completed, diagnostic_completed: completed, language, level: completed ? 'B1' : 'A1', xp: 120, streak: 3, beta_access: true, beta_onboarding_completed: true });
const nextLesson = { id: 77, topic: 'konjunktiv_ii', title: 'Konjunktiv II: advice', level: 'B1', reason: 'weakest_ready_skill' };
const today = (dueCount = 0) => ({ due_count: dueCount, next_lesson: nextLesson, session: { phases: [], minutes: 12 }, assessment: { samples: 4, weakest_dimension: 'coherence', weakest_score: 52, dimensions: { coherence: { score: 52, samples: 4 } }, priority_topics: [{ topic: 'konjunktiv_ii', dimension: 'coherence', score: 52 }] } });
const plan = [{ ...nextLesson, week: 2, track: 'B1', completed: false, blocked_by: [], recommended: true }];
const dashboard = { level: 'B1', targetLevel: 'B2', xp: 120, streak: 3, weaknesses: [{ name: 'konjunktiv_ii', score: 24 }] };
const lesson = {
  id: 77, level: 'B1', topic: 'konjunktiv_ii', estimated_time: 12, xp_reward: 70,
  content: { cefr: 'B1', title: 'Konjunktiv II: advice', objective: 'Give polite advice.', rule: 'Use sollte for advice.', examples: ['Du solltest früher schlafen gehen.'], common_mistakes: [], exercises: [{ type: 'dialogue', stage: 'transfer', question: 'Give a friend polite advice.' }] },
};

async function mockApi(page: Page, options: { completed?: boolean; dueCount?: number; reviews?: unknown[]; language?: string } = {}) {
  await page.route('**/api/**', async route => {
    const { pathname } = new URL(route.request().url());
    if (pathname.includes('/api/user/state/')) return route.fulfill({ json: userState(options.completed ?? true, options.language || 'en') });
    if (pathname.includes('/api/learning/today/')) return route.fulfill({ json: today(options.dueCount ?? 0) });
    if (pathname.includes('/api/learning/reviews/')) return route.fulfill({ json: { reviews: options.reviews ?? [] } });
    if (pathname.includes('/api/dashboard/')) return route.fulfill({ json: dashboard });
    if (pathname.includes('/api/plan/')) return route.fulfill({ json: plan });
    if (pathname === '/api/lesson/start') return route.fulfill({ json: { session_id: 'test-session' } });
    if (pathname === '/api/lesson/check-answer') return route.fulfill({ json: { correct: true, explanation: 'Task completed.', correct_answer: 'Du solltest früher schlafen gehen.', production: true, production_score: 82, cefr_standard: 'B1', pass_mark: 70, dimension_scores: { task_completion: 85, grammar: 80, vocabulary: 78, coherence: 80, register: 86 }, improvement: 'Add one concrete reason.' } });
    if (pathname === '/api/lesson/complete') return route.fulfill({ json: { passed: true, score: 100, mastery: 76, xp_gained: 70, first_try_correct: 1, corrected_retries: 0, needs_review: 0 } });
    if (pathname === '/api/lesson/77') return route.fulfill({ json: lesson });
    if (pathname === '/api/events') return route.fulfill({ status: 204 });
    return route.fulfill({ json: {} });
  });
}

async function expectNoHorizontalOverflow(page: Page) {
  await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
}

test('new user sees onboarding and can enter diagnostics', async ({ page }) => {
  await mockApi(page, { completed: false });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /German that adapts/i })).toBeVisible();
  await expect(page.locator('.bottom-nav')).toHaveCount(0);
  await page.getByRole('button', { name: /Find my level/i }).click();
  await expect(page).toHaveURL(/\/diagnostic/);
  await expectNoHorizontalOverflow(page);
});

test('returning user stays out of diagnostics after reload', async ({ page }) => {
  await mockApi(page, { completed: true });
  await page.goto('/');
  await expect(page.getByText('WELCOME BACK')).toBeVisible();
  await page.getByRole('button', { name: /Continue/i }).click();
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByRole('heading', { name: /Your lesson/i })).toBeVisible();
  await page.goto('/');
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByText(/German that adapts/i)).toHaveCount(0);
  await page.context().setOffline(true);
  await expect(page.getByRole('status')).toContainText('Offline');
  await page.context().setOffline(false);
  await expect(page.getByRole('status')).toHaveCount(0);
  await expectNoHorizontalOverflow(page);
});

test('daily start connects due review to the recommended lesson', async ({ page }) => {
  await mockApi(page, { completed: true, dueCount: 2, reviews: [] });
  await page.goto('/dashboard');
  await page.getByRole('button', { name: /Start with review/i }).click();
  await expect(page).toHaveURL(/\/review\?nextLesson=77/);
  await page.getByRole('button', { name: /Continue to new skill/i }).click();
  await expect(page).toHaveURL(/\/lesson\/77/);
  await expect(page.getByText('NEW SKILL')).toBeVisible();
  await expectNoHorizontalOverflow(page);
});

test('profile bootstrap offers a working retry after a network failure', async ({ page }) => {
  let attempts = 0;
  await page.route('**/api/user/state/**', async route => {
    attempts += 1;
    if (attempts <= 2) return route.abort('failed');
    return route.fulfill({ json: userState(false) });
  });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /Could not load your profile/i })).toBeVisible();
  await page.getByRole('button', { name: /Try again/i }).click();
  await expect(page.getByRole('heading', { name: /German that adapts/i })).toBeVisible();
});

test('invite claim continues through consent onboarding into diagnostics', async ({ page }) => {
  let stage: 'invite'|'onboarding'|'ready' = 'invite';
  await page.route('**/api/**', async route => {
    const { pathname } = new URL(route.request().url());
    if (pathname.includes('/api/user/state/')) return route.fulfill({ json: {
      ...userState(false), exists: stage !== 'invite', beta_access: stage !== 'invite', beta_onboarding_completed: stage === 'ready',
    }});
    if (pathname === '/api/beta/claim') { stage = 'onboarding'; return route.fulfill({ json: { access: true, onboarding_completed: false } }); }
    if (pathname === '/api/beta/onboarding') { stage = 'ready'; return route.fulfill({ json: { onboarding_completed: true } }); }
    return route.fulfill({ json: {} });
  });
  await page.goto('/?invite=READY45');
  await expect(page.getByRole('heading', { name: /Join the closed beta/i })).toBeVisible();
  await page.getByRole('button', { name: /Continue/i }).click();
  await expect(page.getByRole('heading', { name: /Set up your beta/i })).toBeVisible();
  await page.getByRole('checkbox').check();
  await page.getByRole('button', { name: /Start learning/i }).click();
  await expect(page.getByRole('heading', { name: /German that adapts/i })).toBeVisible();
  await expectNoHorizontalOverflow(page);
});

test('beta learner can report an issue from a primary screen', async ({ page }) => {
  let report: any = null;
  await mockApi(page, { completed: true });
  await page.route('**/api/beta/issue', async route => { report = route.request().postDataJSON(); return route.fulfill({ json: { ok: true } }); });
  await page.goto('/dashboard');
  await page.getByRole('button', { name: /Report a problem/i }).click();
  await page.getByRole('textbox').fill('The exercise button is hidden');
  await page.getByRole('button', { name: /^Send$/i }).click();
  await expect.poll(() => report?.page).toBe('/dashboard');
  expect(report.message).toBe('The exercise button is hidden');
});

test('lesson feedback carries the exact exercise context', async ({ page }) => {
  let report: any = null;
  await mockApi(page, { completed: true });
  await page.route('**/api/beta/issue', async route => { report = route.request().postDataJSON(); return route.fulfill({ json: { ok: true } }); });
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: /Show example/i }).click();
  await page.getByRole('button', { name: /Start practice/i }).click();
  await page.getByRole('button', { name: /Report a problem/i }).click();
  await page.locator('.beta-report-backdrop textarea').fill('This dialogue prompt is unclear');
  await page.getByRole('button', { name: /^Send$/i }).click();
  await expect.poll(() => report?.exercise_index).toBe(0);
  expect(report).toMatchObject({ page: '/lesson/77', lesson_id: 77, exercise_type: 'dialogue', topic: 'konjunktiv_ii' });
});

for (const [language, heading] of [['ru', 'Твой урок'], ['de', 'Deine Lektion'], ['en', 'Your lesson']] as const) {
  test(`dashboard renders a complete ${language.toUpperCase()} interface`, async ({ page }) => {
    await mockApi(page, { completed: true, language });
    await page.goto('/dashboard');
    await expect(page.getByRole('heading', { name: heading })).toBeVisible();
    await expect(page.locator('html')).toHaveAttribute('lang', language);
    await expect(page.getByText(/WHAT TO IMPROVE|ЧТО УЛУЧШИТЬ|NÄCHSTER FOKUS/)).toBeVisible();
    await expectNoHorizontalOverflow(page);
  });
}

test('learner completes a production exercise and sees CEFR evidence', async ({ page }) => {
  await mockApi(page, { completed: true });
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: /Show example/i }).click();
  await page.getByRole('button', { name: /Start practice/i }).click();
  await page.getByRole('textbox').fill('Du solltest früher schlafen gehen, weil du oft müde bist.');
  await page.getByRole('button', { name: /^Check$/i }).click();
  await expect(page.getByText('B1 ASSESSMENT')).toBeVisible();
  await expect(page.getByText('82%')).toBeVisible();
  await page.locator('.answer-feedback > button').click();
  await expect(page.getByText('LESSON COMPLETE')).toBeVisible();
  await expect(page.getByRole('heading', { name: '100%' })).toBeVisible();
  await expectNoHorizontalOverflow(page);
});

test('practical reorder exercise is usable without mobile overflow', async ({ page }) => {
  await mockApi(page, { completed: true });
  await page.route('**/api/lesson/77', route => route.fulfill({ json: {
    ...lesson,
    content: {
      ...lesson.content,
      exercises: [{
        id: 'genitive-build', type: 'reorder', stage: 'guided',
        question: 'Build the sentence about the concert.',
        tokens: ['das', 'Konzert', 'des', 'statt', 'Regens', 'findet', 'Trotz'],
        hint: 'trotz + genitive: trotz des Regens',
      }],
    },
  }}));
  await page.goto('/lesson/77');
  await page.getByRole('button', { name: /Show example/i }).click();
  await page.getByRole('button', { name: /Start practice/i }).click();
  await expect(page.getByText('Tap the words in the correct order')).toBeVisible();
  for (const token of ['Trotz', 'des', 'Regens', 'findet', 'das', 'Konzert', 'statt']) {
    await page.locator('.reorder-bank').getByRole('button', { name: token, exact: true }).click();
  }
  await expect(page.locator('.reorder-built')).toContainText('Trotz des Regens findet das Konzert statt');
  await expect(page.getByRole('button', { name: /^Check$/i })).toBeEnabled();
  await expectNoHorizontalOverflow(page);
});

test('stale dashboard cache survives a bounded network failure without reload loops', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq-dashboard-9001', JSON.stringify({ savedAt: Date.now() - 60_000, value: { level: 'B1', targetLevel: 'B2', xp: 321, streak: 4, weaknesses: [] } })));
  let dashboardRequests = 0;
  await mockApi(page, { completed: true });
  await page.route('**/api/dashboard/**', async route => { dashboardRequests += 1; await route.abort('failed'); });
  await page.goto('/dashboard');
  await expect(page.locator('.rc-home-stats small')).toHaveText('321 XP');
  await expect.poll(() => dashboardRequests).toBe(2);
  await page.reload();
  await expect(page.locator('.rc-home-stats small')).toHaveText('321 XP');
  expect(dashboardRequests).toBeLessThanOrEqual(4);
});

test('Telegram BackButton owns nested navigation without duplicate browser control', async ({ page }) => {
  await page.route('https://telegram.org/js/telegram-web-app.js*', route => route.abort());
  await page.addInitScript(() => {
    const calls = { shown: 0, hidden: 0, handler: null as null | (() => void) };
    (window as any).__backCalls = calls;
    Object.defineProperty(window, 'Telegram', { configurable: false, writable: false, value: { WebApp: { platform: 'android', ready() {}, expand() {}, BackButton: { show() { calls.shown += 1; }, hide() { calls.hidden += 1; }, onClick(handler: () => void) { calls.handler = handler; }, offClick() { calls.handler = null; } } } } });
  });
  await mockApi(page, { completed: true });
  await page.goto('/lesson/77');
  await expect(page.locator('.app-back-button')).toHaveCount(0);
  await expect.poll(() => page.evaluate(() => (window as any).__backCalls.shown)).toBeGreaterThan(0);
});
