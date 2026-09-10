import React, { useEffect, useMemo, useState } from 'react';
import { FaChevronDown, FaClock, FaLock, FaPlay } from 'react-icons/fa';
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
  useEffect(() => { Promise.all([api.getPlan(userId), api.getDashboard(userId)]).then(([p, d]) => { setLessons(Array.isArray(p) ? p : []); setDashboard(d); setLoadError(false); }).catch(() => { setDashboard({ level: 'A1', targetLevel: 'A2' }); setLoadError(true); }); }, [userId]);
  const current = useMemo(() => lessons.find(x => !x.completed) || lessons[0], [lessons]);
  const week = Number(current?.week || 1);
  const weekLessons = lessons.filter(x => Number(x.week || 1) === week);
  const visible = showWeek ? weekLessons : weekLessons.slice(0, 3);
  const completed = weekLessons.filter(x => x.completed).length;
  const weekTitle = weekLessons[0]?.topic || current?.topic || 'word_order';

  if (!dashboard) return <div className="app-shell"><div className="skeleton hero-skeleton" /></div>;
  return (
    <main className="app-shell compact-page plan-page precision-plan v30-page v30-plan page-enter">
      <header className="page-header"><div><p className="eyebrow">{lang === 'ru' ? 'Твой план' : 'Dein Lernplan'}</p><h1>{dashboard.level || 'A1'} → {dashboard.targetLevel || 'A2'}</h1></div></header>
      {loadError && <div className="v30-status error"><span>{lang === 'ru' ? 'Не удалось обновить план' : 'Plan konnte nicht aktualisiert werden'}</span><button onClick={() => window.location.reload()}>{lang === 'ru' ? 'Повторить' : 'Erneut laden'}</button></div>}
      <section className="today-focus">
        <div className="section-heading"><span>{lang === 'ru' ? 'Сегодня' : 'Heute'}</span><small><FaClock /> {current?.estimated_time || 12} {lang === 'ru' ? 'мин' : 'Min.'}</small></div>
        <span className="day-label">{lang === 'ru' ? 'День' : 'Tag'} {current?.day || 1}</span>
        <h2>{topicLabel(current?.topic || 'word_order', lang)}</h2>
        <button type="button" className="primary-action" disabled={!current?.id} onClick={() => current?.id && navigate(withUser(`/lesson/${current.id}`))}><FaPlay /> {current?.id ? (lang === 'ru' ? 'Начать' : 'Starten') : (lang === 'ru' ? 'План ещё загружается' : 'Plan wird geladen')}</button>
      </section>
      <section>
        <div className="section-heading"><span>{lang === 'ru' ? `Неделя ${week}` : `Woche ${week}`} · {topicLabel(weekTitle, lang)}</span><small>{completed}/{weekLessons.length || 7}</small></div>
        <div className="progress-bar"><div className="progress-bar-fill" style={{ width: `${weekLessons.length ? completed / weekLessons.length * 100 : 0}%` }} /></div>
        <div className="lesson-list">
          {visible.map((lesson, index) => {
            const locked = Array.isArray(lesson.blocked_by) && lesson.blocked_by.length > 0;
            const detail = locked
              ? `${lang === 'ru' ? 'Сначала' : 'Zuerst'}: ${lesson.blocked_by.map((topic: string) => topicLabel(topic, lang)).join(', ')}`
              : lesson.mastery == null ? `${lesson.estimated_time || 12} ${lang === 'ru' ? 'мин' : 'Min.'}` : `${lang === 'ru' ? 'Освоено' : 'Beherrscht'} ${lesson.mastery}%`;
            return <button type="button" key={lesson.id} className="lesson-row" disabled={locked} aria-label={`${topicLabel(lesson.topic, lang)}${locked ? ` — ${lang === 'ru' ? 'заблокировано' : 'gesperrt'}` : ''}`} onClick={() => !locked && navigate(withUser(`/lesson/${lesson.id}`))}><span className="lesson-number">{lesson.completed ? '✓' : index + 1}</span><span><b>{topicLabel(lesson.topic, lang)}</b><small>{detail}</small></span>{locked ? <FaLock /> : <span>›</span>}</button>;
          })}
          {!visible.length && <p className="empty-state">{lang === 'ru' ? 'Уроки появятся после загрузки плана.' : 'Die Lektionen erscheinen nach dem Laden des Plans.'}</p>}
        </div>
        {weekLessons.length > 3 && <button className="secondary-action" onClick={() => setShowWeek(v => !v)}>{showWeek ? (lang === 'ru' ? 'Свернуть' : 'Weniger') : (lang === 'ru' ? 'Показать всю неделю' : 'Ganze Woche anzeigen')} <FaChevronDown /></button>}
      </section>
    </main>
  );
};
