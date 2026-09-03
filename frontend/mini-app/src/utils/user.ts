export const getTelegramUser = () => (window as any).Telegram?.WebApp?.initDataUnsafe?.user;

export const getTelegramInitData = () => (window as any).Telegram?.WebApp?.initData || '';

export const hasTelegramIdentity = () => Boolean(getTelegramInitData() && getTelegramUser()?.id);

export const getUserId = () => {
  const devId = import.meta.env.DEV ? import.meta.env.VITE_DEV_USER_ID : undefined;
  return Number(getTelegramUser()?.id || devId || 0);
};

export const getUserName = () => getTelegramUser()?.first_name || '';

export const withUser = (path: string) => {
  return path;
};
