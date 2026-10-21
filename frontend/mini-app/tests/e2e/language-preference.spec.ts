import { test, expect } from '@playwright/test';

test('a late profile response cannot override a newer language selection', async ({ page }) => {
  let releaseProfile!: () => void;
  const profileReleased = new Promise<void>(resolve => { releaseProfile = resolve; });
  let profileRequested!: () => void;
  const requestStarted = new Promise<void>(resolve => { profileRequested = resolve; });

  await page.route('**/api/user/state/*', async route => {
    profileRequested();
    await profileReleased;
    await route.fulfill({ json: { exists: true, language: 'ru' } });
  });
  await page.route('**/api/dashboard/*', route => route.fulfill({ json: { level: 'A1', xp: 0, streak: 0 } }));
  await page.route('**/api/plan/*', route => route.fulfill({ json: [] }));
  await page.route('**/api/user/language', route => route.fulfill({ json: { ok: true } }));
  await page.route('**/api/events', route => route.fulfill({ json: {} }));
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));

  await page.goto('/profile');
  await requestStarted;
  const picker = page.getByRole('group', { name: 'Language · Sprache · Язык' });
  await picker.getByRole('button', { name: 'Deutsch' }).click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'de');
  releaseProfile();
  await expect(page.locator('html')).toHaveAttribute('lang', 'de');
  await expect(picker.getByRole('button', { name: 'Deutsch' })).toHaveAttribute('aria-pressed', 'true');
});
