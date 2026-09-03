import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaArrowRight, FaCheck, FaGlobe, FaGraduationCap } from 'react-icons/fa';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { getUserId, getUserName, withUser } from '../utils/user';
import { topicLabel } from '../i18n/topics';

type UserState = { diagnostic_completed: boolean; language: 'ru' | 'de'; level: string };

export const Welcome: React.FC = () => {
  const navigate = useNavigate();
  const { lang, setLanguage } = useLanguage();
  const [state, setState] = useState<UserState | null>(null);
  const [weakness, setWeakness] = useState('articles');
  const userId = getUserId();
  const name = getUserName() || (lang === 'ru' ? 'ученик' : 'Lernende');

  useEffect(() => {
    api.getUserState(userId).then((value) => {
      const remoteLang = value.language === 'de' ? 'de' : 'ru';
      setLanguage(remoteLang, false);
      setState(value);
      if (value.diagnostic_completed) {
        api.getDashboard(userId).then(d => setWeakness(d?.weaknesses?.[0]?.name || 'articles')).catch(() => undefined);
      }
    }).catch(() => setState({ diagnostic_completed: false, language: lang, level: 'A1' }));
  }, [userId]);

  if (!state) return <div className="app-shell bootstrap"><div className="brand-mark">D</div><div className="analysis-loader" /></div>;

  if (state.diagnostic_completed) {
    return (
      <main className="welcome-screen fade-up">
        <div className="brand-mark">D</div>
        <p className="eyebrow">DeutschIQ</p>
        <h1>{lang === 'ru' ? `С возвращением, ${name}` : `Willkommen zurück, ${name}`}</h1>
        <div className="welcome-summary">
          <span>{lang === 'ru' ? 'Твой уровень' : 'Dein Niveau'}</span>
          <strong>{state.level || 'A1'}</strong>
          <p>{lang === 'ru' ? 'Сегодня продолжим: ' : 'Heute geht es weiter mit: '}<b>{topicLabel(weakness, lang)}</b></p>
        </div>
        <button className="primary-action" onClick={() => navigate(withUser('/dashboard'))}>
          {lang === 'ru' ? 'Продолжить обучение' : 'Weiterlernen'} <FaArrowRight />
        </button>
      </main>
    );
  }

  return (
    <main className="welcome-screen fade-up">
      <div className="brand-mark">D</div>
      <p className="eyebrow">DeutschIQ</p>
      <h1>{lang === 'ru' ? 'Немецкий по твоему уровню' : 'Deutsch auf deinem Niveau'}</h1>
      <p className="welcome-copy">{lang === 'ru' ? 'Определим уровень, найдём слабые темы и составим персональный план.' : 'Wir bestimmen dein Niveau, finden Lücken und erstellen deinen persönlichen Lernplan.'}</p>
      <div className="onboarding-points">
        <span><FaCheck /> {lang === 'ru' ? '15 коротких вопросов' : '15 kurze Fragen'}</span>
        <span><FaGraduationCap /> {lang === 'ru' ? 'Персональный план после теста' : 'Persönlicher Plan nach dem Test'}</span>
      </div>
      <div className="language-choice" aria-label={lang === 'ru' ? 'Язык интерфейса' : 'App-Sprache'}>
        <FaGlobe />
        <button className={lang === 'ru' ? 'active' : ''} onClick={() => setLanguage('ru')}>Русский</button>
        <button className={lang === 'de' ? 'active' : ''} onClick={() => setLanguage('de')}>Deutsch</button>
      </div>
      <button className="primary-action" onClick={() => navigate(withUser('/diagnostic'))}>
        {lang === 'ru' ? 'Начать диагностику' : 'Diagnose starten'} <FaArrowRight />
      </button>
    </main>
  );
};
