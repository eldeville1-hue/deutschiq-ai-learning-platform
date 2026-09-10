import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaBolt, FaBrain, FaClock, FaCommentDots, FaExclamation, FaFire, FaPlay, FaRedoAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const Dashboard: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [lesson, setLesson] = useState<any>(null);
  const [learning, setLearning] = useState<any>(null);
  const [loadError, setLoadError] = useState(false);
  const userId = getUserId();

  useEffect(() => {
    void api.trackEvent({ user_id: userId, event_name: 'dashboard_viewed' });
    Promise.allSettled([api.getDashboard(userId), api.getPlan(userId), api.getLearningToday(userId)]).then(([dashboard, plan, today]) => {
      if (dashboard.status === 'fulfilled') setData(dashboard.value);
      else {
        setData({ level: 'A1', targetLevel: 'A2', xp: 0, streak: 0, weaknesses: [] });
        setLoadError(true);
      }
      if (plan.status === 'fulfilled') {
        const items = Array.isArray(plan.value) ? plan.value : [];
        setLesson(items.find((item: any) => !item.completed) || items[0]);
      }
      if (today.status === 'fulfilled') setLearning(today.value);
    });
  }, [userId]);

  if (!data) return <main className="app-shell"><div className="skeleton action-hero-skeleton" /></main>;
  const selectedLesson = learning?.next_lesson || lesson;
  const topic = selectedLesson?.topic || data.weaknesses?.[0]?.name || 'haben_conjugation';
  const weak = data.weaknesses?.[0] || { name: 'articles', percent: 10 };
  const hour = new Date().getHours();
  const greeting = lang === 'ru'
    ? (hour < 12 ? 'ДОБРОЕ УТРО' : hour < 18 ? 'ДОБРЫЙ ДЕНЬ' : 'ДОБРЫЙ ВЕЧЕР')
    : (hour < 12 ? 'GUTEN MORGEN' : hour < 18 ? 'GUTEN TAG' : 'GUTEN ABEND');
  const startLesson = () => navigate(selectedLesson?.id ? withUser(`/lesson/${selectedLesson.id}`) : withUser('/plan'));
  const phases = Array.isArray(learning?.session?.phases) ? learning.session.phases : [];

  const minutes = learning?.session?.minutes || selectedLesson?.minutes || 12;
  return (
    <main className="app-shell v29-home page-enter">
      <header className="v29-topbar">
        <div className="v29-identity"><span className="v29-logo">D</span><div><small>{greeting}</small><strong>DeutschIQ</strong></div></div>
        <div className="v29-stats"><span><b>{data.level || 'A1'}</b>{data.xp || 0} XP</span><span><FaFire /><b>{data.streak || 0}</b></span></div>
      </header>
      {loadError && <div className="v31-status error"><span>{lang === 'ru' ? 'Не удалось обновить данные' : 'Daten konnten nicht aktualisiert werden'}</span><button type="button" onClick={() => window.location.reload()}>{lang === 'ru' ? 'Повторить' : 'Erneut laden'}</button></div>}
      <section className="v29-heading"><span>{lang === 'ru' ? 'ТВОЙ СЛЕДУЮЩИЙ ШАГ' : 'DEIN NÄCHSTER SCHRITT'}</span><h1>{lang === 'ru' ? 'Сегодня учимся уверенно' : 'Heute sicherer werden'}</h1></section>
      <section className="v29-focus-card">
        <div className="v29-focus-label"><span><FaBolt />{lang === 'ru' ? 'Персональный урок' : 'Persönliche Lektion'}</span><b>01</b></div>
        <h2>{topicLabel(topic, lang)}</h2>
        <p>{selectedLesson?.reason === 'review_due' ? (lang === 'ru' ? 'Короткое повторение поможет закрепить тему.' : 'Eine kurze Wiederholung festigt das Thema.') : (lang === 'ru' ? 'Урок выбран по твоему уровню и последним ошибкам.' : 'Nach deinem Niveau und deinen letzten Fehlern gewählt.')}</p>
        <div className="v29-focus-meta"><span><FaClock />{minutes} {lang === 'ru' ? 'мин' : 'Min.'}</span><span><FaBrain />{learning?.due_count || 0} {lang === 'ru' ? 'повторить' : 'fällig'}</span></div>
        <button type="button" className="v29-primary" onClick={startLesson}><span><FaPlay />{lang === 'ru' ? 'Начать урок' : 'Lektion starten'}</span><FaArrowRight /></button>
      </section>
      {phases.length > 0 && <section className="v29-agenda">
        <header><div><span>{lang === 'ru' ? 'СЕГОДНЯ' : 'HEUTE'}</span><h2>{lang === 'ru' ? 'План занятия' : 'Dein Lernplan'}</h2></div><b>{minutes} {lang === 'ru' ? 'мин' : 'Min.'}</b></header>
        <div className="v29-agenda-list">{phases.slice(0, 3).map((phase: any, index: number) => <div className="v29-agenda-row" key={`${phase.kind}-${index}`}>
          <i>{phase.kind === 'review' ? <FaRedoAlt /> : phase.kind === 'transfer' ? <FaCommentDots /> : <FaBrain />}</i>
          <div><strong>{phase.kind === 'review' ? (lang === 'ru' ? `Повторить ${phase.count} тем` : `${phase.count} Themen wiederholen`) : phase.kind === 'transfer' ? (lang === 'ru' ? 'Применить в своей фразе' : 'Im eigenen Satz anwenden') : topicLabel(phase.topic || topic, lang)}</strong><small>{phase.kind === 'transfer' ? (lang === 'ru' ? 'Практика речи' : 'Sprechpraxis') : (lang === 'ru' ? 'Изучение и практика' : 'Lernen und üben')}</small></div>
          <span>{phase.minutes} {lang === 'ru' ? 'мин' : 'Min.'}</span>
        </div>)}</div>
      </section>}
      <section className="v29-shortcuts">
        <button type="button" onClick={() => navigate(withUser('/review'))}><span className="v29-shortcut-icon"><FaRedoAlt /></span><span><small>{lang === 'ru' ? 'ПОВТОРЕНИЕ' : 'WIEDERHOLUNG'}</small><b>{learning?.due_count || 0} {lang === 'ru' ? 'тем ждут' : 'Themen warten'}</b></span></button>
        <button type="button" onClick={() => navigate(withUser('/mistakes'))}><span className="v29-shortcut-icon danger"><FaExclamation /></span><span><small>{lang === 'ru' ? 'СЛАБОЕ МЕСТО' : 'DEIN FOKUS'}</small><b>{topicLabel(String(weak.name), lang)}</b></span></button>
      </section>
    </main>
  );
};
