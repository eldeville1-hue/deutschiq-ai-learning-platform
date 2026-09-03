import React from 'react';
import { FaArrowRight } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { withUser } from '../utils/user';

export const DiagnosticWelcome: React.FC = () => {
  const navigate = useNavigate();
  const { lang, setLanguage } = useLanguage();
  return (
    <main className="diagnostic-welcome">
      <div className="brand-mark intro-step intro-step-1">D</div>
      <p className="brand-name intro-step intro-step-2">DeutschIQ</p>
      <div className="welcome-message intro-step intro-step-3">
        <h1>{lang === 'ru' ? <>Немецкий, который<br />подстраивается под тебя.</> : <>Deutsch, das sich<br />an dich anpasst.</>}</h1>
        <p>{lang === 'ru' ? <>Определим твой уровень<br />и построим первый маршрут.</> : <>Wir bestimmen dein Niveau<br />und erstellen deinen ersten Lernweg.</>}</p>
      </div>
      <p className="diagnostic-meta intro-step intro-step-4">15 {lang === 'ru' ? 'вопросов' : 'Fragen'} · ~5 {lang === 'ru' ? 'минут' : 'Minuten'}</p>
      <button className="primary-action intro-step intro-step-5" onClick={() => navigate(withUser('/diagnostic'))}>
        {lang === 'ru' ? 'Начать диагностику' : 'Diagnose starten'} <FaArrowRight />
      </button>
      <button className="welcome-language intro-step intro-step-5" onClick={() => setLanguage(lang === 'ru' ? 'de' : 'ru')}>
        {lang === 'ru' ? 'Русский' : 'Deutsch'}
      </button>
    </main>
  );
};
