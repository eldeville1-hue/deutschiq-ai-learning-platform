import React, { useCallback, useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaFire, FaPlay, FaRedoAlt } from 'react-icons/fa';
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
    <main className={`app-shell dq-home page-enter level-${String(data.level || 'a1').toLowerCase()}`}>
      <header className="dq-home-top">
        <div className="dq-home-person"><BrandMark label="DeutschIQ" /><div><small>{greeting}</small><strong>{data.first_name || tr(lang, 'Немецкий сегодня', 'Deutsch heute', 'German today')}</strong></div></div>
        <div className="dq-home-streak"><FaFire /><strong>{data.streak || 0}</strong><small>{tr(lang, 'дня', 'Tage', 'days')}</small></div>
      </header>

      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Показываем сохранённые данные', 'Gespeicherte Daten werden angezeigt', 'Showing saved data')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <section className="dq-daily-stage">
        <div className="dq-daily-copy">
          <div className="dq-daily-kicker"><span>{tr(lang, 'ТВОЙ ШАГ НА СЕГОДНЯ', 'DEIN SCHRITT FÜR HEUTE', 'YOUR STEP TODAY')}</span><div><em>{data.level || 'A1'} → {data.targetLevel || 'A2'}</em>{selectedLesson?.module_step && selectedLesson?.module_size ? <b>{selectedLesson.module_step}/{selectedLesson.module_size}</b> : null}</div></div>
          <h1>{selectedLesson?.title || topicLabel(topic, lang)}</h1>
          <p>{selectedLesson?.scenario || selectedLesson?.can_do || tr(lang, 'Один короткий урок для реальной ситуации.', 'Eine kurze Lektion für eine echte Situation.', 'One short lesson for a real situation.')}</p>
          <div className="dq-daily-outcome"><FaCheck /><span><small>{tr(lang, 'ПОСЛЕ УРОКА', 'NACH DER LEKTION', 'AFTER THIS LESSON')}</small><strong>{selectedLesson?.can_do || tr(lang, 'Ты применишь навык в коротком разговоре.', 'Du nutzt die Fähigkeit in einem kurzen Gespräch.', 'You will use the skill in a short conversation.')}</strong></span></div>
          <div className="dq-daily-meta"><span>{Math.max(1, Number(learning?.session?.phases?.length || 1))} {tr(lang, 'шага', 'Schritte', 'steps')}</span><span>≈ {Math.min(10, Number(learning?.session?.minutes || selectedLesson?.minutes || 6))} {tr(lang, 'мин', 'Min.', 'min')}</span></div>
          <button type="button" className="dq-main-action" onClick={startLesson}><span><FaPlay /> {selectedLesson?.id ? (learning?.due_count ? tr(lang, 'Начать с повторения', 'Mit Wiederholung starten', 'Start with review') : tr(lang, 'Начать урок', 'Lektion starten', 'Start lesson')) : tr(lang, 'Открыть план', 'Plan öffnen', 'Open plan')}</span><FaArrowRight /></button>
        </div>
      </section>

      <footer className="dq-home-after" aria-label={tr(lang, 'После урока', 'Nach der Lektion', 'After the lesson')}>
        <div>{learning?.due_count ? <FaRedoAlt /> : <FaCheck />}<span><strong>{learning?.due_count ? `${learning.due_count} ${tr(lang, 'на повтор', 'zu wiederholen', 'to review')}` : tr(lang, 'Маршрут готов', 'Dein Weg ist bereit', 'Your path is ready')}</strong><small>{learning?.due_count ? tr(lang, 'Сначала вернём важное в память', 'Zuerst holen wir Wichtiges zurück', 'We will recall the important parts first') : tr(lang, 'Продолжай в своём темпе', 'Weiter in deinem Tempo', 'Continue at your pace')}</small></span></div>
        <button type="button" onClick={() => navigate(withUser('/analytics'))}>{tr(lang, 'Прогресс', 'Fortschritt', 'Progress')} <FaArrowRight /></button>
      </footer>
    </main>
  );
};
