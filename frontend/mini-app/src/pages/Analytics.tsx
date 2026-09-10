import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaArrowRight, FaChartLine, FaChevronDown, FaLock, FaMicrophone } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { api } from '../services/api';
import { getUserId, withUser } from '../utils/user';

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
      api.getLearningToday(getUserId()),
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
  }, []);

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
    ? (lang === 'ru' ? `Сначала: ${topicLabel(missing[0].key, lang)}` : `Zuerst: ${topicLabel(missing[0].key, lang)}`)
    : errors.length
      ? (lang === 'ru' ? `Фокус: ${topicLabel(String(errors[0].name), lang)}` : `Fokus: ${topicLabel(String(errors[0].name), lang)}`)
      : (lang === 'ru' ? 'Следующий урок уже подобран' : 'Die nächste Lektion ist bereit');

  if (loading && !data) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className="app-shell rc-page rc-analytics page-enter">
      <header className="rc-page-title">
        <p>{lang === 'ru' ? 'АНАЛИЗ' : 'ANALYSE'}</p>
        <h1>{lang === 'ru' ? 'Прогресс' : 'Fortschritt'}</h1>
        <span>{lang === 'ru' ? 'По выполненным заданиям' : 'Aus deinen gelösten Aufgaben'}</span>
      </header>

      {loadError && <div className="rc-notice error"><span>{lang === 'ru' ? 'Свежие данные пока недоступны' : 'Aktuelle Daten sind nicht verfügbar'}</span><button type="button" onClick={load}>{lang === 'ru' ? 'Обновить' : 'Aktualisieren'}</button></div>}

      <section className="rc-analysis-overview" aria-label={lang === 'ru' ? 'Общий прогресс' : 'Gesamtfortschritt'}>
        <div className="rc-level-block"><small>{lang === 'ru' ? 'СЕЙЧАС' : 'JETZT'}</small><strong>{data?.level || 'A1'}</strong><span>{lang === 'ru' ? `цель ${data?.targetLevel || 'A2'}` : `Ziel ${data?.targetLevel || 'A2'}`}</span></div>
        <div className="rc-score-ring" style={{ '--score': `${progress * 3.6}deg` } as React.CSSProperties}><span><strong>{progress}</strong>%</span></div>
        <div className="rc-journey"><span>{data?.level || 'A1'}</span><div><i style={{ width: `${progress}%` }} /></div><span>{data?.targetLevel || 'A2'}</span></div>
        <p>{lang === 'ru' ? 'Оценка обновляется после заданий.' : 'Die Bewertung aktualisiert sich nach Aufgaben.'}</p>
      </section>

      <button type="button" className="rc-next-action" onClick={() => navigate(withUser('/plan'))}>
        <span><small>{lang === 'ru' ? 'СЛЕДУЮЩИЙ ШАГ' : 'NÄCHSTER SCHRITT'}</small><strong>{lang === 'ru' ? 'Продолжить план' : 'Plan fortsetzen'}</strong><em>{nextFocus}</em></span><FaArrowRight />
      </button>

      <section className="rc-skill-report">
        <header><div><small>{lang === 'ru' ? 'НАВЫКИ' : 'FÄHIGKEITEN'}</small><h2>{lang === 'ru' ? 'Профиль навыков' : 'Fähigkeitsprofil'}</h2></div>{strongest && <span><FaChartLine /> {topicLabel(strongest.key, lang)}</span>}</header>
        <div className="rc-skill-visual"><div className="rc-skill-grid">{radarStats.map(skill => <div className={`rc-skill-tile${skill.hasData ? '' : ' locked'}`} key={skill.key}><span>{topicLabel(skill.key, lang)}</span><b>{skill.hasData ? `${skill.score}%` : <><FaLock aria-hidden="true" /> {lang === 'ru' ? 'Нет данных' : 'Keine Daten'}</>}</b><div className="rc-meter"><i style={{ width: `${skill.hasData ? skill.score : 0}%` }} /></div></div>)}</div></div>
      </section>

      <div className="rc-insight-grid">
        <details className="rc-analysis-detail"><summary><span><small>{lang === 'ru' ? 'ПАМЯТЬ' : 'GEDÄCHTNIS'}</small><strong>{lang === 'ru' ? 'Удержание знаний' : 'Wissensspeicherung'}</strong></span><FaChevronDown /></summary><div className="rc-detail-content">{learning?.mastery?.length ? learning.mastery.slice(0, 4).map((item: any) => <div className="rc-detail-row" key={item.topic}><span><strong>{topicLabel(item.topic, lang)}</strong><small>{item.attempts} {lang === 'ru' ? 'попыток' : 'Versuche'}</small></span><b>{item.mastery}%</b></div>) : <p>{lang === 'ru' ? 'Появится после практики и повторений.' : 'Erscheint nach Übungen und Wiederholungen.'}</p>}</div></details>
        <details className="rc-analysis-detail"><summary><span><small><FaMicrophone /> {lang === 'ru' ? 'ГОЛОС' : 'SPRACHE'}</small><strong>{lang === 'ru' ? 'Говорение и слух' : 'Sprechen und Hören'}</strong></span><FaChevronDown /></summary><div className="rc-detail-content">{(['speaking', 'listening'] as const).map(key => <div className="rc-detail-row" key={key}><span><strong>{topicLabel(key === 'speaking' ? 'pronunciation' : 'listening', lang)}</strong><small>{voice?.[key]?.attempts || 0} {lang === 'ru' ? 'попыток' : 'Versuche'}</small></span><b>{voice?.[key]?.score == null ? '—' : `${voice[key].score}%`}</b></div>)}<p>{lang === 'ru' ? 'Распознавание оценивает понятность, а не акцент.' : 'Die Erkennung bewertet Verständlichkeit, nicht den Akzent.'}</p></div></details>
      </div>
    </main>
  );
};
