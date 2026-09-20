import React, { useCallback, useEffect, useState } from 'react';
import { FaArrowRight, FaBrain, FaExclamationCircle, FaFire, FaPlay, FaRedoAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { BrandMark } from '../components/BrandMark';
import { tr } from '../i18n/language';

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
      api.getPlan(userId, lang),
      api.getLearningToday(userId, lang),
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
  }, [lang, userId]);

  useEffect(() => { void load(); }, [load]);

  if (!data) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;
  const selectedLesson = learning?.next_lesson || lesson;
  const topic = selectedLesson?.topic || data.weaknesses?.[0]?.name || 'haben_conjugation';
  const weak = data.weaknesses?.[0];
  const hour = new Date().getHours();
  const greeting = hour < 12
    ? tr(lang, 'Доброе утро', 'Guten Morgen', 'Good morning')
    : hour < 18
      ? tr(lang, 'Добрый день', 'Guten Tag', 'Good afternoon')
      : tr(lang, 'Добрый вечер', 'Guten Abend', 'Good evening');
  const startLesson = () => {
    if (!selectedLesson?.id) return navigate(withUser('/plan'));
    const target = learning?.due_count
      ? `/review?nextLesson=${selectedLesson.id}`
      : `/lesson/${selectedLesson.id}`;
    navigate(withUser(target));
  };

  return (
    <main className="app-shell rc-page rc-home page-enter">
      <header className="rc-home-bar">
        <div className="rc-identity"><BrandMark label="DeutschIQ" /><div><small>{greeting}</small><strong>DeutschIQ</strong></div></div>
        <div className="rc-home-stats"><span><b>{data.level || 'A1'}</b><small>{data.xp || 0} XP</small></span><span><FaFire /><b>{data.streak || 0}</b></span></div>
      </header>

      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Показываем сохранённые данные', 'Gespeicherte Daten werden angezeigt', 'Showing saved data')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <header className="rc-page-title rc-home-title">
        <p>{tr(lang, 'СЕГОДНЯ', 'HEUTE', 'TODAY')}</p>
        <h1>{tr(lang, 'Твой урок', 'Deine Lektion', 'Your lesson')}</h1>
      </header>

      <section className="rc-focus-card">
        <header><span><FaBrain /> {tr(lang, 'ГЛАВНАЯ ТЕМА', 'DEIN THEMA', 'YOUR FOCUS')}</span><b>{data.level || selectedLesson?.level || 'A1'}</b></header>
        <h2>{selectedLesson?.title || topicLabel(topic, lang)}</h2>
        <p>{selectedLesson?.reason === 'review_due'
          ? tr(lang, 'Пора закрепить эту тему.', 'Zeit, dieses Thema zu festigen.', 'Time to strengthen this skill.')
          : tr(lang, 'Выбрано по твоему прогрессу.', 'Passend zu deinem Fortschritt.', 'Selected from your progress.')}</p>
        <button type="button" className="rc-primary" onClick={startLesson}><span><FaPlay /> {selectedLesson?.id ? (learning?.due_count ? tr(lang, 'Начать с повторения', 'Mit Wiederholung starten', 'Start with review') : tr(lang, 'Начать', 'Starten', 'Start')) : tr(lang, 'Открыть план', 'Plan öffnen', 'Open plan')}</span><FaArrowRight /></button>
      </section>

      <section className="rc-home-actions" aria-label={tr(lang, 'Дополнительные действия', 'Weitere Aktionen', 'More actions')}>
        <button type="button" onClick={() => navigate(withUser('/review'))}>
          <span className="rc-action-icon"><FaRedoAlt /></span>
          <span><small>{tr(lang, 'ПОВТОРИТЬ', 'WIEDERHOLEN', 'REVIEW')}</small><strong>{learning?.due_count ? `${learning.due_count} ${tr(lang, 'темы', 'Themen', 'topics')}` : tr(lang, 'Всё готово', 'Alles erledigt', 'All done')}</strong></span>
          <FaArrowRight />
        </button>
        <button type="button" onClick={() => navigate(withUser('/mistakes'))} disabled={!weak}>
          <span className="rc-action-icon danger"><FaExclamationCircle /></span>
          <span><small>{tr(lang, 'ОШИБКИ', 'FEHLER', 'MISTAKES')}</small><strong>{weak ? topicLabel(String(weak.name), lang) : tr(lang, 'Ошибок нет', 'Keine Fehler', 'No mistakes')}</strong></span>
          <FaArrowRight />
        </button>
      </section>
    </main>
  );
};
