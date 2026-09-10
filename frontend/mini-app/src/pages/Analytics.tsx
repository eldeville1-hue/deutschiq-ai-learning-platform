import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaArrowRight, FaChartLine, FaChevronDown, FaExclamationCircle, FaMicrophone } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

type Skill = { key: string; score: number; hasData: boolean };

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
  const nextAction = missing.length
    ? (lang === 'ru' ? `Проверить навык: ${topicLabel(missing[0].key, lang)}` : `${topicLabel(missing[0].key, lang)} einschätzen`)
    : errors.length
      ? (lang === 'ru' ? `Потренировать: ${topicLabel(String(errors[0].name), lang)}` : `${topicLabel(String(errors[0].name), lang)} trainieren`)
      : (lang === 'ru' ? 'Продолжить персональный план' : 'Persönlichen Plan fortsetzen');

  if (loading && !data) return <main className="app-shell rc-page"><div className="skeleton rc-hero-skeleton" /></main>;

  return (
    <main className="app-shell rc-page rc-analytics page-enter">
      <header className="rc-page-title">
        <p>{lang === 'ru' ? 'АНАЛИЗ' : 'ANALYSE'}</p>
        <h1>{lang === 'ru' ? 'Картина знаний' : 'Dein Wissensprofil'}</h1>
        <span>{lang === 'ru' ? 'Только результаты реальных ответов' : 'Nur Ergebnisse aus echten Antworten'}</span>
      </header>

      {loadError && <div className="rc-notice error"><span>{lang === 'ru' ? 'Свежие данные пока недоступны' : 'Aktuelle Daten sind nicht verfügbar'}</span><button type="button" onClick={load}>{lang === 'ru' ? 'Обновить' : 'Aktualisieren'}</button></div>}

      <section className="rc-analysis-overview" aria-label={lang === 'ru' ? 'Общий прогресс' : 'Gesamtfortschritt'}>
        <div className="rc-level-block"><small>{lang === 'ru' ? 'ТЕКУЩИЙ УРОВЕНЬ' : 'AKTUELLES NIVEAU'}</small><strong>{data?.level || 'A1'}</strong><span>{lang === 'ru' ? `цель ${data?.targetLevel || 'A2'}` : `Ziel ${data?.targetLevel || 'A2'}`}</span></div>
        <div className="rc-score-ring" style={{ '--score': `${progress * 3.6}deg` } as React.CSSProperties}><span><strong>{progress}</strong>%</span></div>
        <div className="rc-journey"><span>{data?.level || 'A1'}</span><div><i style={{ width: `${progress}%` }} /></div><span>{data?.targetLevel || 'A2'}</span></div>
        <p>{lang === 'ru' ? 'Оценка меняется после проверенных заданий, а не после открытия урока.' : 'Die Bewertung ändert sich nach geprüften Aufgaben, nicht nach geöffneten Lektionen.'}</p>
      </section>

      <button type="button" className="rc-next-action" onClick={() => navigate(withUser('/plan'))}>
        <span><small>{lang === 'ru' ? 'ЛУЧШИЙ СЛЕДУЮЩИЙ ШАГ' : 'BESTER NÄCHSTER SCHRITT'}</small><strong>{nextAction}</strong></span>
        <FaArrowRight />
      </button>

      <section className="rc-skill-report">
        <header><div><small>{lang === 'ru' ? 'НАВЫКИ' : 'FÄHIGKEITEN'}</small><h2>{lang === 'ru' ? 'Что уже измерено' : 'Was bereits gemessen wurde'}</h2></div>{strongest && <span><FaChartLine /> {lang === 'ru' ? 'Сильнее' : 'Stärke'}: {topicLabel(strongest.key, lang)}</span>}</header>
        <div className="rc-skill-list">
          {stats.length ? stats.map(skill => <div className="rc-skill-row" key={skill.key}>
            <div><strong>{topicLabel(skill.key, lang)}</strong><small>{skill.hasData ? (lang === 'ru' ? 'По выполненным заданиям' : 'Aus erledigten Aufgaben') : (lang === 'ru' ? 'Недостаточно данных' : 'Noch nicht genug Daten')}</small></div>
            <b className={skill.hasData ? '' : 'muted'}>{skill.hasData ? `${skill.score}%` : '—'}</b>
            <div className="rc-meter"><i style={{ width: `${skill.hasData ? skill.score : 0}%` }} /></div>
          </div>) : <div className="rc-empty-inline"><FaExclamationCircle /><span>{lang === 'ru' ? 'Пройди первые задания, чтобы увидеть профиль навыков.' : 'Löse die ersten Aufgaben, um dein Profil zu sehen.'}</span></div>}
        </div>
      </section>

      <details className="rc-analysis-detail">
        <summary><span><small>{lang === 'ru' ? 'ПАМЯТЬ' : 'GEDÄCHTNIS'}</small><strong>{lang === 'ru' ? 'Удержание знаний' : 'Wissensspeicherung'}</strong></span><FaChevronDown /></summary>
        <div className="rc-detail-content">{learning?.mastery?.length ? learning.mastery.slice(0, 4).map((item: any) => <div className="rc-detail-row" key={item.topic}><span><strong>{topicLabel(item.topic, lang)}</strong><small>{item.attempts} {lang === 'ru' ? 'попыток' : 'Versuche'}</small></span><b>{item.mastery}%</b></div>) : <p>{lang === 'ru' ? 'Данные появятся после практики и повторений.' : 'Daten erscheinen nach Übungen und Wiederholungen.'}</p>}</div>
      </details>

      <details className="rc-analysis-detail">
        <summary><span><small><FaMicrophone /> {lang === 'ru' ? 'ГОЛОС' : 'SPRACHE'}</small><strong>{lang === 'ru' ? 'Говорение и аудирование' : 'Sprechen und Hören'}</strong></span><FaChevronDown /></summary>
        <div className="rc-detail-content">{(['speaking', 'listening'] as const).map(key => <div className="rc-detail-row" key={key}><span><strong>{topicLabel(key === 'speaking' ? 'pronunciation' : 'listening', lang)}</strong><small>{voice?.[key]?.attempts || 0} {lang === 'ru' ? 'попыток' : 'Versuche'}</small></span><b>{voice?.[key]?.score == null ? '—' : `${voice[key].score}%`}</b></div>)}<p>{lang === 'ru' ? 'Распознавание слов показывает понятность речи, но не оценивает акцент.' : 'Die Worterkennung zeigt Verständlichkeit, bewertet aber keinen Akzent.'}</p></div>
      </details>

      <section className="rc-mistakes">
        <header><div><small>{lang === 'ru' ? 'ФОКУС' : 'FOKUS'}</small><h2>{lang === 'ru' ? 'Ошибки для разбора' : 'Fehler zum Wiederholen'}</h2></div><span>{errors.length}</span></header>
        {errors.length ? errors.map((error: any) => { const count = Math.max(1, Math.round(Number(error.percent || 10) / 10)); return <div key={error.name}><span>{topicLabel(String(error.name), lang)}</span><b>{count} {errorWord(count, lang)}</b></div>; }) : <p>{lang === 'ru' ? 'Ошибок пока нет — продолжай практику.' : 'Noch keine Fehler – übe weiter.'}</p>}
        <button type="button" disabled={!errors.length} onClick={() => navigate(withUser('/mistakes'))}>{lang === 'ru' ? 'Открыть разбор ошибок' : 'Fehleranalyse öffnen'} <FaArrowRight /></button>
      </section>
    </main>
  );
};
