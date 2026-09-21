import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaArrowRight, FaChartLine, FaChevronDown, FaLock, FaMicrophone } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { api } from '../services/api';
import { getUserId, withUser } from '../utils/user';
import { tr } from '../i18n/language';

type Skill = { key: string; score: number; hasData: boolean };

const skillKey = (label: string) => ({ Grammatik: 'grammar', Aussprache: 'pronunciation', Wortschatz: 'vocabulary', Hörverstehen: 'listening' } as Record<string, string>)[label] || label;
export const Analytics: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [learning, setLearning] = useState<any>(null);
  const [voice, setVoice] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    const [dashboard, today, speech] = await Promise.allSettled([
      api.getDashboard(getUserId()),
      api.getLearningToday(getUserId(), lang),
      api.getSpeechProgress(getUserId()),
    ]);
    if (dashboard.status === 'fulfilled') {
      setData(dashboard.value);
      setLoadError(false);
    } else {
      setData({ level: 'A1', targetLevel: 'A2', targetProgress: 0, stats: [], weaknesses: [] });
      setLoadError(true);
    }
    setLearning(today.status === 'fulfilled' ? today.value : null);
    setVoice(speech.status === 'fulfilled' ? speech.value : null);
    setLoading(false);
  }, [lang]);

  useEffect(() => { void load(); }, [load]);

  const progress = Math.max(0, Math.min(100, Math.round(data?.targetProgress || 0)));
  const stats: Skill[] = useMemo(() => (data?.stats || []).map((item: any) => ({
    key: skillKey(String(item.label)),
    score: Math.max(0, Math.min(100, Math.round(Number(item.value || 0) * (Number(item.value || 0) <= 10 ? 10 : 1)))),
    hasData: item.has_data !== false,
  })), [data]);
  const strongest = [...stats].filter(skill => skill.hasData).sort((a, b) => b.score - a.score)[0];
  const missing = stats.filter(skill => !skill.hasData);
  const errors = (data?.weaknesses || []).slice(0, 3);
  const radarStats = stats.slice(0, 4);
  const nextFocus = missing.length
    ? tr(lang, `Сначала: ${topicLabel(missing[0].key, lang)}`, `Zuerst: ${topicLabel(missing[0].key, lang)}`, `Start with: ${topicLabel(missing[0].key, lang)}`)
    : errors.length
      ? tr(lang, `Фокус: ${topicLabel(String(errors[0].name), lang)}`, `Fokus: ${topicLabel(String(errors[0].name), lang)}`, `Focus: ${topicLabel(String(errors[0].name), lang)}`)
      : tr(lang, 'Следующий урок уже подобран', 'Die nächste Lektion ist bereit', 'Your next lesson is ready');

  if (loading && !data) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className="app-shell rc-page rc-analytics page-enter">
      <header className="rc-page-title">
        <p>{tr(lang, 'АНАЛИЗ', 'ANALYSE', 'ANALYSIS')}</p>
        <h1>{tr(lang, 'Прогресс', 'Fortschritt', 'Progress')}</h1>
        <span>{tr(lang, 'По выполненным заданиям', 'Aus deinen gelösten Aufgaben', 'Based on completed exercises')}</span>
      </header>

      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Свежие данные пока недоступны', 'Aktuelle Daten sind nicht verfügbar', 'Current data is unavailable')}</span><button type="button" onClick={load}>{tr(lang, 'Обновить', 'Aktualisieren', 'Refresh')}</button></div>}

      <section className="rc-analysis-overview" aria-label={tr(lang, 'Общий прогресс', 'Gesamtfortschritt', 'Overall progress')}>
        <div className="rc-level-block"><small>{tr(lang, 'СЕЙЧАС', 'JETZT', 'CURRENT')}</small><strong>{data?.level || 'A1'}</strong><span>{tr(lang, `цель ${data?.targetLevel || 'A2'}`, `Ziel ${data?.targetLevel || 'A2'}`, `goal ${data?.targetLevel || 'A2'}`)}</span></div>
        <div className="rc-score-ring" style={{ '--score': `${progress * 3.6}deg` } as React.CSSProperties}><span><strong>{progress}</strong>%</span></div>
        <div className="rc-journey"><span>{data?.level || 'A1'}</span><div><i style={{ width: `${progress}%` }} /></div><span>{data?.targetLevel || 'A2'}</span></div>
        <p>{tr(lang, 'Оценка обновляется после заданий.', 'Die Bewertung aktualisiert sich nach Aufgaben.', 'Your score updates after completed exercises.')}</p>
      </section>

      <button type="button" className="rc-next-action" onClick={() => navigate(withUser('/plan'))}>
        <span><small>{tr(lang, 'СЛЕДУЮЩИЙ ШАГ', 'NÄCHSTER SCHRITT', 'NEXT STEP')}</small><strong>{tr(lang, 'Продолжить план', 'Plan fortsetzen', 'Continue plan')}</strong><em>{nextFocus}</em></span><FaArrowRight />
      </button>

      <section className="rc-skill-report">
        <header><div><small>{tr(lang, 'НАВЫКИ', 'FÄHIGKEITEN', 'SKILLS')}</small><h2>{tr(lang, 'Профиль навыков', 'Fähigkeitsprofil', 'Skill profile')}</h2></div>{strongest && <span><FaChartLine /> {topicLabel(strongest.key, lang)}</span>}</header>
        <div className="rc-skill-visual"><div className="rc-skill-grid">{radarStats.map(skill => <div className={`rc-skill-tile${skill.hasData ? '' : ' locked'}`} key={skill.key}><span>{topicLabel(skill.key, lang)}</span><b>{skill.hasData ? `${skill.score}%` : <><FaLock aria-hidden="true" /> {tr(lang, 'Нет данных', 'Keine Daten', 'No data')}</>}</b><div className="rc-meter"><i style={{ width: `${skill.hasData ? skill.score : 0}%` }} /></div></div>)}</div></div>
      </section>

      <div className="rc-insight-grid">
        <details className="rc-analysis-detail"><summary><span><small>{tr(lang, 'ПАМЯТЬ', 'GEDÄCHTNIS', 'MEMORY')}</small><strong>{tr(lang, 'Удержание знаний', 'Wissensspeicherung', 'Knowledge retention')}</strong></span><FaChevronDown /></summary><div className="rc-detail-content">{learning?.retention_summary?.learned > 0 && <p>{tr(lang, `Удерживается ${learning.retention_summary.retained} из ${learning.retention_summary.learned} навыков · под риском ${learning.retention_summary.at_risk}`, `${learning.retention_summary.retained} von ${learning.retention_summary.learned} Fähigkeiten behalten · ${learning.retention_summary.at_risk} gefährdet`, `${learning.retention_summary.retained} of ${learning.retention_summary.learned} skills retained · ${learning.retention_summary.at_risk} at risk`)}</p>}{learning?.mastery?.length ? learning.mastery.slice(0, 4).map((item: any) => <div className="rc-detail-row" key={item.topic}><span><strong>{topicLabel(item.topic, lang)}</strong><small>{item.attempts} {tr(lang, 'попыток', 'Versuche', 'attempts')}</small></span><b>{item.retention}%</b></div>) : <p>{tr(lang, 'Появится после практики и повторений.', 'Erscheint nach Übungen und Wiederholungen.', 'Appears after practice and review.')}</p>}</div></details>
        <details className="rc-analysis-detail"><summary><span><small><FaMicrophone /> {tr(lang, 'ГОЛОС', 'SPRACHE', 'VOICE')}</small><strong>{tr(lang, 'Говорение и слух', 'Sprechen und Hören', 'Speaking and listening')}</strong></span><FaChevronDown /></summary><div className="rc-detail-content">{(['speaking', 'listening'] as const).map(key => <div className="rc-detail-row" key={key}><span><strong>{topicLabel(key === 'speaking' ? 'pronunciation' : 'listening', lang)}</strong><small>{voice?.[key]?.attempts || 0} {tr(lang, 'попыток', 'Versuche', 'attempts')}</small></span><b>{voice?.[key]?.score == null ? '—' : `${voice[key].score}%`}</b></div>)}<p>{tr(lang, 'Распознавание оценивает понятность, а не акцент.', 'Die Erkennung bewertet Verständlichkeit, nicht den Akzent.', 'Recognition measures intelligibility, not your accent.')}</p></div></details>
      </div>
    </main>
  );
};
