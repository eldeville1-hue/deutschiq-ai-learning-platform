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
  const [showWeek, setShowWeek] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const userId = getUserId();

  const load = useCallback(async () => {
    const [plan, profile] = await Promise.allSettled([api.getPlan(userId, lang), api.getDashboard(userId)]);
    if (plan.status === 'fulfilled') setLessons(Array.isArray(plan.value) ? plan.value : []);
    if (profile.status === 'fulfilled') setDashboard(profile.value);
    else setDashboard({ level: 'A1', targetLevel: 'A2' });
    setLoadError(plan.status === 'rejected' || profile.status === 'rejected');
  }, [lang, userId]);

  useEffect(() => { void load(); }, [load]);

  const current = useMemo(() => lessons.find(item => !item.completed && !(Array.isArray(item.blocked_by) && item.blocked_by.length)) || lessons.find(item => !item.completed) || lessons[0], [lessons]);
  const week = Number(current?.week || 1);
  const weekLessons = lessons.filter(item => Number(item.week || 1) === week);
  const visible = showWeek ? weekLessons : weekLessons.slice(0, 5);
  const completed = weekLessons.filter(item => item.completed).length;
  const total = weekLessons.length || 7;
  const progress = Math.round((completed / total) * 100);
  const routeCompleted = lessons.filter(item => item.completed).length;
  const weekdays = lang === 'ru' ? ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'] : lang === 'de' ? ['MO', 'DI', 'MI', 'DO', 'FR', 'SA', 'SO'] : ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'];

  if (!dashboard) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className="app-shell rc-page rc-plan page-enter">
      <header className="rc-page-title">
        <p>{tr(lang, 'ПЛАН', 'PLAN', 'PLAN')}</p>
        <h1>{dashboard.level || 'A1'} <span>→</span> {dashboard.targetLevel || 'A2'}</h1>
        <span>{tr(lang, `${routeCompleted} из ${lessons.length || 30} тем освоено`, `${routeCompleted} von ${lessons.length || 30} Themen gelernt`, `${routeCompleted} of ${lessons.length || 30} topics mastered`)}</span>
      </header>

      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Не удалось полностью обновить маршрут', 'Die Route konnte nicht vollständig aktualisiert werden', 'The learning path could not be fully refreshed')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <section className="rc-plan-now">
        <header><span>{tr(lang, 'СЛЕДУЮЩИЙ УРОК', 'NÄCHSTE LEKTION', 'NEXT LESSON')}</span></header>
        <div><small>{tr(lang, 'РЕКОМЕНДОВАНО', 'EMPFOHLEN', 'RECOMMENDED')}</small><h2>{current?.title || topicLabel(current?.topic || 'word_order', lang)}</h2></div>
        <button type="button" className="rc-primary" disabled={!current?.id} onClick={() => current?.id && navigate(withUser(`/lesson/${current.id}`))}><span><FaPlay /> {current?.id ? tr(lang, 'Начать', 'Starten', 'Start') : tr(lang, 'Загрузка…', 'Laden…', 'Loading…')}</span></button>
      </section>

      <section className="rc-week-progress">
        <header><div><small>{tr(lang, `НЕДЕЛЯ ${week}`, `WOCHE ${week}`, `WEEK ${week}`)}</small><h2>{tr(lang, 'Календарь занятий', 'Lernkalender', 'Learning calendar')}</h2></div><strong>{completed}/{total}</strong></header>
        <div className="rc-week-days">{weekdays.map((day, index) => <div key={day} className={index < completed ? 'done' : index === completed ? 'current' : ''}><span>{day}</span><i>{index < completed ? <FaCheck /> : index + 1}</i></div>)}</div>
        <div className="rc-meter"><i style={{ width: `${progress}%` }} /></div>
      </section>

      <section className="rc-route">
        <header><div><small>{tr(lang, 'МАРШРУТ', 'ROUTE', 'PATH')}</small><h2>{tr(lang, 'Следующие навыки', 'Nächste Fähigkeiten', 'Next skills')}</h2></div><span>{progress}%</span></header>
        <div className="rc-route-list">
          {visible.map((lesson, index) => {
            const locked = Array.isArray(lesson.blocked_by) && lesson.blocked_by.length > 0;
            const active = lesson.id === current?.id;
            const detail = lesson.completed
              ? tr(lang, 'Завершено', 'Abgeschlossen', 'Completed')
              : locked
                ? tr(lang, 'Сначала заверши предыдущий этап', 'Zuerst die vorherige Etappe abschließen', 'Complete the previous step first')
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
        {weekLessons.length > 5 && <button type="button" className="rc-text-action" onClick={() => setShowWeek(value => !value)}>{showWeek ? tr(lang, 'Скрыть дополнительные дни', 'Weitere Tage ausblenden', 'Show fewer days') : tr(lang, 'Показать всю неделю', 'Ganze Woche anzeigen', 'Show full week')} <FaChevronDown className={showWeek ? 'rotated' : ''} /></button>}
      </section>
    </main>
  );
};
