import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaClock, FaLayerGroup } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const ReturningIntro: React.FC<{ level: string; introKey: string }> = ({ level, introKey }) => {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const [today, setToday] = useState<any>(null);
  const continueToDashboard = () => { sessionStorage.setItem(introKey, '1'); navigate(withUser('/dashboard'), { replace: true }); };

  useEffect(() => {
    api.getLearningToday(getUserId()).then(setToday).catch(() => undefined);
  }, []);

  const lesson = today?.next_lesson;
  const minutes = today?.session?.minutes || lesson?.minutes || 12;
  const phases = Array.isArray(today?.session?.phases) ? today.session.phases.length : 1;

  return (
    <main className="returning-intro rc-returning">
      <header className="return-step return-step-1"><div className="brand-mark">D</div><span>DeutschIQ</span><b>{level}</b></header>
      <section className="rc-return-copy return-step return-step-2"><p>{lang === 'ru' ? 'С ВОЗВРАЩЕНИЕМ' : 'WILLKOMMEN ZURÜCK'}</p><h1>{lang === 'ru' ? 'Продолжим с одного ясного шага' : 'Weiter mit einem klaren Schritt'}</h1><span>{lang === 'ru' ? 'План уже собран по твоим ответам и прогрессу.' : 'Dein Plan basiert bereits auf Antworten und Fortschritt.'}</span></section>
      <section className="return-lesson return-step return-step-3">
        <small>{lang === 'ru' ? 'ЗАДАНИЕ НА СЕГОДНЯ' : 'HEUTIGE AUFGABE'}</small>
        <b>{topicLabel(lesson?.topic || 'haben_conjugation', lang)}</b>
        <div><span><FaClock /> {minutes} {lang === 'ru' ? 'мин' : 'Min.'}</span><span><FaLayerGroup /> {phases} {lang === 'ru' ? 'этапа' : 'Schritte'}</span></div>
      </section>
      <button className="rc-primary return-step return-step-4" onClick={continueToDashboard}><span>{lang === 'ru' ? 'Открыть занятие' : 'Lektion öffnen'}</span><FaArrowRight /></button>
    </main>
  );
};
