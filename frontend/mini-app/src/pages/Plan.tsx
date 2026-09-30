import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaCheck, FaChevronDown, FaLock, FaPlay } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { tr } from '../i18n/language';
import { ProductState } from '../components/ProductState';
import type { JourneyLesson } from '../learning/journey';
import { normalizeJourneyLessons, selectCurrentLesson } from '../learning/journey';

export const Plan: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [lessons, setLessons] = useState<JourneyLesson[]>([]);
  const [dashboard, setDashboard] = useState<any>(null);
  const [journey, setJourney] = useState<any>(null);
  const [selectedTrack, setSelectedTrack] = useState<string>('');
  const [showWeek, setShowWeek] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [loading, setLoading] = useState(true);
  const userId = getUserId();

  const load = useCallback(async () => {
    setLoading(true);
    const [plan, profile, path] = await Promise.allSettled([api.getPlan(userId, lang, selectedTrack || undefined), api.getDashboard(userId), api.getJourney(userId)]);
    if (plan.status === 'fulfilled') setLessons(normalizeJourneyLessons(plan.value));
    if (profile.status === 'fulfilled') setDashboard(profile.value);
    else setDashboard({ level: 'A1', targetLevel: 'A2' });
    if (path.status === 'fulfilled') {
      setJourney(path.value);
      if (!selectedTrack && path.value?.current_level) setSelectedTrack(path.value.current_level);
    }
    setLoadError(plan.status === 'rejected' || profile.status === 'rejected' || path.status === 'rejected');
    setLoading(false);
  }, [lang, selectedTrack, userId]);

  useEffect(() => { void load(); }, [load]);

  const current = useMemo(() => selectCurrentLesson(lessons), [lessons]);
  const week = current?.week || 1;
  const weekLessons = lessons.filter(item => item.week === week);
  const upcomingLessons = weekLessons.filter(item => item.id !== current?.id);
  const upcoming = showWeek ? upcomingLessons : upcomingLessons.slice(0, 3);
  const routeCompleted = lessons.filter(item => item.completed).length;
  const routeProgress = Math.round((routeCompleted / Math.max(lessons.length, 1)) * 100);
  const track = selectedTrack || current?.track || dashboard?.level || 'A1';
  const moduleNames = track === 'B1' ? [
    tr(lang, 'Связи предложений', 'Satzverknüpfung', 'Linking clauses'),
    tr(lang, 'Пассив и модальность', 'Passiv & Modalität', 'Voice & modality'),
    tr(lang, 'Грамматическая точность', 'Grammatische Präzision', 'Grammatical precision'),
    tr(lang, 'Письмо и речь', 'Schreiben & Sprechen', 'Writing & speaking'),
  ] : track === 'B2' ? [
    tr(lang, 'Связи и сжатие', 'Verknüpfen & Verdichten', 'Linking & condensing'),
    tr(lang, 'Формальный язык', 'Formeller Ausdruck', 'Formal expression'),
    tr(lang, 'Аргументация', 'Argumentieren', 'Argumentation'),
    tr(lang, 'Дискуссия', 'Diskutieren', 'Discussion'),
  ] : track === 'A2' ? [
    tr(lang, 'Падежи', 'Fälle', 'Cases'),
    tr(lang, 'Прошедшее', 'Vergangenheit', 'Past events'),
    tr(lang, 'Придаточные', 'Nebensätze', 'Subordinate clauses'),
    tr(lang, 'Самостоятельная речь', 'Selbstständig sprechen', 'Independent communication'),
  ] : [
    tr(lang, 'Первый разговор', 'Das erste Gespräch', 'Your first conversation'),
    tr(lang, 'Мой день', 'Mein Tag', 'My day'),
    tr(lang, 'В городе', 'In der Stadt', 'In the city'),
    tr(lang, 'Решаем дела', 'Alltag erledigen', 'Getting things done'),
  ];

  if (loading && !dashboard) return <main className="app-shell dq-plan" aria-busy="true"><div className="dq-page-skeleton"><span /><span /><span /></div></main>;
  if (!dashboard) return <main className="app-shell dq-plan page-enter"><ProductState kind="error" eyebrow={tr(lang, 'МАРШРУТ НЕДОСТУПЕН', 'LERNWEG NICHT VERFÜGBAR', 'PATH UNAVAILABLE')} title={tr(lang, 'Не удалось загрузить план', 'Der Lernweg konnte nicht geladen werden', 'We could not load your path')} detail={tr(lang, 'Твой прогресс сохранён. Проверь соединение и попробуй снова.', 'Dein Fortschritt ist sicher. Prüfe die Verbindung und versuche es erneut.', 'Your progress is safe. Check the connection and try again.')} action={tr(lang, 'Повторить', 'Erneut versuchen', 'Try again')} onAction={() => void load()} /></main>;

  return (
    <main className={`app-shell dq-plan page-enter level-${String(track).toLowerCase()}`}>
      <header className="dq-plan-head">
        <p>{tr(lang, 'ПЛАН', 'PLAN', 'PLAN')}</p>
        <h1>{dashboard.level || 'A1'} <span>→</span> {dashboard.targetLevel || 'A2'}</h1>
        <span>{tr(lang, 'Твой маршрут по навыкам', 'Dein Weg nach Fähigkeiten', 'Your skill-based path')}</span>
      </header>

      {loadError && <div className="rc-notice saved"><span>{tr(lang, 'Показываем сохранённый маршрут', 'Gespeicherter Lernweg wird angezeigt', 'Showing your saved path')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      {(journey?.levels || []).some((item: any) => item.total_lessons > 0) && <section className="dq-level-switcher" aria-label={tr(lang, 'Путь по уровням', 'Niveaureise', 'Level journey')}>
        <div className="dq-levels">{(journey?.levels || []).filter((item: any) => item.total_lessons > 0).map((item: any) => {
          const accessible = ['active', 'review', 'completed'].includes(item.state);
          const label = item.state === 'active' ? tr(lang, 'Активный', 'Aktiv', 'Active') : item.state === 'review' ? tr(lang, 'Повторение', 'Wiederholen', 'Review') : item.state === 'completed' ? tr(lang, 'Пройден', 'Abgeschlossen', 'Completed') : item.state === 'coming_soon' ? tr(lang, 'Позже', 'Demnächst', 'Coming later') : tr(lang, 'Закрыт', 'Gesperrt', 'Locked');
          return <button type="button" key={item.level} className={`dq-level ${item.state}${track === item.level ? ' selected' : ''}`} disabled={!accessible} onClick={() => accessible && setSelectedTrack(item.level)} aria-label={`${item.level}: ${label}`}>
            <span>{item.level}</span>{accessible ? item.state === 'completed' ? <FaCheck /> : track === item.level ? <FaPlay /> : null : <FaLock />}
          </button>;
        })}</div>
        {(() => { const active = (journey?.levels || []).find((item: any) => item.state === 'active'); const rule = journey?.unlock_rule || { completion: 100, mastery: 60 }; return active && active.completion >= rule.completion && active.mastery >= rule.mastery ? <button type="button" className="rc-primary checkpoint-cta" onClick={() => navigate(withUser(`/checkpoint/${active.level}`))}>{tr(lang, `Пройти выпускную миссию ${active.level}`, `${active.level}-Abschlussmission starten`, `Take the ${active.level} graduation mission`)}</button> : null; })()}
      </section>}

      {current?.id ? <section className="dq-plan-now">
        <header><span>{tr(lang, 'ПРОДОЛЖИТЬ МАРШРУТ', 'WEG FORTSETZEN', 'CONTINUE YOUR PATH')}</span><small>{tr(lang, `Модуль ${week} из 4`, `Modul ${week} von 4`, `Module ${week} of 4`)}</small></header>
        <div><small>{current.moduleTitle || moduleNames[week - 1]}</small><h2>{current.title || topicLabel(current.topic || 'word_order', lang)}</h2>{current.canDo && <p>{current.canDo}</p>}</div>
        <button type="button" className="dq-main-action" onClick={() => navigate(withUser(`/lesson/${current.id}`))}><span><FaPlay /> {tr(lang, 'Продолжить', 'Weitermachen', 'Continue')}</span><b>→</b></button>
      </section> : <ProductState kind={loadError ? 'error' : 'empty'} eyebrow={loadError ? tr(lang, 'СВЯЗЬ ПРЕРВАЛАСЬ', 'VERBINDUNG UNTERBROCHEN', 'CONNECTION INTERRUPTED') : tr(lang, 'ПЛАН ГОТОВИТСЯ', 'LERNWEG WIRD VORBEREITET', 'PATH IN PREPARATION')} title={loadError ? tr(lang, 'Маршрут пока не загрузился', 'Dein Lernweg wurde noch nicht geladen', 'Your path has not loaded yet') : tr(lang, 'Следующий урок скоро появится', 'Die nächste Lektion erscheint bald', 'Your next lesson will appear soon')} detail={loadError ? tr(lang, 'Проверь соединение — прогресс уже сохранён.', 'Prüfe die Verbindung — dein Fortschritt ist gespeichert.', 'Check your connection—your progress is already safe.') : tr(lang, 'Мы собираем следующий шаг из твоих результатов.', 'Wir erstellen den nächsten Schritt aus deinen Ergebnissen.', 'We are building the next step from your results.')} action={loadError ? tr(lang, 'Повторить', 'Erneut versuchen', 'Try again') : tr(lang, 'Обновить план', 'Lernweg aktualisieren', 'Refresh path')} onAction={() => void load()} />}

      {current?.id && <section className="dq-route">
        <header><div><small>{tr(lang, `МОДУЛЬ ${week} · ${routeCompleted}/${lessons.length || 20}`, `MODUL ${week} · ${routeCompleted}/${lessons.length || 20}`, `MODULE ${week} · ${routeCompleted}/${lessons.length || 20}`)}</small><h2>{tr(lang, 'Следующие шаги', 'Nächste Schritte', 'Next steps')}</h2></div><span>{routeProgress}%</span></header>
        <div className="dq-route-progress"><i style={{ width: `${routeProgress}%` }} /></div>
        <div className="dq-route-list">
          {upcoming.map((lesson, index) => {
            const locked = lesson.blockedBy.length > 0;
            const active = lesson.id === current?.id;
            const detail = lesson.completed
              ? tr(lang, 'Завершено', 'Abgeschlossen', 'Completed')
              : locked
                ? lesson.blockedBy.includes('previous_step')
                  ? tr(lang, 'Сначала пройди предыдущий шаг', 'Zuerst den vorherigen Schritt abschließen', 'Complete the previous step first')
                  : tr(lang, 'Сначала закрепи базовый навык', 'Zuerst die Grundlage festigen', 'Strengthen the prerequisite first')
                : lesson.mastery == null
                  ? tr(lang, 'Доступно', 'Bereit', 'Ready')
                  : `${tr(lang, 'Освоено', 'Beherrscht', 'Mastery')} ${lesson.mastery}%`;
            return <button type="button" key={lesson.id || index} className={`dq-route-step${active ? ' active' : ''}${lesson.completed ? ' complete' : ''}`} disabled={locked} onClick={() => !locked && lesson.id && navigate(withUser(`/lesson/${lesson.id}`))}>
              <span className="dq-route-dot">{lesson.completed ? <FaCheck /> : locked ? <FaLock /> : String(index + 2).padStart(2, '0')}</span>
              <span><strong>{lesson.title || topicLabel(lesson.topic, lang)}</strong><small>{detail}</small></span>
              {!locked && <span className="dq-route-arrow">›</span>}
            </button>;
          })}
          {!upcoming.length && <div className="rc-empty-inline"><span>{tr(lang, 'Заверши текущий урок — следующий шаг откроется автоматически.', 'Schließe die aktuelle Lektion ab – der nächste Schritt öffnet sich automatisch.', 'Finish the current lesson and the next step will open automatically.')}</span></div>}
        </div>
        {upcomingLessons.length > 3 && <button type="button" className="rc-text-action" onClick={() => setShowWeek(value => !value)}>{showWeek ? tr(lang, 'Показать меньше шагов', 'Weniger Schritte anzeigen', 'Show fewer steps') : tr(lang, 'Показать весь модуль', 'Ganzes Modul anzeigen', 'Show full module')} <FaChevronDown className={showWeek ? 'rotated' : ''} /></button>}
      </section>}
    </main>
  );
};
