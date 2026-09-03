import React, { useEffect, useState } from 'react';
import { FaArrowRight } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const ReturningIntro: React.FC<{ level: string; introKey: string }> = ({ level, introKey }) => {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const [topic, setTopic] = useState('haben_conjugation');
  const continueToDashboard = () => { sessionStorage.setItem(introKey, '1'); navigate(withUser('/dashboard'), { replace: true }); };

  useEffect(() => {
    api.getDashboard(getUserId()).then((data) => setTopic(data?.weaknesses?.[0]?.name || 'haben_conjugation')).catch(() => undefined);
    const timer = window.setTimeout(continueToDashboard, 1400);
    return () => window.clearTimeout(timer);
  }, []);

  return (
    <main className="returning-intro">
      <div className="brand-mark return-step return-step-1">D</div>
      <h1 className="return-step return-step-2">{lang === 'ru' ? 'С возвращением.' : 'Willkommen zurück.'}</h1>
      <div className="return-level return-step return-step-3"><span>{lang === 'ru' ? 'Твой уровень' : 'Dein Niveau'}</span><strong>{level}</strong></div>
      <p className="return-copy return-step return-step-3">{lang === 'ru' ? <>Сегодня продолжим<br />с самого важного.</> : <>Heute geht es mit dem<br />Wichtigsten weiter.</>}</p>
      <div className="return-lesson return-step return-step-4">
        <small>{lang === 'ru' ? 'СЕГОДНЯ' : 'HEUTE'} · 12 {lang === 'ru' ? 'МИН' : 'MIN.'}</small>
        <b>{topicLabel(topic, lang)}</b>
        <span>3 {lang === 'ru' ? 'коротких задания' : 'kurze Aufgaben'}</span>
      </div>
      <button className="primary-action return-step return-step-4" onClick={continueToDashboard}>{lang === 'ru' ? 'Продолжить' : 'Weiter'} <FaArrowRight /></button>
    </main>
  );
};
