// frontend/mini-app/src/context/LanguageContext.tsx
import React, { createContext, useContext, useState } from 'react';
import { api } from '../services/api';
import { getTelegramUser, getUserId } from '../utils/user';

type Language = 'de' | 'ru';

interface LanguageContextType {
  lang: Language;
  toggleLang: () => void;
  setLanguage: (language: Language, persist?: boolean) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [lang, setLang] = useState<Language>(() => {
    const saved = localStorage.getItem('deutschiq_lang') as Language;
    if (saved === 'ru' || saved === 'de') return saved;
    return getTelegramUser()?.language_code === 'de' ? 'de' : 'ru';
  });

  const setLanguage = (language: Language, persist = true) => {
    setLang(language);
    localStorage.setItem('deutschiq_lang', language);
    if (persist) api.updateLanguage(getUserId(), language).catch(() => undefined);
  };
  const toggleLang = () => setLanguage(lang === 'de' ? 'ru' : 'de');

  return (
    <LanguageContext.Provider value={{ lang, toggleLang, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage must be used within LanguageProvider');
  return context;
};
