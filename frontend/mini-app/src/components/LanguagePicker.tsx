import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { SUPPORTED_LANGUAGES } from '../i18n/language';

type Props = { compact?: boolean; className?: string };

export const LanguagePicker: React.FC<Props> = ({ compact = false, className = '' }) => {
  const { lang, setLanguage } = useLanguage();
  return (
    <div className={`language-picker${compact ? ' compact' : ''}${className ? ` ${className}` : ''}`} role="group" aria-label="Language · Sprache · Язык">
      {SUPPORTED_LANGUAGES.map(item => (
        <button
          key={item.code}
          type="button"
          className={lang === item.code ? 'active' : ''}
          aria-pressed={lang === item.code}
          aria-label={item.label}
          onClick={() => setLanguage(item.code)}
        >
          {compact ? item.short : item.label}
        </button>
      ))}
    </div>
  );
};
