import { expect, Page, test } from '@playwright/test';

const userState = (completed: boolean) => ({ exists: completed, diagnostic_completed: completed, language: 'en', level: completed ? 'B1' : 'A1', xp: 120, streak: 3, beta_access: true, beta_onboarding_completed: true });
const nextLesson = { id: 77, topic: 'konjunktiv_ii', title: 'Konjunktiv II: advice', level: 'B1', reason: 'weakest_ready_skill' };
const today = (dueCount = 0) => ({ due_count: dueCount, next_lesson: nextLesson, session: { phases: [], minutes: 12 } });
const plan = [{ ...nextLesson, week: 2, track: 'B1', completed: false, blocked_by: [], recommended: true }];
const dashboard = { level: 'B1', targetLevel: 'B2', xp: 120, streak: 3, weaknesses: [{ name: 'konjunktiv_ii', score: 24 }] };
const lesson = {
  id: 77, level: 'B1', topic: 'konjunktiv_ii', estimated_time: 12, xp_reward: 70,
  content: { cefr: 'B1', title: 'Konjunktiv II: advice', objective: 'Give polite advice.', rule: 'Use sollte for advice.', examples: ['Du solltest früher schlafen gehen.'], common_mistakes: [], exercises: [] },
};

async function mockApi(page: Page, options: { completed?: boolean; dueCount?: number; reviews?: unknown[] } = {}) {
  await page.route('**/api/**', async route => {
    const { pathname } = new URL(route.request().url());
    if (pathname.includes('/api/user/state/')) return route.fulfill({ json: userState(options.completed ?? true) });
    if (pathname.includes('/api/learning/today/')) return route.fulfill({ json: today(options.dueCount ?? 0) });
    if (pathname.includes('/api/learning/reviews/')) return route.fulfill({ json: { reviews: options.reviews ?? [] } });
    if (pathname.includes('/api/dashboard/')) return route.fulfill({ json: dashboard });
    if (pathname.includes('/api/plan/')) return route.fulfill({ json: plan });
    if (pathname === '/api/lesson/start') return route.fulfill({ json: { session_id: 'test-session' } });
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
