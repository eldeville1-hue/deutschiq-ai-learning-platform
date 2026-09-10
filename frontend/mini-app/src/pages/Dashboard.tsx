import React, { useCallback, useEffect, useState } from 'react';
import { FaArrowRight, FaBrain, FaExclamationCircle, FaFire, FaPlay, FaRedoAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { BrandMark } from '../components/BrandMark';

export const Dashboard: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [lesson, setLesson] = useState<any>(null);
  const [learning, setLearning] = useState<any>(null);
  const [loadError, setLoadError] = useState(false);
  const userId = getUserId();

  const load = useCallback(async () => {
    void api.trackEvent({ user_id: userId, event_name: 'dashboard_viewed' });
    const [dashboard, plan, today] = await Promise.allSettled([
      api.getDashboard(userId),
      api.getPlan(userId),
      api.getLearningToday(userId),
    ]);
    if (dashboard.status === 'fulfilled') {
      setData(dashboard.value);
      setLoadError(false);
    } else {
      setData({ level: 'A1', targetLevel: 'A2', xp: 0, streak: 0, weaknesses: [] });
      setLoadError(true);
    }
    if (plan.status === 'fulfilled') {
      const items = Array.isArray(plan.value) ? plan.value : [];
      setLesson(items.find((item: any) => !item.completed) || items[0]);
    }
    setLearning(today.status === 'fulfilled' ? today.value : null);
  }, [userId]);

  useEffect(() => { void load(); }, [load]);

  if (!data) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;
  const selectedLesson = learning?.next_lesson || lesson;
  const topic = selectedLesson?.topic || data.weaknesses?.[0]?.name || 'haben_conjugation';
  const weak = data.weaknesses?.[0];
  const hour = new Date().getHours();
  const greeting = lang === 'ru'
    ? (hour < 12 ? 'Доброе утро' : hour < 18 ? 'Добрый день' : 'Добрый вечер')
    : (hour < 12 ? 'Guten Morgen' : hour < 18 ? 'Guten Tag' : 'Guten Abend');
  const startLesson = () => navigate(selectedLesson?.id ? withUser(`/lesson/${selectedLesson.id}`) : withUser('/plan'));

  return (
    <main className="app-shell rc-page rc-home page-enter">
      <header className="rc-home-bar">
        <div className="rc-identity"><BrandMark label="DeutschIQ" /><div><small>{greeting}</small><strong>DeutschIQ</strong></div></div>
        <div className="rc-home-stats"><span><b>{data.level || 'A1'}</b><small>{data.xp || 0} XP</small></span><span><FaFire /><b>{data.streak || 0}</b></span></div>
      </header>

      {loadError && <div className="rc-notice error"><span>{lang === 'ru' ? 'Показываем сохранённые данные' : 'Gespeicherte Daten werden angezeigt'}</span><button type="button" onClick={load}>{lang === 'ru' ? 'Обновить' : 'Aktualisieren'}</button></div>}

      <header className="rc-page-title rc-home-title">
        <p>{lang === 'ru' ? 'СЕГОДНЯ' : 'HEUTE'}</p>
        <h1>{lang === 'ru' ? 'Твой урок' : 'Deine Lektion'}</h1>
      </header>

      <section className="rc-focus-card">
        <header><span><FaBrain /> {lang === 'ru' ? 'ГЛАВНАЯ ТЕМА' : 'DEIN THEMA'}</span><b>{data.level || selectedLesson?.level || 'A1'}</b></header>
        <h2>{topicLabel(topic, lang)}</h2>
        <p>{selectedLesson?.reason === 'review_due'
          ? (lang === 'ru' ? 'Пора закрепить эту тему.' : 'Zeit, dieses Thema zu festigen.')
          : (lang === 'ru' ? 'Выбрано по твоему прогрессу.' : 'Passend zu deinem Fortschritt.')}</p>
        <button type="button" className="rc-primary" onClick={startLesson}><span><FaPlay /> {selectedLesson?.id ? (lang === 'ru' ? 'Начать' : 'Starten') : (lang === 'ru' ? 'Открыть план' : 'Plan öffnen')}</span><FaArrowRight /></button>
      </section>

      <section className="rc-home-actions" aria-label={lang === 'ru' ? 'Дополнительные действия' : 'Weitere Aktionen'}>
        <button type="button" onClick={() => navigate(withUser('/review'))}>
          <span className="rc-action-icon"><FaRedoAlt /></span>
          <span><small>{lang === 'ru' ? 'ПОВТОРИТЬ' : 'WIEDERHOLEN'}</small><strong>{learning?.due_count ? `${learning.due_count} ${lang === 'ru' ? 'темы' : 'Themen'}` : (lang === 'ru' ? 'Всё готово' : 'Alles erledigt')}</strong></span>
          <FaArrowRight />
        </button>
        <button type="button" onClick={() => navigate(withUser('/mistakes'))} disabled={!weak}>
          <span className="rc-action-icon danger"><FaExclamationCircle /></span>
          <span><small>{lang === 'ru' ? 'ОШИБКИ' : 'FEHLER'}</small><strong>{weak ? topicLabel(String(weak.name), lang) : (lang === 'ru' ? 'Ошибок нет' : 'Keine Fehler')}</strong></span>
          <FaArrowRight />
        </button>
      </section>
    </main>
  );
};
