import React, { useEffect, useMemo, useState } from 'react';
import { FaChevronDown, FaClock, FaLock, FaPlay } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { BottomNav } from '../components/BottomNav';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const Plan: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [lessons, setLessons] = useState<any[]>([]);
  const [dashboard, setDashboard] = useState<any>(null);
  const [showWeek, setShowWeek] = useState(false);
  const userId = getUserId();
  useEffect(() => { Promise.all([api.getPlan(userId), api.getDashboard(userId)]).then(([p, d]) => { setLessons(Array.isArray(p) ? p : []); setDashboard(d); }).catch(() => setDashboard({ level: 'A1', targetLevel: 'A2' })); }, [userId]);
  const current = useMemo(() => lessons.find(x => !x.completed) || lessons[0], [lessons]);
  const week = Number(current?.week || 1);
  const weekLessons = lessons.filter(x => Number(x.week || 1) === week);
  const visible = showWeek ? weekLessons : weekLessons.slice(0, 3);
  const completed = weekLessons.filter(x => x.completed).length;
  const weekTitle = ['word_order', 'dative_case', 'articles', 'perfekt_auxiliary'][week - 1] || 'word_order';

  if (!dashboard) return <div className="app-shell"><div className="skeleton hero-skeleton" /></div>;
  return (
    <main className="app-shell compact-page plan-page precision-plan page-enter">
      <header className="page-header"><div><p className="eyebrow">{lang === 'ru' ? 'Твой план' : 'Dein Lernplan'}</p><h1>{dashboard.level || 'A1'} → {dashboard.targetLevel || 'A2'}</h1></div></header>
      <section className="today-focus">
        <div className="section-heading"><span>{lang === 'ru' ? 'Сегодня' : 'Heute'}</span><small><FaClock /> {current?.estimated_time || 12} {lang === 'ru' ? 'мин' : 'Min.'}</small></div>
        <span className="day-label">{lang === 'ru' ? 'День' : 'Tag'} {current?.day || 1}</span>
        <h2>{topicLabel(current?.topic || 'word_order', lang)}</h2>
        <button className="primary-action" onClick={() => current?.id && navigate(withUser(`/lesson/${current.id}`))}><FaPlay /> {lang === 'ru' ? 'Начать' : 'Starten'}</button>
      </section>
      <section>
        <div className="section-heading"><span>{lang === 'ru' ? `Неделя ${week}` : `Woche ${week}`} · {topicLabel(weekTitle, lang)}</span><small>{completed}/{weekLessons.length || 7}</small></div>
        <div className="progress-bar"><div className="progress-bar-fill" style={{ width: `${weekLessons.length ? completed / weekLessons.length * 100 : 0}%` }} /></div>
        <div className="lesson-list">
          {visible.map((lesson, index) => {
            const locked = dashboard.subscription_status !== 'pro' && Number(lesson.day) > 3;
            return <button key={lesson.id} className="lesson-row" onClick={() => !locked && navigate(withUser(`/lesson/${lesson.id}`))}><span className="lesson-number">{lesson.completed ? '✓' : index + 1}</span><span><b>{topicLabel(lesson.topic, lang)}</b><small>{lesson.mastery == null ? `${lesson.estimated_time || 12} ${lang === 'ru' ? 'мин' : 'Min.'}` : `${lang === 'ru' ? 'Освоено' : 'Beherrscht'} ${lesson.mastery}%`}</small></span>{locked ? <FaLock /> : <span>›</span>}</button>;
          })}
          {!visible.length && <p className="empty-state">{lang === 'ru' ? 'Уроки появятся после загрузки плана.' : 'Die Lektionen erscheinen nach dem Laden des Plans.'}</p>}
        </div>
        {weekLessons.length > 3 && <button className="secondary-action" onClick={() => setShowWeek(v => !v)}>{showWeek ? (lang === 'ru' ? 'Свернуть' : 'Weniger') : (lang === 'ru' ? 'Показать всю неделю' : 'Ganze Woche anzeigen')} <FaChevronDown /></button>}
      </section>
      <BottomNav />
    </main>
  );
};
