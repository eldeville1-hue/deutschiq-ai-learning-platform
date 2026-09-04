import React, { useEffect, useMemo, useState } from 'react';
import { FaBell, FaCheck, FaChevronRight, FaGlobe, FaMedal, FaMoon, FaRedo, FaShareAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { BottomNav } from '../components/BottomNav';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';
import { getTelegramUser, getUserId, withUser } from '../utils/user';

const CountUp: React.FC<{ value: number }> = ({ value }) => {
  const [shown, setShown] = useState(0);
  useEffect(() => { let frame = 0; const start = performance.now(); const tick = (now: number) => { const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; const p = reduced ? 1 : Math.min(1, (now - start) / 700); setShown(Math.round(value * (1 - Math.pow(1 - p, 3)))); if (p < 1) frame = requestAnimationFrame(tick); }; frame = requestAnimationFrame(tick); return () => cancelAnimationFrame(frame); }, [value]);
  return <>{shown}</>;
};

export const Profile: React.FC = () => {
  const { lang, toggleLang } = useLanguage();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [lessons, setLessons] = useState<any[]>([]);
  const user = getTelegramUser();
  const name = user?.first_name || (lang === 'ru' ? 'Пользователь' : 'Lernende');
  useEffect(() => { Promise.allSettled([api.getDashboard(getUserId()), api.getPlan(getUserId())]).then(([d, p]) => { setData(d.status === 'fulfilled' ? d.value : {}); setLessons(p.status === 'fulfilled' && Array.isArray(p.value) ? p.value : []); }); }, []);
  const completed = useMemo(() => lessons.filter(item => item.completed).length, [lessons]);
  if (!data) return <main className="app-shell"><div className="skeleton profile-skeleton" /></main>;
  const activityCount = Math.max(completed, data.diagnostic_completed ? 1 : 0);
  const retake = () => { const ok = window.confirm(lang === 'ru' ? 'Пройти диагностику заново? Новый результат заменит текущую оценку уровня.' : 'Diagnose wiederholen? Das neue Ergebnis ersetzt deine aktuelle Einstufung.'); if (ok) navigate(withUser('/diagnostic?retake=true')); };
  const share = () => window.open(`https://t.me/share/url?url=https://t.me/DeutschIQ_bot?start=ref_${getUserId()}&text=DeutschIQ`, '_blank');
  const weekdays = lang === 'ru' ? ['ПН','ВТ','СР','ЧТ','ПТ','СБ','ВС'] : ['MO','DI','MI','DO','FR','SA','SO'];

  return (
    <main className="app-shell profile-page precision-profile page-enter">
      <header className="profile-masthead page-stagger-1"><span>{lang === 'ru' ? 'ПРОФИЛЬ' : 'PROFIL'}</span><b>DeutschIQ</b></header>
      <section className="profile-passport page-stagger-1"><div className="avatar">{name.slice(0, 2).toUpperCase()}</div><div><small>{lang === 'ru' ? 'УЧЕНИК' : 'LERNENDE'}</small><h1>{name}</h1><p>{lang === 'ru' ? 'Немецкий каждый день' : 'Deutsch jeden Tag'}</p></div><strong>{data.level || 'A1'}</strong></section>
      <section className="profile-numbers page-stagger-2"><div><strong><CountUp value={data.xp || 0} /></strong><span>XP</span></div><div><strong>{completed}</strong><span>{lang === 'ru' ? 'уроков' : 'Lektionen'}</span></div><div><strong>{activityCount}</strong><span>{lang === 'ru' ? 'активностей' : 'Aktivitäten'}</span></div></section>
      <section className="streak-section page-stagger-2"><small>{lang === 'ru' ? 'ТВОЯ СЕРИЯ' : 'DEINE SERIE'}</small><h2>{data.streak || 0} {lang === 'ru' ? 'дней' : 'Tage'}</h2><div className="week-row">{weekdays.map((day, index) => <div key={day} style={{ animationDelay: `${index * 55}ms` }}><span>{day}</span><i className={index < (data.streak || 0) ? 'active' : ''} /></div>)}</div></section>
      <section className="achievement-section page-stagger-3"><header><small>{lang === 'ru' ? 'ДОСТИЖЕНИЯ' : 'ERFOLGE'}</small><span>1 / 8 <FaChevronRight /></span></header><div><FaMedal /><span><b>{lang === 'ru' ? 'Первый шаг' : 'Erster Schritt'}</b><small>{lang === 'ru' ? 'Диагностика завершена' : 'Diagnose abgeschlossen'} <FaCheck /></small></span></div></section>
      {data.subscription_status !== 'pro' && <section className="pro-section page-stagger-3"><h2>DeutschIQ Pro</h2><p>{lang === 'ru' ? 'Больше практики, полный анализ ошибок и ИИ-репетитор.' : 'Mehr Übung, vollständige Fehleranalyse und KI-Tutor.'}</p><button disabled>{lang === 'ru' ? 'Скоро' : 'Demnächst'}</button></section>}
      <section className="profile-settings page-stagger-4"><button onClick={toggleLang}><span><FaGlobe />{lang === 'ru' ? 'Язык интерфейса' : 'App-Sprache'}</span><small>{lang === 'ru' ? 'Русский' : 'Deutsch'}</small><FaChevronRight /></button><button onClick={toggleTheme}><span><FaMoon />{lang === 'ru' ? 'Оформление' : 'Darstellung'}</span><small>{theme === 'dark' ? (lang === 'ru' ? 'Тёмное' : 'Dunkel') : (lang === 'ru' ? 'Светлое' : 'Hell')}</small><FaChevronRight /></button><button disabled><span><FaBell />{lang === 'ru' ? 'Уведомления' : 'Benachrichtigungen'}</span><small>{lang === 'ru' ? 'Скоро' : 'Demnächst'}</small></button><button onClick={share}><span><FaShareAlt />{lang === 'ru' ? 'Пригласить друга' : 'Freund einladen'}</span><FaChevronRight /></button></section>
      <button className="retake-link" onClick={retake}><FaRedo /> {lang === 'ru' ? 'Пройти диагностику заново' : 'Diagnose wiederholen'}</button>
      <nav className="legal-links"><a href="/privacy">Datenschutz</a><a href="/imprint">Impressum</a><a href="/terms">Nutzung</a></nav>
      <small className="build-version">DeutschIQ 15.0.0 · Production</small>
      <BottomNav />
    </main>
  );
};
