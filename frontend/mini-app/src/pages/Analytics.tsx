import React, { useEffect, useState } from 'react';
import { FaArrowRight } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

const skillKey = (label: string) => ({ Grammatik: 'grammar', Aussprache: 'pronunciation', Wortschatz: 'vocabulary', Hörverstehen: 'listening' } as Record<string, string>)[label] || label;
const errorWord = (count: number, lang: 'ru' | 'de') => {
  if (lang === 'de') return 'Fehler';
  const mod10 = count % 10;
  const mod100 = count % 100;
  return mod10 === 1 && mod100 !== 11 ? 'ошибка' : mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14) ? 'ошибки' : 'ошибок';
};

export const Analytics: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [learning, setLearning] = useState<any>(null);
  const [voice, setVoice] = useState<any>(null);
  useEffect(() => { Promise.allSettled([api.getDashboard(getUserId()), api.getLearningToday(getUserId()), api.getSpeechProgress(getUserId())]).then(([dashboard, today, speech]) => { setData(dashboard.status === 'fulfilled' ? dashboard.value : { level:'A1', targetLevel:'B1', targetProgress:0, stats:[], weaknesses:[] }); if (today.status === 'fulfilled') setLearning(today.value); if (speech.status === 'fulfilled') setVoice(speech.value); }); }, []);
  if (!data) return <main className="app-shell"><div className="skeleton analysis-skeleton" /></main>;
  const progress = Math.max(0, Math.min(100, Math.round(data.targetProgress || 0)));
  const stats = (data.stats || []).map((item: any) => ({ key: skillKey(String(item.label)), score: Math.round(Number(item.value || 0) * (Number(item.value || 0) <= 10 ? 10 : 1)), hasData: item.has_data !== false }));
  const strongest = [...stats].filter((s: any) => s.hasData).sort((a: any, b: any) => b.score - a.score)[0];
  const missing = stats.filter((s: any) => !s.hasData);
  const errors = (data.weaknesses || []).slice(0, 3);
  return (
    <main className="app-shell analytics-page precision-analysis v30-page v30-analytics page-enter">
      <header className="analysis-title page-stagger-1"><p>{lang === 'ru' ? 'АНАЛИЗ' : 'ANALYSE'}</p><h1>{lang === 'ru' ? 'Твоя картина знаний' : 'Dein Wissensprofil'}</h1></header>
      <section className="knowledge-instrument page-stagger-2">
        <div className="instrument-level"><small>{lang === 'ru' ? 'ТЕКУЩИЙ УРОВЕНЬ' : 'AKTUELLES NIVEAU'}</small><strong>{data.level || 'A1'}</strong></div>
        <div className="instrument-progress"><strong>{progress}</strong><span>%</span><small>{lang === 'ru' ? 'оценка знаний' : 'Wissensstand'}</small></div>
        <div className="instrument-axis"><span>A1</span><div><i style={{ width: `${progress}%` }} /><b style={{ left: `${progress}%` }} /></div><span>{data.targetLevel || 'B1'}</span></div>
        <p>{lang === 'ru' ? `${100 - progress}% до цели ${data.targetLevel || 'B1'}` : `${100 - progress}% bis zum Ziel ${data.targetLevel || 'B1'}`}</p>
      </section>
      {strongest && <section className="strongest-skill page-stagger-3"><small>{lang === 'ru' ? 'СИЛЬНЕЕ ВСЕГО' : 'DEINE STÄRKE'}</small><div><h2>{topicLabel(strongest.key, lang)}</h2><b>{strongest.score}%</b></div><div className="analysis-bar"><i style={{ width: `${strongest.score}%` }} /></div></section>}
      {learning?.mastery?.length > 0 && <section className="mastery-section page-stagger-3"><header><h2>{lang === 'ru' ? 'Удержание знаний' : 'Wissensspeicherung'}</h2><small>{lang === 'ru' ? 'По реальным ответам, не по завершённым урокам' : 'Aus echten Antworten, nicht aus Abschlüssen'}</small></header>{learning.mastery.slice(0,4).map((item:any) => <div key={item.topic}><span>{topicLabel(item.topic, lang)}<small>{item.attempts} {lang === 'ru' ? 'попыток' : 'Versuche'}</small></span><b>{item.mastery}%</b><div className="analysis-bar"><i style={{width:`${item.mastery}%`}} /></div></div>)}</section>}
      <section className="voice-progress page-stagger-3"><header><small>{lang === 'ru' ? 'ГОЛОСОВАЯ ПРАКТИКА' : 'SPRACHTRAINING'}</small><h2>{lang === 'ru' ? 'Говорение и аудирование' : 'Sprechen und Hören'}</h2></header>{(['speaking', 'listening'] as const).map(key => <div key={key}><span>{topicLabel(key === 'speaking' ? 'pronunciation' : 'listening', lang)}<small>{voice?.[key]?.attempts || 0} {lang === 'ru' ? 'попыток' : 'Versuche'}</small></span><b>{voice?.[key]?.score == null ? '—' : `${voice[key].score}%`}</b><div className="analysis-bar"><i style={{width:`${voice?.[key]?.score || 0}%`}} /></div></div>)}<p>{lang === 'ru' ? 'Точность распознанных слов — не оценка акцента.' : 'Worterkennung ist keine Akzentbewertung.'}</p></section>
      <section className="attention-list page-stagger-3"><h2>{lang === 'ru' ? 'Требует внимания' : 'Noch nicht bewertet'}</h2>{missing.length ? missing.map((skill: any, index: number) => <div key={skill.key}><b>0{index + 1}</b><span><strong>{topicLabel(skill.key, lang)}</strong><small>{lang === 'ru' ? (skill.key === 'listening' ? 'Пройди 2 задания для оценки' : 'Пока нет данных') : (skill.key === 'listening' ? 'Löse 2 Aufgaben für eine Einschätzung' : 'Noch keine Daten')}</small></span></div>) : <p>{lang === 'ru' ? 'Все навыки уже получили первую оценку.' : 'Alle Fähigkeiten haben bereits eine erste Bewertung.'}</p>}</section>
      <section className="error-list page-stagger-4"><h2>{lang === 'ru' ? 'Твои ошибки' : 'Deine Fehler'}</h2>{errors.length ? errors.map((error: any) => { const count = Math.max(1, Math.round(Number(error.percent || 10) / 10)); return <div key={error.name}><span>{topicLabel(String(error.name), lang)}</span><b>{count} {errorWord(count, lang)}</b></div>; }) : <p>{lang === 'ru' ? 'Ошибок пока нет.' : 'Noch keine Fehler.'}</p>}<button onClick={() => navigate(withUser('/mistakes'))}>{lang === 'ru' ? 'Посмотреть разбор' : 'Fehler ansehen'} <FaArrowRight /></button></section>
    </main>
  );
};
