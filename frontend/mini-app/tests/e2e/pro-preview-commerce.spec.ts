import { test, expect } from '@playwright/test';

test('Pro preview records interest without opening checkout during free beta', async ({ page }) => {
  const events: string[] = [];
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'ru'));
  await page.route('**/api/**', async route => {
    const { pathname } = new URL(route.request().url());
    if (pathname.startsWith('/api/dashboard/')) {
      return route.fulfill({ json: {
        subscription_status: 'free', beta_free: true, payments_enabled: true,
        commerce_ready: false, pro_price_stars: 700,
      } });
    }
    if (pathname === '/api/events') {
      const payload = route.request().postDataJSON();
      if (payload?.event_name) events.push(payload.event_name);
      return route.fulfill({ status: 204 });
    }
    return route.fulfill({ json: {} });
  });

  await page.goto('/pro');
  await expect(page.getByRole('button', { name: 'Мне интересен Pro' })).toBeVisible();
  await page.getByRole('button', { name: 'Мне интересен Pro' }).click();
  await expect(page.getByRole('status')).toContainText('платить не нужно');
  await expect.poll(() => events.includes('pro_interest_clicked')).toBe(true);
  await expect(page).toHaveURL(/\/pro(?:\?|$)/);
});

test('Pro preview does not offer checkout without legal seller readiness', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('deutschiq_lang', 'de'));
  await page.route('**/api/**', route => {
    const { pathname } = new URL(route.request().url());
    if (pathname.startsWith('/api/dashboard/')) return route.fulfill({ json: {
      beta_free: false, payments_enabled: true, commerce_ready: false, pro_price_stars: 700,
    } });
    return route.fulfill({ json: {} });
  });

  await page.goto('/pro');
  await expect(page.getByRole('button', { name: 'Ich interessiere mich für Pro' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Abo in Telegram öffnen' })).toHaveCount(0);
});
