import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FaChartLine, FaComments, FaHome, FaRegCalendarAlt, FaUser } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';
import { getText } from '../i18n/translations';
import { withUser } from '../utils/user';

export const BottomNav: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { lang } = useLanguage();
  const t = getText(lang);
  const tabs = [
    ['/dashboard', FaHome, t.nav.overview],
    ['/analytics', FaChartLine, t.nav.analysis],
    ['/plan', FaRegCalendarAlt, t.nav.plan],
    ['/tutor', FaComments, t.nav.tutor],
    ['/profile', FaUser, t.nav.profile],
  ] as const;
  const openTab = (path: string) => {
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    document.querySelector<HTMLElement>('.app-shell')?.scrollTo({ top: 0, left: 0, behavior: 'auto' });
    navigate(withUser(path));
  };

  return <nav className="bottom-nav" aria-label={lang === 'ru' ? 'Основная навигация' : 'Hauptnavigation'}>{tabs.map(([path, Icon, label]) => {
    const active = location.pathname === path;
    return <button type="button" key={path} className={active ? 'active' : ''} aria-current={active ? 'page' : undefined} aria-label={label} onClick={() => openTab(path)}><Icon aria-hidden="true" /><span>{label}</span></button>;
  })}</nav>;
};
