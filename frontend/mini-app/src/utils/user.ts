type TelegramUser = {
  id: number;
  first_name?: string;
  last_name?: string;
  username?: string;
  language_code?: string;
};

const telegramWebApp = () => (window as any).Telegram?.WebApp;

export const getTelegramInitData = () => telegramWebApp()?.initData || '';

const getUserFromInitData = (): TelegramUser | undefined => {
  const initData = getTelegramInitData();
  if (!initData) return undefined;

  try {
    const rawUser = new URLSearchParams(initData).get('user');
    if (!rawUser) return undefined;
    const parsed = JSON.parse(rawUser) as TelegramUser;
    return parsed?.id ? parsed : undefined;
  } catch {
    return undefined;
  }
};

export const getTelegramUser = (): TelegramUser | undefined => {
  const unsafeUser = telegramWebApp()?.initDataUnsafe?.user as TelegramUser | undefined;
  if (unsafeUser?.id) return unsafeUser;

  // Some Telegram clients expose the signed initData before initDataUnsafe.user
  // is populated. Reading the user from the signed payload keeps startup robust;
  // the backend still validates the Telegram signature on every API request.
  return getUserFromInitData();
};

export const hasTelegramIdentity = () => Boolean(getTelegramInitData() && getTelegramUser()?.id);

export const getUserId = () => {
  const devId = import.meta.env.DEV ? import.meta.env.VITE_DEV_USER_ID : undefined;
  return Number(getTelegramUser()?.id || devId || 0);
};

export const getUserName = () => getTelegramUser()?.first_name || '';

export const withUser = (path: string) => path;
