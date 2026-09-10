import React, { useCallback, useEffect, useState } from 'react';
import { FaArrowRight, FaBrain, FaClock, FaExclamationCircle, FaFire, FaPlay, FaRedoAlt } from 'react-icons/fa';
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
  const minutes = learning?.session?.minutes || selectedLesson?.estimated_time || selectedLesson?.minutes || 12;
  const phaseCount = Array.isArray(learning?.session?.phases) ? learning.session.phases.length : 1;
  const hour = new Date().getHours();
  const greeting = lang === 'ru'
    ? (hour < 12 ? 'Доброе утро' : hour < 18 ? 'Добрый день' : 'Добрый вечер')
    : (hour < 12 ? 'Guten Morgen' : hour < 18 ? 'Guten Tag' : 'Guten Abend');
  const startLesson = () => navigate(selectedLesson?.id ? withUser(`/lesson/${selectedLesson.id}`) : withUser('/plan'));

  return (
    <main className="app-shell rc-page rc-home page-enter">
      <header className="rc-home-bar">
        <div className="rc-identity"><span>D</span><div><small>{greeting}</small><strong>DeutschIQ</strong></div></div>
        <div className="rc-home-stats"><span><b>{data.level || 'A1'}</b><small>{data.xp || 0} XP</small></span><span><FaFire /><b>{data.streak || 0}</b></span></div>
      </header>

      {loadError && <div className="rc-notice error"><span>{lang === 'ru' ? 'Показываем сохранённые данные' : 'Gespeicherte Daten werden angezeigt'}</span><button type="button" onClick={load}>{lang === 'ru' ? 'Обновить' : 'Aktualisieren'}</button></div>}

      <header className="rc-page-title rc-home-title">
        <p>{lang === 'ru' ? 'СЕГОДНЯ' : 'HEUTE'}</p>
        <h1>{lang === 'ru' ? 'Один ясный следующий шаг' : 'Ein klarer nächster Schritt'}</h1>
      </header>

      <section className="rc-focus-card">
        <header><span><FaBrain /> {lang === 'ru' ? 'ЗАДАНИЕ НА СЕГОДНЯ' : 'HEUTIGE AUFGABE'}</span><b>{data.level || selectedLesson?.level || 'A1'}</b></header>
        <h2>{topicLabel(topic, lang)}</h2>
        <p>{selectedLesson?.reason === 'review_due'
          ? (lang === 'ru' ? 'Эта тема готова к повторению — сейчас лучший момент её закрепить.' : 'Dieses Thema ist bereit zur Wiederholung — jetzt ist der richtige Moment.')
          : (lang === 'ru' ? 'Выбрано по твоему уровню, ошибкам и прогрессу.' : 'Ausgewählt nach Niveau, Fehlern und Fortschritt.')}</p>
        <div className="rc-focus-meta"><span><FaClock /> {minutes} {lang === 'ru' ? 'мин' : 'Min.'}</span><span>{phaseCount} {lang === 'ru' ? 'этапа' : 'Schritte'}</span></div>
        <button type="button" className="rc-primary" onClick={startLesson}><span><FaPlay /> {selectedLesson?.id ? (lang === 'ru' ? 'Начать урок' : 'Lektion starten') : (lang === 'ru' ? 'Открыть план' : 'Plan öffnen')}</span><FaArrowRight /></button>
      </section>

      <section className="rc-today-summary">
        <div><small>{lang === 'ru' ? 'ПЛАН НА СЕГОДНЯ' : 'HEUTIGER PLAN'}</small><strong>{minutes} {lang === 'ru' ? 'минут для результата' : 'Minuten bis zum Ziel'}</strong></div>
        <button type="button" onClick={() => navigate(withUser('/plan'))}>{lang === 'ru' ? 'Посмотреть план' : 'Plan ansehen'} <FaArrowRight /></button>
      </section>

      <section className="rc-home-actions" aria-label={lang === 'ru' ? 'Дополнительные действия' : 'Weitere Aktionen'}>
        <button type="button" onClick={() => navigate(withUser('/review'))}>
          <span className="rc-action-icon"><FaRedoAlt /></span>
          <span><small>{lang === 'ru' ? 'ПОВТОРЕНИЕ' : 'WIEDERHOLUNG'}</small><strong>{learning?.due_count ? `${learning.due_count} ${lang === 'ru' ? 'тем ждут' : 'Themen warten'}` : (lang === 'ru' ? 'На сегодня всё' : 'Für heute erledigt')}</strong></span>
          <FaArrowRight />
        </button>
        <button type="button" onClick={() => navigate(withUser('/mistakes'))} disabled={!weak}>
          <span className="rc-action-icon danger"><FaExclamationCircle /></span>
          <span><small>{lang === 'ru' ? 'РАЗБОР ОШИБОК' : 'FEHLERANALYSE'}</small><strong>{weak ? topicLabel(String(weak.name), lang) : (lang === 'ru' ? 'Ошибок пока нет' : 'Noch keine Fehler')}</strong></span>
          <FaArrowRight />
        </button>
      </section>
    </main>
  );
};
