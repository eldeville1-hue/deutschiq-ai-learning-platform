import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaChevronDown } from 'react-icons/fa';
import { useLocation, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { tr } from '../i18n/language';

export const Result: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const [data, setData] = useState<any>(null);
  const [showAll, setShowAll] = useState(false);
  useEffect(() => {
    const state = (location.state as any)?.result;
    if (state) return setData(state);
    try { setData(JSON.parse(sessionStorage.getItem(`deutschiq-result-${getUserId()}`) || 'null')); } catch { setData(null); }
  }, [location]);
  if (!data) return <main className="app-shell empty-state">{tr(lang, 'Результат не найден', 'Ergebnis nicht gefunden', 'Result not found')}</main>;
  const mistakes = Array.isArray(data.mistakes) ? data.mistakes : [];
  const visible = showAll ? mistakes : mistakes.slice(0, 3);
  const pillars = [
    ['grammar', topicLabel('grammar', lang)],
    ['vocabulary', topicLabel('vocabulary', lang)],
    ['listening', topicLabel('listening', lang)],
    ['pronunciation', topicLabel('pronunciation', lang)],
  ];
  const percent = (value: any) => Math.round(Number(value || 0) * (Number(value || 0) <= 10 ? 10 : 1));
  return (
    <main className="app-shell result-page page-enter">
      <header className="result-hero"><span className="result-icon"><FaCheck /></span><p className="eyebrow">{tr(lang, 'Предварительная оценка уровня', 'Vorläufige Niveaueinschätzung', 'Preliminary level estimate')}</p><h1>{data.level || 'A1'}</h1><strong>{Math.round(data.overall_score || 0)}%</strong><p>{tr(lang, 'Это стартовая оценка по ответам в тесте. Говорение и аудирование уточнят её во время занятий.', 'Das ist eine erste Einschätzung aus deinen Testantworten. Sprechen und Hören präzisieren sie im Training.', 'This is a starting estimate from your test answers. Speaking and listening practice will refine it.')}</p></header>
      <section className="result-skills">{pillars.map(([key, label]) => { const assessed = data.skill_status?.[key] !== 'not_assessed'; return <div key={key}><span>{label}</span><b>{assessed ? `${percent(data.pillars?.[key])}%` : tr(lang, 'Не проверено', 'Nicht geprüft', 'Not assessed')}</b>{assessed && <div className="progress-bar"><div className="progress-bar-fill progress-fill" style={{ width: `${percent(data.pillars?.[key])}%` }} /></div>}</div>; })}</section>
      <section><div className="section-heading"><span>{tr(lang, `Темы для улучшения · ${mistakes.length}`, `Lernfelder · ${mistakes.length}`, `Areas to improve · ${mistakes.length}`)}</span></div><div className="result-mistakes">{visible.map((mistake: any, index: number) => <div key={index}><span>{index + 1}</span><p>{topicLabel(String(mistake.tag || mistake.weak_tag || mistake.topic || mistake.question || 'grammar'), lang)}</p></div>)}</div>{mistakes.length > 3 && <button className="secondary-action" onClick={() => setShowAll(v => !v)}>{showAll ? tr(lang, 'Скрыть', 'Weniger anzeigen', 'Show less') : tr(lang, 'Показать все темы', 'Alle Lernfelder anzeigen', 'Show all areas')} <FaChevronDown /></button>}</section>
      <section className="next-step"><p className="eyebrow">{tr(lang, 'Следующий шаг', 'Nächster Schritt', 'Next step')}</p><h2>{tr(lang, 'Разберём приоритетные темы', 'Wir trainieren deine wichtigsten Lernfelder', 'Train your priority areas')}</h2><button className="primary-action" onClick={() => navigate(withUser('/plan'))}>{tr(lang, 'Открыть мой план', 'Meinen Lernplan öffnen', 'Open my plan')} <FaArrowRight /></button></section>
    </main>
  );
};
