import React, { useEffect, useState } from 'react';
import { FaArrowRight } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { BrandMark } from '../components/BrandMark';

export const ReturningIntro: React.FC<{ level: string; introKey: string }> = ({ level, introKey }) => {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const [today, setToday] = useState<any>(null);
  const continueToDashboard = () => { sessionStorage.setItem(introKey, '1'); navigate(withUser('/dashboard'), { replace: true }); };

  useEffect(() => {
    api.getLearningToday(getUserId()).then(setToday).catch(() => undefined);
  }, []);

  const lesson = today?.next_lesson;
  return (
    <main className="returning-intro rc-returning">
      <header className="return-step return-step-1"><BrandMark label="DeutschIQ" /><span>DeutschIQ</span><b>{level}</b></header>
      <section className="rc-return-copy return-step return-step-2"><p>{lang === 'ru' ? 'С ВОЗВРАЩЕНИЕМ' : 'WILLKOMMEN ZURÜCK'}</p><h1>{lang === 'ru' ? 'Продолжим обучение' : 'Weiterlernen'}</h1><span>{lang === 'ru' ? 'Следующий урок уже готов.' : 'Deine nächste Lektion ist bereit.'}</span></section>
      <section className="return-lesson return-step return-step-3">
        <small>{lang === 'ru' ? 'СЛЕДУЮЩИЙ УРОК' : 'NÄCHSTE LEKTION'}</small>
        <b>{topicLabel(lesson?.topic || 'haben_conjugation', lang)}</b>
      </section>
      <button className="rc-primary return-step return-step-4" onClick={continueToDashboard}><span>{lang === 'ru' ? 'Продолжить' : 'Weiter'}</span><FaArrowRight /></button>
    </main>
  );
};
