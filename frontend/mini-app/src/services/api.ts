import axios from 'axios';
import { getTelegramInitData, getUserId } from '../utils/user';

const API_BASE = '';

console.log('🔍 API_BASE =', API_BASE);

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 4500,
});

apiClient.interceptors.request.use((config) => {
  const initData = getTelegramInitData();
  if (initData) config.headers['X-Telegram-Init-Data'] = initData;
  else if (import.meta.env.DEV && getUserId()) config.headers['X-Dev-User-Id'] = String(getUserId());
  return config;
});

const CACHE_TTL = 5 * 60 * 1000;
const cachedGet = async <T>(key: string, request: () => Promise<T>): Promise<T> => {
  const stored = localStorage.getItem(key);
  if (stored) {
    try {
      const cached = JSON.parse(stored);
      if (Date.now() - cached.savedAt < CACHE_TTL) return cached.value as T;
    } catch { localStorage.removeItem(key); }
  }
  const value = await request();
  localStorage.setItem(key, JSON.stringify({ savedAt: Date.now(), value }));
  return value;
};

apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('❌ API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const api = {
  // Диагностика
  getQuestions: (lang: string = 'ru') => {
    return cachedGet(`deutschiq-questions-${lang}`, () => apiClient.get(`/api/diagnostic/questions?lang=${lang}`).then(r => r.data));
  },
  submitDiagnostic: (payload: { user_id: number; answers: Record<number, string> }) => {
    return apiClient.post('/api/diagnostic/submit', payload).then(r => r.data);
  },

  // Dashboard
  getDashboard: (userId: number) => {
    return apiClient.get(`/api/dashboard/${userId}`).then(r => r.data);
  },
  getUserState: (userId: number) => apiClient.get(`/api/user/state/${userId}`).then(r => r.data),
  updateLanguage: (userId: number, language: 'ru' | 'de') =>
    apiClient.put('/api/user/language', { user_id: userId, language }).then(r => r.data),

  // Ошибки
  getMistakes: (userId: number) => {
    return apiClient.get(`/api/mistakes/${userId}`).then(r => r.data);
  },

  // План
  getPlan: (userId: number) => {
    return apiClient.get(`/api/plan/${userId}`).then(r => r.data);
  },

  // Уроки
  getLesson: (lessonId: number) => {
    return apiClient.get(`/api/lesson/${lessonId}`).then(r => r.data);
  },
  startLesson: (payload: { user_id: number; lesson_id: number }) => apiClient.post('/api/lesson/start', payload).then(r => r.data),
  completeLesson: (payload: { user_id: number; lesson_id: number; session_id: string }) => {
    return apiClient.post('/api/lesson/complete', payload).then(r => r.data);
  },
  checkLessonAnswer: (payload: { user_id: number; lesson_id: number; exercise_index: number; answer: string; session_id: string; confidence?: 'guess' | 'okay' | 'sure'; response_ms?: number }) =>
    apiClient.post('/api/lesson/check-answer', payload).then(r => r.data),

  // Learning engine
  getLearningToday: (userId: number) => apiClient.get(`/api/learning/today/${userId}`).then(r => r.data),
  getReviews: (userId: number) => apiClient.get(`/api/learning/reviews/${userId}`).then(r => r.data),

  // AI-тьютор
  askTutor: (payload: { user_id: number; question: string; history?: any[] }) => {
    return apiClient.post('/api/tutor/ask', payload).then(r => r.data);
  },
  getTutorState: (userId: number) => apiClient.get(`/api/tutor/state/${userId}`).then(r => r.data),

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
