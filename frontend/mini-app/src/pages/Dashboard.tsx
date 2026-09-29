import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaArrowRight, FaCheck, FaComments, FaFire, FaLightbulb, FaPlay, FaRedoAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { BrandMark } from '../components/BrandMark';
import { ProductState } from '../components/ProductState';
import { tr } from '../i18n/language';
import type { JourneyLesson } from '../learning/journey';
import { normalizeJourneyLesson, normalizeJourneyLessons, normalizeLearningPhases, selectCurrentLesson } from '../learning/journey';
import { readDailySession, saveDailySession } from '../learning/dailySession';

export const Dashboard: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const userId = getUserId();
  const [data, setData] = useState<any>(null);
  const [lesson, setLesson] = useState<JourneyLesson | null>(null);
  const [learning, setLearning] = useState<any>(null);
  const [status, setStatus] = useState<'loading' | 'ready' | 'partial' | 'error'>('loading');
  const [resume, setResume] = useState(() => readDailySession(userId));

  const load = useCallback(async () => {
    setStatus(current => current === 'ready' || current === 'partial' ? current : 'loading');
    void api.trackEvent({ user_id: userId, event_name: 'dashboard_viewed' });
    const [dashboard, plan, today] = await Promise.allSettled([
      api.getDashboard(userId),
      api.getPlan(userId, lang),
      api.getLearningToday(userId, lang),
    ]);
    setData(dashboard.status === 'fulfilled' ? dashboard.value : null);
    if (plan.status === 'fulfilled') {
      setLesson(selectCurrentLesson(normalizeJourneyLessons(plan.value)));
    }
    setLearning(today.status === 'fulfilled' ? today.value : null);
    const hasLesson = today.status === 'fulfilled' && Boolean(today.value?.next_lesson)
      || plan.status === 'fulfilled' && Array.isArray(plan.value) && plan.value.length > 0;
    setStatus(dashboard.status === 'fulfilled'
      ? (plan.status === 'fulfilled' || today.status === 'fulfilled' ? 'ready' : 'partial')
      : hasLesson ? 'partial' : 'error');
  }, [lang, userId]);

  useEffect(() => { void load(); }, [load]);

  const selectedLesson = useMemo(() => normalizeJourneyLesson(learning?.next_lesson) || lesson, [learning, lesson]);
  const phases = useMemo(() => normalizeLearningPhases(learning?.session?.phases), [learning]);
  if (status === 'loading') return <main className="app-shell dq-home" aria-busy="true"><div className="dq-page-skeleton"><span /><span /><span /></div></main>;
  if (status === 'error') return <main className="app-shell dq-home page-enter"><ProductState kind="error" eyebrow={tr(lang, 'СВЯЗЬ ПРЕРВАЛАСЬ', 'VERBINDUNG UNTERBROCHEN', 'CONNECTION INTERRUPTED')} title={tr(lang, 'Не удалось подготовить урок', 'Die Lektion konnte nicht vorbereitet werden', 'We could not prepare your lesson')} detail={tr(lang, 'Твои результаты сохранены. Проверь соединение и попробуй ещё раз.', 'Dein Fortschritt ist sicher. Prüfe die Verbindung und versuche es erneut.', 'Your progress is safe. Check your connection and try again.')} action={tr(lang, 'Повторить', 'Erneut versuchen', 'Try again')} onAction={() => void load()} /></main>;
  if (!selectedLesson) return <main className="app-shell dq-home page-enter"><ProductState eyebrow={tr(lang, 'СЛЕДУЮЩИЙ ШАГ', 'NÄCHSTER SCHRITT', 'NEXT STEP')} title={tr(lang, 'Подготовим новый урок', 'Wir bereiten eine neue Lektion vor', 'Let’s prepare your next lesson')} detail={tr(lang, 'Открой план, чтобы выбрать доступный навык или обновить маршрут.', 'Öffne den Lernweg, um eine verfügbare Fähigkeit auszuwählen.', 'Open your path to choose an available skill or refresh the route.')} action={tr(lang, 'Открыть план', 'Lernweg öffnen', 'Open learning path')} onAction={() => navigate(withUser('/plan'))} /></main>;
  const resolvedData = data || { level: selectedLesson.level, targetLevel: 'A2', streak: 0, weaknesses: [] };
  const topic = selectedLesson.topic || resolvedData.weaknesses?.[0]?.name || 'haben_conjugation';
  const hour = new Date().getHours();
  const greeting = hour < 12
    ? tr(lang, 'Доброе утро', 'Guten Morgen', 'Good morning')
    : hour < 18
      ? tr(lang, 'Добрый день', 'Guten Tag', 'Good afternoon')
      : tr(lang, 'Добрый вечер', 'Guten Abend', 'Good evening');
  const startLesson = () => {
    if (!selectedLesson?.id) return navigate(withUser('/plan'));
    const nextLessonId = resume?.nextLessonId || selectedLesson.id;
    const stage = resume?.stage || (learning?.due_count ? 'review' : 'lesson');
    saveDailySession(userId, { nextLessonId, stage });
    setResume(readDailySession(userId));
    const target = stage === 'review'
      ? `/review?nextLesson=${nextLessonId}`
      : `/lesson/${nextLessonId}`;
    navigate(withUser(target));
  };

  return (
    <main className={`app-shell dq-home page-enter level-${String(resolvedData.level || 'a1').toLowerCase()}`}>
      <header className="dq-home-top">
        <div className="dq-home-person"><BrandMark label="DeutschIQ" /><div><small>{greeting}</small><strong>{resolvedData.first_name || tr(lang, 'Немецкий сегодня', 'Deutsch heute', 'German today')}</strong></div></div>
        <div className="dq-home-streak"><FaFire /><strong>{resolvedData.streak || 0}</strong><small>{tr(lang, 'дня', 'Tage', 'days')}</small></div>
      </header>

      {status === 'partial' && <div className="rc-notice saved"><span>{tr(lang, 'Часть данных обновится после восстановления связи', 'Einige Daten werden nach der Verbindung aktualisiert', 'Some details will update when the connection returns')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <section className="dq-daily-stage">
        <div className="dq-daily-copy">
          <div className="dq-daily-kicker"><span>{tr(lang, 'ТВОЙ ШАГ НА СЕГОДНЯ', 'DEIN SCHRITT FÜR HEUTE', 'YOUR STEP TODAY')}</span><div><em>{resolvedData.level || 'A1'} → {resolvedData.targetLevel || 'A2'}</em>{selectedLesson.moduleStep && selectedLesson.moduleSize ? <b>{selectedLesson.moduleStep}/{selectedLesson.moduleSize}</b> : null}</div></div>
          <h1>{selectedLesson.title || topicLabel(topic, lang)}</h1>
          <p>{selectedLesson.scenario || selectedLesson.canDo || tr(lang, 'Один короткий урок для реальной ситуации.', 'Eine kurze Lektion für eine echte Situation.', 'One short lesson for a real situation.')}</p>
          <div className="dq-session-path" aria-label={tr(lang, 'Путь занятия', 'Ablauf der Einheit', 'Session path')}>
            <span className={learning?.due_count ? 'active' : 'ready'}><FaRedoAlt /><small>{tr(lang, 'Повторить', 'Wiederholen', 'Review')}</small>{learning?.due_count ? <b>{learning.due_count}</b> : <FaCheck />}</span>
            <i />
            <span className="active"><FaLightbulb /><small>{tr(lang, 'Понять', 'Verstehen', 'Learn')}</small><b>{phases.find(item => item.kind === 'learn')?.count || 1}</b></span>
            <i />
            <span className="ready"><FaComments /><small>{tr(lang, 'Применить', 'Anwenden', 'Use')}</small><FaCheck /></span>
          </div>
          <div className="dq-daily-outcome"><FaCheck /><span><small>{tr(lang, 'ПОСЛЕ УРОКА', 'NACH DER LEKTION', 'AFTER THIS LESSON')}</small><strong>{selectedLesson.canDo || tr(lang, 'Ты применишь навык в коротком разговоре.', 'Du nutzt die Fähigkeit in einem kurzen Gespräch.', 'You will use the skill in a short conversation.')}</strong></span></div>
          <div className="dq-daily-meta"><span>{Math.max(1, phases.length || 1)} {tr(lang, 'шага', 'Schritte', 'steps')}</span><span>≈ {Math.min(10, Number(learning?.session?.minutes || selectedLesson.minutes))} {tr(lang, 'мин', 'Min.', 'min')}</span></div>
          <button type="button" className="dq-main-action" onClick={startLesson}><span><FaPlay /> {selectedLesson?.id ? (resume ? tr(lang, 'Продолжить занятие', 'Einheit fortsetzen', 'Continue session') : learning?.due_count ? tr(lang, 'Начать с повторения', 'Mit Wiederholung starten', 'Start with review') : tr(lang, 'Начать урок', 'Lektion starten', 'Start lesson')) : tr(lang, 'Открыть план', 'Plan öffnen', 'Open plan')}</span><FaArrowRight /></button>
        </div>
      </section>

      <footer className="dq-home-after" aria-label={tr(lang, 'После урока', 'Nach der Lektion', 'After the lesson')}>
        <div>{learning?.due_count ? <FaRedoAlt /> : <FaCheck />}<span><strong>{learning?.due_count ? `${learning.due_count} ${tr(lang, 'на повтор', 'zu wiederholen', 'to review')}` : tr(lang, 'Маршрут готов', 'Dein Weg ist bereit', 'Your path is ready')}</strong><small>{learning?.due_count ? tr(lang, 'Сначала вернём важное в память', 'Zuerst holen wir Wichtiges zurück', 'We will recall the important parts first') : tr(lang, 'Продолжай в своём темпе', 'Weiter in deinem Tempo', 'Continue at your pace')}</small></span></div>
        <button type="button" onClick={() => navigate(withUser('/analytics'))}>{tr(lang, 'Прогресс', 'Fortschritt', 'Progress')} <FaArrowRight /></button>
      </footer>
    </main>
  );
};
