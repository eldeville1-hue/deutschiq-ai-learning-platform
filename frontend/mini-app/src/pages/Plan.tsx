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
    tr(lang, 'Порядок слов', 'Satzbau', 'Word order'),
    tr(lang, 'Падежи', 'Fälle', 'Cases'),
    tr(lang, 'Артикли', 'Artikel', 'Articles'),
    tr(lang, 'Прошедшее время', 'Vergangenheit', 'Past tense'),
  ];

  if (!dashboard) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className="app-shell rc-page rc-plan page-enter">
      <header className="rc-page-title">
        <p>{tr(lang, 'ПЛАН', 'PLAN', 'PLAN')}</p>
        <h1>{dashboard.level || 'A1'} <span>→</span> {dashboard.targetLevel || 'A2'}</h1>
        <span>{tr(lang, 'Твой маршрут по навыкам', 'Dein Weg nach Fähigkeiten', 'Your skill-based path')}</span>
      </header>

      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Не удалось полностью обновить маршрут', 'Die Route konnte nicht vollständig aktualisiert werden', 'The learning path could not be fully refreshed')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <section className="cefr-journey" aria-label={tr(lang, 'Путь по уровням', 'Niveaureise', 'Level journey')}>
        <header><div><small>{tr(lang, 'ТВОЙ ПУТЬ', 'DEIN WEG', 'YOUR JOURNEY')}</small><h2>{tr(lang, 'Уровни немецкого', 'Deine Deutschniveaus', 'Your German levels')}</h2></div><span>{tr(lang, 'Освоение, не спешка', 'Können statt Tempo', 'Mastery over speed')}</span></header>
        <div className="cefr-levels">{(journey?.levels || []).map((item: any) => {
          const accessible = ['active', 'review', 'completed'].includes(item.state);
          const label = item.state === 'active' ? tr(lang, 'Активный', 'Aktiv', 'Active') : item.state === 'review' ? tr(lang, 'Повторение', 'Wiederholen', 'Review') : item.state === 'completed' ? tr(lang, 'Пройден', 'Abgeschlossen', 'Completed') : item.state === 'coming_soon' ? tr(lang, 'Позже', 'Demnächst', 'Coming later') : tr(lang, 'Закрыт', 'Gesperrt', 'Locked');
          return <button type="button" key={item.level} className={`cefr-level ${item.state}${track === item.level ? ' selected' : ''}`} disabled={!accessible} onClick={() => accessible && setSelectedTrack(item.level)}>
            <span className="cefr-code">{item.level}</span><span><strong>{label}</strong><small>{item.total_lessons ? `${item.completed_lessons}/${item.total_lessons} · ${item.mastery}%` : '—'}</small></span>{accessible ? item.state === 'completed' ? <FaCheck /> : <FaPlay /> : <FaLock />}
          </button>;
        })}</div>
        <p>{tr(lang, 'Нижние уровни доступны для повторения. Следующий уровень откроется после 80% уроков и 70% освоения.', 'Frühere Niveaus bleiben zum Wiederholen offen. Das nächste Niveau öffnet sich nach 80 % der Lektionen und 70 % Beherrschung.', 'Earlier levels remain open for review. The next level unlocks after 80% lesson completion and 70% mastery.')}</p>
        {(() => { const active = (journey?.levels || []).find((item: any) => item.state === 'active'); return active && active.completion >= 80 && active.mastery >= 70 ? <button type="button" className="rc-primary checkpoint-cta" onClick={() => navigate(withUser(`/checkpoint/${active.level}`))}>{tr(lang, `Пройти финальный тест ${active.level}`, `${active.level}-Abschlusstest starten`, `Take the ${active.level} final checkpoint`)}</button> : null; })()}
      </section>

      <section className="rc-plan-now">
        <header><span>{tr(lang, 'СЛЕДУЮЩИЙ УРОК', 'NÄCHSTE LEKTION', 'NEXT LESSON')}</span></header>
        <div><small>{tr(lang, 'РЕКОМЕНДОВАНО', 'EMPFOHLEN', 'RECOMMENDED')}</small><h2>{current?.title || topicLabel(current?.topic || 'word_order', lang)}</h2></div>
        <button type="button" className="rc-primary" disabled={!current?.id} onClick={() => current?.id && navigate(withUser(`/lesson/${current.id}`))}><span><FaPlay /> {current?.id ? tr(lang, 'Начать', 'Starten', 'Start') : tr(lang, 'Загрузка…', 'Laden…', 'Loading…')}</span></button>
      </section>

      <section className="rc-plan-progress">
        <header><span>{tr(lang, 'ПРОГРЕСС', 'FORTSCHRITT', 'PROGRESS')}</span><strong>{routeCompleted}/{lessons.length || 30}</strong></header>
        <div className="rc-meter"><i style={{ width: `${routeProgress}%` }} /></div>
        <div className="rc-module-strip">{moduleNames.map((name, index) => <span key={name} className={index + 1 < week ? 'done' : index + 1 === week ? 'current' : ''}>{index + 1}. {name}</span>)}</div>
      </section>

      <section className="rc-route">
        <header><div><small>{tr(lang, `МОДУЛЬ ${week}`, `MODUL ${week}`, `MODULE ${week}`)}</small><h2>{moduleNames[week - 1] || tr(lang, 'Следующие навыки', 'Nächste Fähigkeiten', 'Next skills')}</h2></div><span>{routeProgress}%</span></header>
        <div className="rc-route-list">
          {visible.map((lesson, index) => {
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
          {!visible.length && <div className="rc-empty-inline"><span>{tr(lang, 'Маршрут появится после диагностики.', 'Deine Route erscheint nach der Diagnose.', 'Your learning path will appear after the placement test.')}</span></div>}
        </div>
        {weekLessons.length > 5 && <button type="button" className="rc-text-action" onClick={() => setShowWeek(value => !value)}>{showWeek ? tr(lang, 'Показать меньше шагов', 'Weniger Schritte anzeigen', 'Show fewer steps') : tr(lang, 'Показать весь модуль', 'Ganzes Modul anzeigen', 'Show full module')} <FaChevronDown className={showWeek ? 'rotated' : ''} /></button>}
      </section>
    </main>
  );
};
