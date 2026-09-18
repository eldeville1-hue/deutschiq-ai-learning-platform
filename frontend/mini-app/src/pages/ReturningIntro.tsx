import React, { useEffect, useState } from 'react';
import { FaArrowRight } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { BrandMark } from '../components/BrandMark';
import { tr } from '../i18n/language';

export const ReturningIntro: React.FC<{ level: string; introKey: string }> = ({ level, introKey }) => {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const [today, setToday] = useState<any>(null);
  const continueToDashboard = () => { sessionStorage.setItem(introKey, '1'); navigate(withUser('/dashboard'), { replace: true }); };

  useEffect(() => {
    api.getLearningToday(getUserId(), lang).then(setToday).catch(() => undefined);
  }, [lang]);

  const lesson = today?.next_lesson;
  return (
    <main className="returning-intro rc-returning">
      <header className="return-step return-step-1"><BrandMark label="DeutschIQ" /><span>DeutschIQ</span><b>{level}</b></header>
      <section className="rc-return-copy return-step return-step-2"><p>{tr(lang, 'С ВОЗВРАЩЕНИЕМ', 'WILLKOMMEN ZURÜCK', 'WELCOME BACK')}</p><h1>{tr(lang, 'Продолжим обучение', 'Weiterlernen', 'Keep learning')}</h1><span>{tr(lang, 'Следующий урок уже готов.', 'Deine nächste Lektion ist bereit.', 'Your next lesson is ready.')}</span></section>
      <section className="return-lesson return-step return-step-3">
        <small>{tr(lang, 'СЛЕДУЮЩИЙ УРОК', 'NÄCHSTE LEKTION', 'NEXT LESSON')}</small>
        <b>{topicLabel(lesson?.topic || 'haben_conjugation', lang)}</b>
      </section>
      <button className="rc-primary return-step return-step-4" onClick={continueToDashboard}><span>{tr(lang, 'Продолжить', 'Weiter', 'Continue')}</span><FaArrowRight /></button>
    </main>
  );
};
