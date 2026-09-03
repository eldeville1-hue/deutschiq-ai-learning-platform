import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaBolt, FaClock, FaExclamation, FaFire, FaLayerGroup, FaRedoAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { BottomNav } from '../components/BottomNav';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const Dashboard: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [lesson, setLesson] = useState<any>(null);
  const [learning, setLearning] = useState<any>(null);
  const userId = getUserId();

  useEffect(() => {
    Promise.allSettled([api.getDashboard(userId), api.getPlan(userId), api.getLearningToday(userId)]).then(([dashboard, plan, today]) => {
      if (dashboard.status === 'fulfilled') setData(dashboard.value);
      if (plan.status === 'fulfilled') {
        const items = Array.isArray(plan.value) ? plan.value : [];
        setLesson(items.find((item: any) => !item.completed) || items[0]);
      }
      if (today.status === 'fulfilled') setLearning(today.value);
    });
  }, [userId]);

  if (!data) return <main className="app-shell"><div className="skeleton action-hero-skeleton" /></main>;
  const topic = lesson?.topic || data.weaknesses?.[0]?.name || 'haben_conjugation';
  const weak = data.weaknesses?.[0] || { name: 'articles', percent: 10 };
  const hour = new Date().getHours();
  const greeting = lang === 'ru'
    ? (hour < 12 ? 'ДОБРОЕ УТРО' : hour < 18 ? 'ДОБРЫЙ ДЕНЬ' : 'ДОБРЫЙ ВЕЧЕР')
    : (hour < 12 ? 'GUTEN MORGEN' : hour < 18 ? 'GUTEN TAG' : 'GUTEN ABEND');
  const startLesson = () => navigate(lesson?.id ? withUser(`/lesson/${lesson.id}`) : withUser('/plan'));

  return (
    <main className="app-shell dashboard-page precision-home page-enter">
      <header className="home-masthead page-stagger-1">
        <div className="home-brand"><span>D</span><div><small>{greeting}</small><strong>DeutschIQ</strong></div></div>
        <div className="home-streak"><FaFire /><b>{data.streak || 0}</b></div>
      </header>
      <section className="home-intro page-stagger-1"><h1>{lang === 'ru' ? 'Что изучаем сегодня?' : 'Was lernen wir heute?'}</h1><div><span>{data.level || 'A1'}</span><span>{data.xp || 0} XP</span></div></section>
      <section className="focus-stage page-stagger-2">
        <div className="focus-orbit" aria-hidden="true"><span>01</span></div>
        <div className="focus-kicker"><FaBolt />{lang === 'ru' ? 'СЛЕДУЮЩИЙ ШАГ' : 'NÄCHSTER SCHRITT'}</div>
        <h2>{topicLabel(topic, lang)}</h2>
        <p>{lang === 'ru' ? 'Пойми структуру, услышь пример и используй её в собственной немецкой фразе.' : 'Verstehe die Struktur, höre ein Beispiel und nutze sie in deinem eigenen Satz.'}</p>
        <div className="focus-meta"><span><FaClock />{lesson?.estimated_time || 12} {lang === 'ru' ? 'мин' : 'Min.'}</span><span><FaLayerGroup />3 {lang === 'ru' ? 'этапа' : 'Phasen'}</span></div>
        <button className="focus-start" onClick={startLesson}><span>{lang === 'ru' ? 'Начать занятие' : 'Training starten'}</span><FaArrowRight /></button>
      </section>
      <section className="home-actions page-stagger-3">
        <button onClick={() => navigate(withUser('/review'))}><span className="action-symbol"><FaRedoAlt /></span><span><small>{lang === 'ru' ? 'ПАМЯТЬ' : 'GEDÄCHTNIS'}</small><b>{learning?.due_count || 0} {lang === 'ru' ? 'к повторению' : 'fällig'}</b></span><FaArrowRight /></button>
        <button onClick={() => navigate(withUser('/mistakes'))}><span className="action-symbol danger"><FaExclamation /></span><span><small>{lang === 'ru' ? 'ФОКУС' : 'FOKUS'}</small><b>{topicLabel(String(weak.name), lang)}</b></span><FaArrowRight /></button>
      </section>
      <section className="session-strip page-stagger-4"><span>{lang === 'ru' ? 'Сегодня' : 'Heute'}</span><div><i className="done" /><i className="active" /><i /></div><strong>{learning?.session?.minutes || 12} {lang === 'ru' ? 'мин' : 'Min.'}</strong></section>
      <BottomNav />
    </main>
  );
};
