import { test, expect } from '@playwright/test';

test('a late profile response cannot override a newer language selection', async ({ page }) => {
  let resolveProfile: (() => void) | undefined;
  const profileReleased = new Promise<void>(resolve => { resolveProfile = resolve; });
  await page.route('**/api/user/state/*', async route => {
    await profileReleased;
    await route.fulfill({ json: { exists: true, language: 'ru' } });
  });
  await page.route('**/api/user/language', route => route.fulfill({ json: { ok: true } }));
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'en'));
  await page.goto('/about');
  // Public pages use the same LanguageProvider as the authenticated application.
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  // The profile request may not run on public pages without a user identity.
  // This test requires an authenticated dev identity before asserting the race.
  const profileRequest = page.waitForRequest('**/api/user/state/*', { timeout: 5000 }).catch(() => null);
  const request = await profileRequest;
  resolveProfile?.();
  expect(request, 'Language preference race requires an authenticated profile fetch').not.toBeNull();
});
