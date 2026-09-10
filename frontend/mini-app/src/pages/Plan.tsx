import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaCheck, FaChevronDown, FaLock, FaPlay } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const Plan: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [lessons, setLessons] = useState<any[]>([]);
  const [dashboard, setDashboard] = useState<any>(null);
  const [showWeek, setShowWeek] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const userId = getUserId();

  const load = useCallback(async () => {
    const [plan, profile] = await Promise.allSettled([api.getPlan(userId), api.getDashboard(userId)]);
    if (plan.status === 'fulfilled') setLessons(Array.isArray(plan.value) ? plan.value : []);
    if (profile.status === 'fulfilled') setDashboard(profile.value);
    else setDashboard({ level: 'A1', targetLevel: 'A2' });
    setLoadError(plan.status === 'rejected' || profile.status === 'rejected');
  }, [userId]);

  useEffect(() => { void load(); }, [load]);

  const current = useMemo(() => lessons.find(item => !item.completed && !(Array.isArray(item.blocked_by) && item.blocked_by.length)) || lessons.find(item => !item.completed) || lessons[0], [lessons]);
  const week = Number(current?.week || 1);
  const weekLessons = lessons.filter(item => Number(item.week || 1) === week);
  const visible = showWeek ? weekLessons : weekLessons.slice(0, 5);
  const completed = weekLessons.filter(item => item.completed).length;
  const total = weekLessons.length || 7;
  const progress = Math.round((completed / total) * 100);
  const routeCompleted = lessons.filter(item => item.completed).length;
  const weekdays = lang === 'ru' ? ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'] : ['MO', 'DI', 'MI', 'DO', 'FR', 'SA', 'SO'];

  if (!dashboard) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className="app-shell rc-page rc-plan page-enter">
      <header className="rc-page-title">
        <p>{lang === 'ru' ? 'ПЛАН' : 'PLAN'}</p>
        <h1>{dashboard.level || 'A1'} <span>→</span> {dashboard.targetLevel || 'A2'}</h1>
        <span>{lang === 'ru' ? `${routeCompleted} из ${lessons.length || 30} тем освоено` : `${routeCompleted} von ${lessons.length || 30} Themen gelernt`}</span>
      </header>

      {loadError && <div className="rc-notice error"><span>{lang === 'ru' ? 'Не удалось полностью обновить маршрут' : 'Die Route konnte nicht vollständig aktualisiert werden'}</span><button type="button" onClick={load}>{lang === 'ru' ? 'Обновить' : 'Aktualisieren'}</button></div>}

      <section className="rc-plan-now">
        <header><span>{lang === 'ru' ? 'СЛЕДУЮЩИЙ УРОК' : 'NÄCHSTE LEKTION'}</span></header>
        <div><small>{lang === 'ru' ? 'РЕКОМЕНДОВАНО' : 'EMPFOHLEN'}</small><h2>{topicLabel(current?.topic || 'word_order', lang)}</h2></div>
        <button type="button" className="rc-primary" disabled={!current?.id} onClick={() => current?.id && navigate(withUser(`/lesson/${current.id}`))}><span><FaPlay /> {current?.id ? (lang === 'ru' ? 'Начать' : 'Starten') : (lang === 'ru' ? 'Загрузка…' : 'Laden…')}</span></button>
      </section>

      <section className="rc-week-progress">
        <header><div><small>{lang === 'ru' ? `НЕДЕЛЯ ${week}` : `WOCHE ${week}`}</small><h2>{lang === 'ru' ? 'Календарь занятий' : 'Lernkalender'}</h2></div><strong>{completed}/{total}</strong></header>
        <div className="rc-week-days">{weekdays.map((day, index) => <div key={day} className={index < completed ? 'done' : index === completed ? 'current' : ''}><span>{day}</span><i>{index < completed ? <FaCheck /> : index + 1}</i></div>)}</div>
        <div className="rc-meter"><i style={{ width: `${progress}%` }} /></div>
      </section>

      <section className="rc-route">
        <header><div><small>{lang === 'ru' ? 'МАРШРУТ' : 'ROUTE'}</small><h2>{lang === 'ru' ? 'Следующие навыки' : 'Nächste Fähigkeiten'}</h2></div><span>{progress}%</span></header>
        <div className="rc-route-list">
          {visible.map((lesson, index) => {
            const locked = Array.isArray(lesson.blocked_by) && lesson.blocked_by.length > 0;
            const active = lesson.id === current?.id;
            const detail = lesson.completed
              ? (lang === 'ru' ? 'Завершено' : 'Abgeschlossen')
              : locked
                ? (lang === 'ru' ? 'Сначала заверши предыдущий этап' : 'Zuerst die vorherige Etappe abschließen')
                : lesson.mastery == null
                  ? (lang === 'ru' ? 'Доступно' : 'Bereit')
                  : `${lang === 'ru' ? 'Освоено' : 'Beherrscht'} ${lesson.mastery}%`;
            return <button type="button" key={lesson.id || index} className={`rc-route-row${active ? ' active' : ''}${lesson.completed ? ' complete' : ''}`} disabled={locked} onClick={() => !locked && lesson.id && navigate(withUser(`/lesson/${lesson.id}`))}>
              <span className="rc-route-marker">{lesson.completed ? <FaCheck /> : locked ? <FaLock /> : index + 1}</span>
              <span><strong>{topicLabel(lesson.topic, lang)}</strong><small>{detail}</small></span>
              {!locked && <span className="rc-route-arrow">›</span>}
            </button>;
          })}
          {!visible.length && <div className="rc-empty-inline"><span>{lang === 'ru' ? 'Маршрут появится после диагностики.' : 'Deine Route erscheint nach der Diagnose.'}</span></div>}
        </div>
        {weekLessons.length > 5 && <button type="button" className="rc-text-action" onClick={() => setShowWeek(value => !value)}>{showWeek ? (lang === 'ru' ? 'Скрыть дополнительные дни' : 'Weitere Tage ausblenden') : (lang === 'ru' ? 'Показать всю неделю' : 'Ganze Woche anzeigen')} <FaChevronDown className={showWeek ? 'rotated' : ''} /></button>}
      </section>
    </main>
  );
};
