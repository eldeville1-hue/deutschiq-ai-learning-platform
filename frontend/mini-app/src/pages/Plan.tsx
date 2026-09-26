import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaCheck, FaChevronDown, FaLock, FaPlay } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { tr } from '../i18n/language';

export const Plan: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [lessons, setLessons] = useState<any[]>([]);
  const [dashboard, setDashboard] = useState<any>(null);
  const [journey, setJourney] = useState<any>(null);
  const [selectedTrack, setSelectedTrack] = useState<string>('');
  const [showWeek, setShowWeek] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const userId = getUserId();

  const load = useCallback(async () => {
    const [plan, profile, path] = await Promise.allSettled([api.getPlan(userId, lang, selectedTrack || undefined), api.getDashboard(userId), api.getJourney(userId)]);
    if (plan.status === 'fulfilled') setLessons(Array.isArray(plan.value) ? plan.value : []);
    if (profile.status === 'fulfilled') setDashboard(profile.value);
    else setDashboard({ level: 'A1', targetLevel: 'A2' });
    if (path.status === 'fulfilled') {
      setJourney(path.value);
      if (!selectedTrack && path.value?.current_level) setSelectedTrack(path.value.current_level);
    }
    setLoadError(plan.status === 'rejected' || profile.status === 'rejected' || path.status === 'rejected');
  }, [lang, selectedTrack, userId]);

  useEffect(() => { void load(); }, [load]);

  const current = useMemo(() => lessons.find(item => item.recommended) || lessons.find(item => !item.completed && !(Array.isArray(item.blocked_by) && item.blocked_by.length)) || lessons.find(item => !item.completed) || lessons[0], [lessons]);
  const week = Number(current?.week || 1);
  const weekLessons = lessons.filter(item => Number(item.week || 1) === week);
  const visible = showWeek ? weekLessons : weekLessons.slice(0, 5);
  const upcoming = visible.filter(item => item.id !== current?.id);
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

  if (!dashboard) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className={`app-shell rc-page rc-plan page-enter level-${String(track).toLowerCase()}`}>
      <header className="rc-page-title">
        <p>{tr(lang, 'ПЛАН', 'PLAN', 'PLAN')}</p>
        <h1>{dashboard.level || 'A1'} <span>→</span> {dashboard.targetLevel || 'A2'}</h1>
        <span>{tr(lang, 'Твой маршрут по навыкам', 'Dein Weg nach Fähigkeiten', 'Your skill-based path')}</span>
      </header>

      {loadError && <div className="rc-notice saved"><span>{tr(lang, 'Показываем сохранённый маршрут', 'Gespeicherter Lernweg wird angezeigt', 'Showing your saved path')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      {(journey?.levels || []).some((item: any) => item.total_lessons > 0) && <section className="cefr-journey compact" aria-label={tr(lang, 'Путь по уровням', 'Niveaureise', 'Level journey')}>
        <header><div><small>{tr(lang, 'УРОВЕНЬ', 'NIVEAU', 'LEVEL')}</small><h2>{tr(lang, 'Выбери доступный маршрут', 'Wähle einen verfügbaren Weg', 'Choose an available path')}</h2></div></header>
        <div className="cefr-levels">{(journey?.levels || []).filter((item: any) => item.total_lessons > 0).map((item: any) => {
          const accessible = ['active', 'review', 'completed'].includes(item.state);
          const label = item.state === 'active' ? tr(lang, 'Активный', 'Aktiv', 'Active') : item.state === 'review' ? tr(lang, 'Повторение', 'Wiederholen', 'Review') : item.state === 'completed' ? tr(lang, 'Пройден', 'Abgeschlossen', 'Completed') : item.state === 'coming_soon' ? tr(lang, 'Позже', 'Demnächst', 'Coming later') : tr(lang, 'Закрыт', 'Gesperrt', 'Locked');
          return <button type="button" key={item.level} className={`cefr-level ${item.state}${track === item.level ? ' selected' : ''}`} disabled={!accessible} onClick={() => accessible && setSelectedTrack(item.level)}>
            <span className="cefr-code">{item.level}</span><span><strong>{label}</strong><small>{item.total_lessons ? `${item.completed_lessons}/${item.total_lessons} ${tr(lang, 'уроков', 'Lektionen', 'lessons')}` : '—'}</small></span>{accessible ? item.state === 'completed' ? <FaCheck /> : <FaPlay /> : <FaLock />}
          </button>;
        })}</div>
        {(() => { const active = (journey?.levels || []).find((item: any) => item.state === 'active'); return active && active.completion >= 80 && active.mastery >= 70 ? <button type="button" className="rc-primary checkpoint-cta" onClick={() => navigate(withUser(`/checkpoint/${active.level}`))}>{tr(lang, `Пройти финальный тест ${active.level}`, `${active.level}-Abschlusstest starten`, `Take the ${active.level} final checkpoint`)}</button> : null; })()}
      </section>}

      <section className="rc-plan-now">
        <header><span>{tr(lang, 'ПРОДОЛЖИТЬ МАРШРУТ', 'WEG FORTSETZEN', 'CONTINUE YOUR PATH')}</span><small>{tr(lang, `Модуль ${week} из 4`, `Modul ${week} von 4`, `Module ${week} of 4`)}</small></header>
        <div><small>{moduleNames[week - 1]}</small><h2>{current?.title || topicLabel(current?.topic || 'word_order', lang)}</h2></div>
        <button type="button" className="rc-primary" disabled={!current?.id} onClick={() => current?.id && navigate(withUser(`/lesson/${current.id}`))}><span><FaPlay /> {current?.id ? tr(lang, 'Начать', 'Starten', 'Start') : tr(lang, 'Загрузка…', 'Laden…', 'Loading…')}</span></button>
      </section>

      <section className="rc-route">
        <header><div><small>{tr(lang, `МОДУЛЬ ${week} · ${routeCompleted}/${lessons.length || 20}`, `MODUL ${week} · ${routeCompleted}/${lessons.length || 20}`, `MODULE ${week} · ${routeCompleted}/${lessons.length || 20}`)}</small><h2>{tr(lang, 'Следующие шаги', 'Nächste Schritte', 'Next steps')}</h2></div><span>{routeProgress}%</span></header>
        <div className="rc-route-progress"><i style={{ width: `${routeProgress}%` }} /></div>
        <div className="rc-route-list">
          {upcoming.map((lesson, index) => {
            const locked = Array.isArray(lesson.blocked_by) && lesson.blocked_by.length > 0;
            const active = lesson.id === current?.id;
            const detail = lesson.completed
              ? tr(lang, 'Завершено', 'Abgeschlossen', 'Completed')
              : locked
                ? lesson.blocked_by?.includes('previous_step')
                  ? tr(lang, 'Сначала пройди предыдущий шаг', 'Zuerst den vorherigen Schritt abschließen', 'Complete the previous step first')
                  : tr(lang, 'Сначала закрепи базовый навык', 'Zuerst die Grundlage festigen', 'Strengthen the prerequisite first')
                : lesson.mastery == null
                  ? tr(lang, 'Доступно', 'Bereit', 'Ready')
                  : `${tr(lang, 'Освоено', 'Beherrscht', 'Mastery')} ${lesson.mastery}%`;
            return <button type="button" key={lesson.id || index} className={`rc-route-row${active ? ' active' : ''}${lesson.completed ? ' complete' : ''}`} disabled={locked} onClick={() => !locked && lesson.id && navigate(withUser(`/lesson/${lesson.id}`))}>
              <span className="rc-route-marker">{lesson.completed ? <FaCheck /> : locked ? <FaLock /> : index + 1}</span>
              <span><strong>{lesson.title || topicLabel(lesson.topic, lang)}</strong><small>{detail}</small></span>
              {!locked && <span className="rc-route-arrow">›</span>}
            </button>;
          })}
          {!upcoming.length && <div className="rc-empty-inline"><span>{tr(lang, 'Следующие шаги появятся после этого урока.', 'Die nächsten Schritte erscheinen nach dieser Lektion.', 'Your next steps will appear after this lesson.')}</span></div>}
        </div>
        {weekLessons.length > 5 && <button type="button" className="rc-text-action" onClick={() => setShowWeek(value => !value)}>{showWeek ? tr(lang, 'Показать меньше шагов', 'Weniger Schritte anzeigen', 'Show fewer steps') : tr(lang, 'Показать весь модуль', 'Ganzes Modul anzeigen', 'Show full module')} <FaChevronDown className={showWeek ? 'rotated' : ''} /></button>}
      </section>
    </main>
  );
};
