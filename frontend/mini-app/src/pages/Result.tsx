import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaChevronDown } from 'react-icons/fa';
import { useLocation, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

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
  if (!data) return <main className="app-shell empty-state">{lang === 'ru' ? 'Результат не найден' : 'Ergebnis nicht gefunden'}</main>;
  const mistakes = Array.isArray(data.mistakes) ? data.mistakes : [];
  const visible = showAll ? mistakes : mistakes.slice(0, 3);
  const pillars = [
    ['grammar', lang === 'ru' ? 'Грамматика' : 'Grammatik'],
    ['vocabulary', lang === 'ru' ? 'Словарный запас' : 'Wortschatz'],
    ['listening', lang === 'ru' ? 'Аудирование' : 'Hörverstehen'],
    ['pronunciation', lang === 'ru' ? 'Произношение' : 'Aussprache'],
  ];
  const percent = (value: any) => Math.round(Number(value || 0) * (Number(value || 0) <= 10 ? 10 : 1));
  return (
    <main className="app-shell result-page page-enter">
      <header className="result-hero"><span className="result-icon"><FaCheck /></span><p className="eyebrow">{lang === 'ru' ? 'Твой результат' : 'Dein Ergebnis'}</p><h1>{data.level || 'A1'}</h1><strong>{Math.round(data.overall_score || 0)}%</strong><p>{lang === 'ru' ? 'Хорошая база. Теперь DeutschIQ построит план под твои ошибки.' : 'Eine gute Basis. DeutschIQ erstellt jetzt einen Plan für deine Fehler.'}</p></header>
      <section className="result-skills">{pillars.map(([key, label]) => { const assessed = data.skill_status?.[key] !== 'not_assessed'; return <div key={key}><span>{label}</span><b>{assessed ? `${percent(data.pillars?.[key])}%` : (lang === 'ru' ? 'Не проверено' : 'Nicht geprüft')}</b>{assessed && <div className="progress-bar"><div className="progress-bar-fill progress-fill" style={{ width: `${percent(data.pillars?.[key])}%` }} /></div>}</div>; })}</section>
      <section><div className="section-heading"><span>{lang === 'ru' ? `Ошибки диагностики · ${mistakes.length}` : `Fehler in der Diagnose · ${mistakes.length}`}</span></div><div className="result-mistakes">{visible.map((mistake: any, index: number) => <div key={index}><span>{index + 1}</span><p>{topicLabel(String(mistake.tag || mistake.weak_tag || mistake.topic || mistake.question || 'grammar'), lang)}</p></div>)}</div>{mistakes.length > 3 && <button className="secondary-action" onClick={() => setShowAll(v => !v)}>{showAll ? (lang === 'ru' ? 'Скрыть' : 'Weniger anzeigen') : (lang === 'ru' ? 'Показать все ошибки' : 'Alle Fehler anzeigen')} <FaChevronDown /></button>}</section>
      <section className="next-step"><p className="eyebrow">{lang === 'ru' ? 'Следующий шаг' : 'Nächster Schritt'}</p><h2>{lang === 'ru' ? 'Исправим три главные слабые темы' : 'Wir trainieren deine drei wichtigsten Lücken'}</h2><button className="primary-action" onClick={() => navigate(withUser('/plan'))}>{lang === 'ru' ? 'Открыть мой план' : 'Meinen Lernplan öffnen'} <FaArrowRight /></button></section>
    </main>
  );
};
