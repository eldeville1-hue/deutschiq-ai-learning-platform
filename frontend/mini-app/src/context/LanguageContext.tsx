// frontend/mini-app/src/context/LanguageContext.tsx
import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import { api } from '../services/api';
import { getTelegramUser, getUserId } from '../utils/user';
import { normalizeLanguage } from '../i18n/language';
import type { AppLanguage } from '../i18n/language';

const META_COPY: Record<AppLanguage, { title: string; description: string }> = {
  ru: {
    title: 'DeutschIQ · Персональное изучение немецкого',
    description: 'Диагностика, персональный маршрут и ИИ-репетитор для изучения немецкого в Telegram.',
  },
  de: {
    title: 'DeutschIQ · Personalisiertes Deutschlernen',
    description: 'Einstufung, persönlicher Lernweg und KI-Tutor zum Deutschlernen in Telegram.',
  },
  en: {
    title: 'DeutschIQ · Adaptive German Learning',
    description: 'Placement, a personal learning path and an AI tutor for learning German in Telegram.',
  },
};

interface LanguageContextType {
  lang: AppLanguage;
  setLanguage: (language: AppLanguage, persist?: boolean) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [lang, setLang] = useState<AppLanguage>(() => {
    const saved = localStorage.getItem('deutschiq_lang');
    if (saved) return normalizeLanguage(saved);
    return normalizeLanguage(getTelegramUser()?.language_code);
  });
  const initialLanguage = useRef(lang);

  const setLanguage = useCallback((language: AppLanguage, persist = true) => {
    setLang(language);
    localStorage.setItem('deutschiq_lang', language);
    if (persist) api.updateLanguage(getUserId(), language).catch(() => undefined);
  }, []);

  useEffect(() => {
    const userId = getUserId();
    if (!userId) return;
    api.getUserState(userId).then(state => {
      if (state.exists) setLanguage(normalizeLanguage(state.language), false);
      else setLanguage(initialLanguage.current, true);
    }).catch(() => undefined);
  }, [setLanguage]);

  useEffect(() => {
    const metadata = META_COPY[lang];
    document.documentElement.lang = lang;
    document.title = metadata.title;
    document.querySelector<HTMLMetaElement>('meta[name="description"]')?.setAttribute('content', metadata.description);
    document.querySelector<HTMLMetaElement>('meta[property="og:description"]')?.setAttribute('content', metadata.description);
  }, [lang]);
  return (
    <LanguageContext.Provider value={{ lang, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage must be used within LanguageProvider');
  return context;
};
