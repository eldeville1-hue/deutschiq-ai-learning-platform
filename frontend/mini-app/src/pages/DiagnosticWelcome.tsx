import React from 'react';
import { FaArrowRight } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { withUser } from '../utils/user';
import { BrandMark } from '../components/BrandMark';
import { LanguagePicker } from '../components/LanguagePicker';
import { tr } from '../i18n/language';

export const DiagnosticWelcome: React.FC = () => {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  return (
    <main className="diagnostic-welcome">
      <BrandMark className="welcome-brand intro-step intro-step-1" label="DeutschIQ" />
      <p className="brand-name intro-step intro-step-2">DeutschIQ</p>
      <div className="welcome-message intro-step intro-step-3">
        <h1>{tr(lang, 'Немецкий, который подстраивается под тебя.', 'Deutsch, das sich an dich anpasst.', 'German that adapts to you.')}</h1>
        <p>{tr(lang, 'Определим твой уровень и построим первый маршрут.', 'Wir bestimmen dein Niveau und erstellen deinen ersten Lernweg.', 'Find your level and get a personal learning path.')}</p>
      </div>
      <p className="diagnostic-meta intro-step intro-step-4">15 {tr(lang, 'вопросов', 'Fragen', 'questions')}</p>
      <button className="primary-action intro-step intro-step-5" onClick={() => navigate(withUser('/diagnostic'))}>
        {tr(lang, 'Определить уровень', 'Niveau bestimmen', 'Find my level')} <FaArrowRight />
      </button>
      <LanguagePicker compact className="intro-step intro-step-5" />
    </main>
  );
};
