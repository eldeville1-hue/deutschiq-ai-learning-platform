export type AppLanguage = 'ru' | 'de' | 'en';

export const SUPPORTED_LANGUAGES: ReadonlyArray<{ code: AppLanguage; short: string; label: string }> = [
  { code: 'de', short: 'DE', label: 'Deutsch' },
  { code: 'en', short: 'EN', label: 'English' },
  { code: 'ru', short: 'RU', label: 'Русский' },
];

export const normalizeLanguage = (value?: string | null): AppLanguage => {
  const code = String(value || '').toLowerCase().split(/[-_]/)[0];
  return code === 'de' || code === 'en' || code === 'ru' ? code : 'en';
};

export const tr = (lang: AppLanguage, ru: string, de: string, en: string): string => (
  lang === 'ru' ? ru : lang === 'de' ? de : en
);

export const languageLabel = (lang: AppLanguage): string => (
  SUPPORTED_LANGUAGES.find(item => item.code === lang)?.label || 'English'
);
