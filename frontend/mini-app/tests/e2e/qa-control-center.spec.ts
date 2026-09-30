import { expect, Page, test } from '@playwright/test';

const betaData = {
  audience: { total_users: 12, new_users: 3, active_learners: 7, languages: { ru: 7, de: 5 } },
  funnel: { completion_rate: 71, lesson_completed: 5, invite_claimed: 9, onboarding_completed: 8, diagnostic_started: 8, diagnostic_completed: 7, lesson_started: 7 },
  sessions: { abandoned_events: 1, started: 7 },
  events: { reliability: {}, learning_modes: [], feedback: [] },
  exercise_health: [], retention: { d1: { rate: 70, eligible: 10 }, d3: { rate: 55, eligible: 8 }, d7: { rate: 40, eligible: 5 } },
  beta: { enrolled: 9, onboarded: 8, invites: [] }, testers: [],
};

const catalog = [
  { id: 1, level: 'A1', day: 1, title: 'Say where you are from' },
  { id: 2, level: 'A2', day: 1, title: 'Plan a meeting' },
  { id: 3, level: 'B1', day: 1, title: 'Explain a decision' },
  { id: 4, level: 'B2', day: 1, title: 'Defend a proposal' },
].map(item => ({ ...item, publish_ready: true, publication_blockers: [], reviewed_languages: ['ru', 'de'], delayed_review_method: 'changed_context_retrieval' }));

const lesson = (id: number, lang: string) => ({
  id, level: catalog.find(item => item.id === id)?.level || 'A1', pillar: 'Communication',
  content: {
    title: lang === 'de' ? 'Sagen, woher du kommst' : 'Рассказать, откуда ты',
    scenario: lang === 'de' ? 'Jemand im Kurs fragt, woher du kommst.' : 'Кто-то на курсе спрашивает, откуда ты.',
    objective: lang === 'de' ? 'Du kannst dich kurz vorstellen.' : 'Ты можешь коротко представиться.',
    success_evidence: lang === 'de' ? 'Du kannst kurz sagen, woher du kommst und wo du wohnst.' : 'Ты можешь коротко сказать, откуда ты и где живёшь.',
    exercises: [{ id: 'qa-1', type: 'short_answer', question: lang === 'de' ? 'Woher kommst du?' : 'Откуда ты?', explanation: 'Use: Ich komme aus …', answer: 'Ich komme aus Kyiv.' }],
  },
});

async function mockOwnerApi(page: Page) {
  const writes: string[] = [];
  await page.route('**/api/internal/**', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (request.method() !== 'GET') writes.push(`${request.method()} ${url.pathname}`);
    if (request.headers()['x-control-key'] !== 'owner-test-key') return route.fulfill({ status: 403, json: { detail: 'Invalid control-center key' } });
    if (url.pathname === '/api/internal/beta') return route.fulfill({ json: betaData });
    if (url.pathname === '/api/internal/curriculum') return route.fulfill({ json: catalog });
    const match = url.pathname.match(/\/api\/internal\/curriculum\/(\d+)/);
    if (match) return route.fulfill({ json: lesson(Number(match[1]), url.searchParams.get('lang') || 'ru') });
    return route.fulfill({ status: 404, json: {} });
  });
  return writes;
}

async function unlock(page: Page) {
  await page.goto('/control-center');
  await expect(page.getByRole('heading', { name: 'Owner quality center' })).toBeVisible();
  await expect(page.getByTestId('qa-lab')).toHaveCount(0);
  await page.getByPlaceholder('Owner access key').fill('owner-test-key');
  await page.getByRole('button', { name: 'Open quality center' }).click();
  await expect(page.getByTestId('qa-lab')).toBeVisible();
}

test('owner QA stays protected and performs no learner writes', async ({ page }) => {
  const writes = await mockOwnerApi(page);
  await unlock(page);
  await expect(page.getByText('Ready to publish')).toBeVisible();
  await expect(page.getByText('RU copy reviewed')).toBeVisible();
  await expect(page.getByText('Changed-context review')).toBeVisible();
  await page.getByLabel('Learner state').selectOption('graduation');
  await page.getByLabel('Preview screen').selectOption('checkpoint');
  await page.getByLabel('Interface state').selectOption('pass');
  await expect(page.getByText('A1 ✓ · 0% → A2')).toBeVisible();
  await page.getByLabel('Interface state').selectOption('fail');
  await expect(page.getByText(/Порядок слов/)).toBeVisible();
  expect(writes).toEqual([]);
});

test('QA matrix renders RU and DE recovery states at every supported width', async ({ page }, testInfo) => {
  // The quality center is an owner workspace: give its controls enough room while
  // the nested device keeps the exact learner viewport under test.
  await page.setViewportSize({ width: 1280, height: 1000 });
  await mockOwnerApi(page);
  await unlock(page);
  await page.getByLabel('Preview screen').selectOption('overview');
  for (const width of [320, 360, 390, 430]) {
    await page.getByLabel('Preview width').selectOption(String(width));
    const device = page.getByTestId('qa-device');
    await expect(device).toHaveCSS('width', `${width}px`);
    await expect.poll(() => device.evaluate(node => node.scrollWidth <= node.clientWidth)).toBe(true);
    await testInfo.attach(`overview-ru-${width}.png`, { body: await device.screenshot(), contentType: 'image/png' });
  }
  await page.getByLabel('Preview language').selectOption('de');
  await page.getByLabel('Interface state').selectOption('offline');
  await expect(page.getByText('Keine Verbindung')).toBeVisible();
  await page.getByLabel('Interface state').selectOption('mic_denied');
  await expect(page.getByText('Mikrofon nicht verfügbar')).toBeVisible();
  await page.getByLabel('Keyboard').check();
  await expect(page.locator('.qa-keyboard')).toBeVisible();
});

test('QA lesson uses real exercise and completion components', async ({ page }) => {
  await mockOwnerApi(page);
  await unlock(page);
  await page.getByLabel('Preview screen').selectOption('lesson');
  await expect(page.getByText('Откуда ты?')).toBeVisible();
  await page.getByLabel('Interface state').selectOption('wrong');
  await expect(page.getByText('Исправь только эту часть')).toBeVisible();
  await page.getByLabel('Interface state').selectOption('complete');
  await expect(page.getByText('МИССИЯ ВЫПОЛНЕНА')).toBeVisible();
  await expect(page.getByText('Это уже твой немецкий')).toBeVisible();
});
