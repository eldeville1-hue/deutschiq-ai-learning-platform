import axios from 'axios';
import { getTelegramInitData, getUserId } from '../utils/user';
import type { AppLanguage } from '../i18n/language';

const API_BASE = '';

const apiClient = axios.create({
  baseURL: API_BASE,
  // Render free instances can need several seconds to wake up. A short timeout
  // made valid screens look broken before the server had a chance to answer.
  timeout: 35000,
});

apiClient.interceptors.request.use((config) => {
  (config as any).__startedAt = performance.now();
  const initData = getTelegramInitData();
  if (initData) config.headers['X-Telegram-Init-Data'] = initData;
  else if (import.meta.env.DEV && getUserId()) config.headers['X-Dev-User-Id'] = String(getUserId());
  return config;
});

const reportApiEvent = (eventName: 'api_failed' | 'api_slow', config: any, status = 0) => {
  if (config?.__telemetry || !getUserId()) return;
  const durationMs = Math.round(performance.now() - Number(config?.__startedAt || performance.now()));
  const properties = {
    path: String(config?.url || '').split('?')[0].slice(0, 160),
    method: String(config?.method || 'unknown').toUpperCase(),
    status,
    duration_ms: Math.max(0, durationMs),
    online: navigator.onLine,
  };
  void apiClient.post('/api/events', {
    user_id: getUserId(), event_name: eventName, properties,
  }, { __telemetry: true } as any).catch(() => undefined);
};

const CACHE_TTL = 5 * 60 * 1000;
const inFlightGets = new Map<string, Promise<unknown>>();

const readCache = (key: string) => {
  try { return localStorage.getItem(key); } catch { return null; }
};

const writeCache = (key: string, value: unknown) => {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* Private mode or full storage: network still works. */ }
};

const cachedGet = async <T>(key: string, request: () => Promise<T>, ttl = CACHE_TTL, allowStale = false): Promise<T> => {
  const stored = readCache(key);
  let staleValue: T | undefined;
  if (stored) {
    try {
      const cached = JSON.parse(stored);
      staleValue = cached.value as T;
      if (Date.now() - cached.savedAt < ttl) return staleValue;
    } catch { try { localStorage.removeItem(key); } catch { /* Ignore unavailable storage. */ } }
  }
  const existing = inFlightGets.get(key) as Promise<T> | undefined;
  if (existing) return existing;

  const pending = request()
    .then(value => {
      writeCache(key, { savedAt: Date.now(), value });
      return value;
    })
    .catch(error => {
      if (allowStale && staleValue !== undefined) return staleValue;
      throw error;
    })
    .finally(() => inFlightGets.delete(key));
  inFlightGets.set(key, pending);
  return pending;
};

const removeCached = (...prefixes: string[]) => {
  try {
    for (let index = localStorage.length - 1; index >= 0; index -= 1) {
      const key = localStorage.key(index);
      if (key && prefixes.some(prefix => key.startsWith(prefix))) localStorage.removeItem(key);
    }
  } catch { /* Cache invalidation must never block a learning action. */ }
};

const userCacheKey = (resource: string, userId: number, suffix = '') => `deutschiq-${resource}-${userId}${suffix}`;
const invalidateLearningData = (userId: number) => removeCached(
  userCacheKey('state', userId),
  userCacheKey('dashboard', userId),
  userCacheKey('plan', userId),
  userCacheKey('today', userId),
);

apiClient.interceptors.response.use(
  response => {
    const config = response.config as any;
    const durationMs = performance.now() - Number(config.__startedAt || performance.now());
    if (durationMs >= 3000) reportApiEvent('api_slow', config, response.status);
    return response;
  },
  async error => {
    const config = error.config as any;
    const retryable = config?.method === 'get' && !config.__deutschiqRetried && (!error.response || error.response.status >= 500);
    if (retryable) {
      config.__deutschiqRetried = true;
      await new Promise(resolve => window.setTimeout(resolve, 450));
      return apiClient(config);
    }
    reportApiEvent('api_failed', config, Number(error.response?.status || 0));
    console.error('❌ API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const api = {
  getVersion: () => apiClient.get('/api/version').then(r => r.data),
  trackEvent: (payload: { user_id: number; event_name: string; properties?: Record<string, string | number | boolean> }) =>
    apiClient.post('/api/events', payload).catch(() => undefined),
  submitBetaFeedback: (payload: { user_id: number; message: string; language: AppLanguage; page: string }) =>
    apiClient.post('/api/events', {
      user_id: payload.user_id,
      event_name: 'beta_feedback',
      properties: { message: payload.message, language: payload.language, page: payload.page },
    }),
  exportUserData: (userId: number) => apiClient.get(`/api/user-data/${userId}`).then(r => r.data),
  deleteUserData: (userId: number) => apiClient.delete(`/api/user-data/${userId}`),
  resetTestJourney: (userId: number) => apiClient.post(`/api/user-data/${userId}/reset-test`),
  getBetaControlCenter: (key: string, days = 30) => apiClient.get(`/api/internal/beta?days=${days}`, { headers: { 'X-Control-Key': key }, __telemetry: true } as any).then(r => r.data),
  createBetaInvite: (key: string, payload: { label: string; max_uses: number }) => apiClient.post('/api/internal/invites', payload, { headers: { 'X-Control-Key': key }, __telemetry: true } as any).then(r => r.data),
  createBetaInviteBatch: (key: string, payload: { label_prefix: string; count: number }) => apiClient.post('/api/internal/invites/batch', payload, { headers: { 'X-Control-Key': key }, __telemetry: true } as any).then(r => r.data),
  deactivateBetaInvite: (key: string, id: number) => apiClient.delete(`/api/internal/invites/${id}`, { headers: { 'X-Control-Key': key }, __telemetry: true } as any).then(r => r.data),
  claimBetaInvite: (payload: { user_id: number; code: string; language: AppLanguage }) => apiClient.post('/api/beta/claim', payload).then(r => { removeCached(userCacheKey('state', payload.user_id)); return r.data; }),
  completeBetaOnboarding: (payload: { user_id: number; goal: string; study_minutes: number; consent: boolean }) => apiClient.put('/api/beta/onboarding', payload).then(r => { removeCached(userCacheKey('state', payload.user_id)); return r.data; }),
  reportBetaIssue: (payload: { user_id: number; category: string; message: string; page: string; lesson_id?: number; exercise_index?: number; exercise_type?: string; topic?: string }) => apiClient.post('/api/beta/issue', payload).then(r => r.data),
  // Диагностика
  getQuestions: (lang: AppLanguage = 'en') => {
    return cachedGet(`deutschiq-questions-${lang}`, () => apiClient.get(`/api/diagnostic/questions?lang=${lang}`).then(r => r.data));
  },
  submitDiagnostic: (payload: { user_id: number; answers: Record<number, string>; language: AppLanguage }) => {
    return apiClient.post('/api/diagnostic/submit', payload).then(r => {
      invalidateLearningData(payload.user_id);
      return r.data;
    });
  },

  // Dashboard
  getDashboard: (userId: number) => {
    return cachedGet(userCacheKey('dashboard', userId), () => apiClient.get(`/api/dashboard/${userId}`).then(r => r.data), 30_000, true);
  },
  getUserState: (userId: number) => cachedGet(userCacheKey('state', userId), () => apiClient.get(`/api/user/state/${userId}`).then(r => r.data), 30_000, true),
  updateLanguage: (userId: number, language: AppLanguage) =>
    apiClient.put('/api/user/language', { user_id: userId, language }).then(r => {
      removeCached(userCacheKey('state', userId));
      return r.data;
    }),

  // Ошибки
  getMistakes: (userId: number, lang: AppLanguage) => {
    return apiClient.get(`/api/mistakes/${userId}?lang=${lang}`).then(r => r.data);
  },

  // План
  getPlan: (userId: number, lang?: AppLanguage, track?: string) => {
    const params = new URLSearchParams();
    if (lang) params.set('lang', lang);
    if (track) params.set('track', track);
    const suffix = params.toString() ? `?${params.toString()}` : '';
    return cachedGet(userCacheKey('plan', userId, `-${lang || 'default'}-${track || 'active'}`), () => apiClient.get(`/api/plan/${userId}${suffix}`).then(r => r.data), 30_000, true);
  },
  getJourney: (userId: number) => cachedGet(userCacheKey('journey', userId), () => apiClient.get(`/api/plan/journey/${userId}`).then(r => r.data), 30_000, true),
  getCheckpoint: (userId: number, level: string, lang?: AppLanguage) => apiClient.get(`/api/checkpoint/${userId}/${level}${lang ? `?lang=${lang}` : ''}`).then(r => r.data),
  submitCheckpoint: (payload: { user_id: number; level: string; answers: string[]; language: AppLanguage }) => apiClient.post('/api/checkpoint/submit', payload).then(r => r.data),

  // Уроки
  getLesson: (lessonId: number, lang: AppLanguage) => {
    return apiClient.get(`/api/lesson/${lessonId}?lang=${lang}`).then(r => r.data);
  },
  startLesson: (payload: { user_id: number; lesson_id: number }) => apiClient.post('/api/lesson/start', payload).then(r => r.data),
  completeLesson: (payload: { user_id: number; lesson_id: number; session_id: string }) => {
    return apiClient.post('/api/lesson/complete', payload).then(r => {
      invalidateLearningData(payload.user_id);
      return r.data;
    });
  },
  checkLessonAnswer: (payload: { user_id: number; lesson_id: number; exercise_index: number; answer: string; session_id: string; language: AppLanguage; confidence?: 'guess' | 'okay' | 'sure'; response_ms?: number }) =>
    apiClient.post('/api/lesson/check-answer', payload).then(r => r.data),
  transcribeSpeech: (payload: { user_id: number; lesson_id: number; exercise_index: number; session_id: string; audio: Blob }) => {
    const form = new FormData();
    form.append('user_id', String(payload.user_id));
    form.append('lesson_id', String(payload.lesson_id));
    form.append('exercise_index', String(payload.exercise_index));
    form.append('session_id', payload.session_id);
    const extension = payload.audio.type.includes('mp4') ? 'm4a' : payload.audio.type.includes('ogg') ? 'ogg' : 'webm';
    form.append('audio', payload.audio, `speech.${extension}`);
    return apiClient.post('/api/speech/transcribe', form, { timeout: 25000 }).then(r => r.data);
  },
  transcribeTutorSpeech: (userId: number, audio: Blob) => {
    const form = new FormData();
    form.append('user_id', String(userId));
    const extension = audio.type.includes('mp4') ? 'm4a' : audio.type.includes('ogg') ? 'ogg' : 'webm';
    form.append('audio', audio, `speech.${extension}`);
    return apiClient.post('/api/speech/tutor-transcribe', form, { timeout: 25000 }).then(r => r.data);
  },
  getSpeechProgress: (userId: number) => apiClient.get(`/api/speech/progress/${userId}`).then(r => r.data),

  // Learning engine
  getLearningToday: (userId: number, lang: AppLanguage) => cachedGet(userCacheKey('today', userId, `-${lang}`), () => apiClient.get(`/api/learning/today/${userId}?lang=${lang}`).then(r => r.data), 30_000, true),
  getReviews: (userId: number, lang: AppLanguage) => apiClient.get(`/api/learning/reviews/${userId}?lang=${lang}`).then(r => r.data),

  // AI-тьютор
  askTutor: (payload: { user_id: number; question: string; language: AppLanguage; history?: any[] }) => {
    return apiClient.post('/api/tutor/ask', payload).then(r => r.data);
  },
  getTutorState: (userId: number, lang: AppLanguage) => apiClient.get(`/api/tutor/state/${userId}?lang=${lang}`).then(r => r.data),

  // Достижения
  getBadges: (userId: number) => {
    return apiClient.get(`/api/badges/${userId}`).then(r => r.data);
  },

  // Статистика
  getStats: (userId: number) => {
    return apiClient.get(`/api/stats/${userId}`).then(r => r.data);
  },

  // Рефералы
  createReferral: (userId: number) => {
    return apiClient.post('/api/referral/create', { user_id: userId }).then(r => r.data);
  },
  claimReferral: (referrerId: number, refereeId: number) => {
    return apiClient.post('/api/referral/claim', { referrer_id: referrerId, referee_id: refereeId }).then(r => r.data);
  },
};
