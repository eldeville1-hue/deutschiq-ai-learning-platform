import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';
import './styles/product.css';
import { api } from './services/api';
import { getUserId } from './utils/user';

const bootStartedAt = performance.now();
const reloadKey = 'deutschiq-recent-startups';
let recentStarts: number[] = [];
try {
  recentStarts = JSON.parse(sessionStorage.getItem(reloadKey) || '[]')
    .filter((timestamp: number) => Date.now() - timestamp < 30_000);
  recentStarts.push(Date.now());
  sessionStorage.setItem(reloadKey, JSON.stringify(recentStarts.slice(-5)));
} catch { /* App startup must not depend on storage availability. */ }

const reportClientError = (kind: string, message: string) => {
  if (!getUserId()) return;
  void api.trackEvent({ user_id: getUserId(), event_name: 'client_error', properties: {
    kind, message: message.slice(0, 300), path: window.location.pathname,
  }});
};
window.addEventListener('error', event => reportClientError('error', event.message || 'unknown'));
window.addEventListener('unhandledrejection', event => reportClientError('unhandledrejection', String(event.reason || 'unknown')));

const telegram = (window as any).Telegram?.WebApp;
telegram?.ready();
telegram?.expand();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode><App /></React.StrictMode>
);

window.setTimeout(() => {
  if (!getUserId()) return;
  const properties = {
    path: window.location.pathname,
    platform: String(telegram?.platform || 'web'),
    startup_ms: Math.round(performance.now() - bootStartedAt),
    navigation: (performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined)?.type || 'unknown',
  };
  void api.trackEvent({ user_id: getUserId(), event_name: 'app_started', properties });
  if (recentStarts.length >= 3) {
    void api.trackEvent({ user_id: getUserId(), event_name: 'reload_loop_detected', properties: { ...properties, starts_30s: recentStarts.length } });
  }
}, 500);
