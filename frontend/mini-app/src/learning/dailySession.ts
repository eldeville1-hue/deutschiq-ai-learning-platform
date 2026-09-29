export type DailySessionState = {
  nextLessonId: number;
  stage: 'review' | 'lesson';
  updatedAt: number;
};

const key = (userId: number) => `deutschiq-daily-session-${userId}`;
const MAX_AGE_MS = 24 * 60 * 60 * 1000;

export const readDailySession = (userId: number): DailySessionState | null => {
  try {
    const value = JSON.parse(localStorage.getItem(key(userId)) || 'null') as DailySessionState | null;
    if (!value || !value.nextLessonId || !['review', 'lesson'].includes(value.stage)) return null;
    if (Date.now() - Number(value.updatedAt || 0) > MAX_AGE_MS) {
      localStorage.removeItem(key(userId));
      return null;
    }
    return value;
  } catch {
    return null;
  }
};

export const saveDailySession = (
  userId: number,
  value: Omit<DailySessionState, 'updatedAt'>,
) => {
  try {
    localStorage.setItem(key(userId), JSON.stringify({ ...value, updatedAt: Date.now() }));
  } catch { /* The route still works when storage is unavailable. */ }
};

export const clearDailySession = (userId: number) => {
  try { localStorage.removeItem(key(userId)); } catch { /* Ignore unavailable storage. */ }
};
