import React, { useCallback, useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaComments, FaFire, FaPlay, FaRedoAlt, FaVolumeUp } from 'react-icons/fa';
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
    <main className={`app-shell rc-page rc-home page-enter level-${String(data.level || 'a1').toLowerCase()}`}>
      <header className="rc-home-bar">
        <div className="rc-identity"><BrandMark label="DeutschIQ" /><div><small>{greeting}</small><strong>DeutschIQ</strong></div></div>
        <div className="rc-home-stats"><span><b>{data.level || 'A1'}</b><small>{data.xp || 0} XP</small></span><span><FaFire /><b>{data.streak || 0}</b></span></div>
      </header>

      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Показываем сохранённые данные', 'Gespeicherte Daten werden angezeigt', 'Showing saved data')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <div className="rc-home-context">
        <span>{tr(lang, 'СЕГОДНЯШНИЙ ФОКУС', 'HEUTIGER FOKUS', 'TODAY’S FOCUS')}</span>
        <small>{data.level || 'A1'} <b>→</b> {data.targetLevel || 'A2'}</small>
      </div>

      <section className="rc-focus-card">
        <header><span>{selectedLesson?.module_title || tr(lang, 'СЛЕДУЮЩИЙ ШАГ', 'NÄCHSTER SCHRITT', 'NEXT STEP')}{selectedLesson?.module_step && selectedLesson?.module_size ? ` · ${selectedLesson.module_step}/${selectedLesson.module_size}` : ''}</span><b>{tr(lang, '≈ 10 МИН', '≈ 10 MIN', '≈ 10 MIN')}</b></header>
        <h2>{selectedLesson?.title || topicLabel(topic, lang)}</h2>
        <div className="rc-lesson-meta"><span>{Math.max(1, Number(learning?.session?.phases?.length || 1))} {tr(lang, 'коротких шага', 'kurze Schritte', 'short steps')}</span><span>≈ {Math.min(10, Number(learning?.session?.minutes || selectedLesson?.minutes || 6))} {tr(lang, 'мин', 'Min.', 'min')}</span></div>
        <div className="rc-focus-outcome"><FaCheck /><span><small>{tr(lang, 'ПОСЛЕ УРОКА', 'NACH DER LEKTION', 'AFTER THIS LESSON')}</small><strong>{selectedLesson?.can_do || tr(lang, 'Ты применишь навык в короткой реальной ситуации.', 'Du nutzt die Fähigkeit in einer kurzen Alltagssituation.', 'You will use the skill in a short real-life situation.')}</strong></span></div>
        {learning?.session?.phases?.length > 0 && <div className="rc-session-path" aria-label={tr(lang, 'План занятия', 'Ablauf', 'Session path')}>
          {(learning.session.phases as any[]).filter(phase => ['review','learn','speak'].includes(phase.kind)).map((phase, index) => <span key={`${phase.kind}-${index}`}>{phase.kind === 'review' ? <FaRedoAlt /> : phase.kind === 'speak' ? <FaComments /> : <FaVolumeUp />}<small>{phase.kind === 'review' ? tr(lang, 'Повторить', 'Wiederholen', 'Review') : phase.kind === 'speak' ? tr(lang, 'Сказать', 'Sprechen', 'Speak') : tr(lang, 'Освоить', 'Lernen', 'Learn')}</small></span>)}
        </div>}
        <button type="button" className="rc-primary" onClick={startLesson}><span><FaPlay /> {selectedLesson?.id ? (learning?.due_count ? tr(lang, 'Начать с повторения', 'Mit Wiederholung starten', 'Start with review') : tr(lang, 'Продолжить урок', 'Lektion fortsetzen', 'Continue lesson')) : tr(lang, 'Открыть план', 'Plan öffnen', 'Open plan')}</span><FaArrowRight /></button>
      </section>

      <section className={`rc-today-secondary${learning?.due_count ? ' has-review' : ''}`} aria-label={tr(lang, 'После урока', 'Nach der Lektion', 'After the lesson')}>
        <div>{learning?.due_count ? <FaRedoAlt /> : <FaCheck />}<span><strong>{learning?.due_count ? learning.due_count : tr(lang, 'На сегодня всё готово', 'Für heute ist alles bereit', 'Everything is ready for today')}</strong><small>{learning?.due_count ? tr(lang, 'коротких повторений перед уроком', 'kurze Wiederholungen vor der Lektion', 'short reviews before the lesson') : tr(lang, 'один понятный следующий шаг', 'ein klarer nächster Schritt', 'one clear next step')}</small></span></div>
        <button type="button" onClick={() => navigate(withUser('/analytics'))}>{tr(lang, 'Посмотреть прогресс', 'Fortschritt ansehen', 'View progress')} <FaArrowRight /></button>
      </section>
    </main>
  );
};
