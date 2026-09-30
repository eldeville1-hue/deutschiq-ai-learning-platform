import React, { useEffect, useRef, useState } from 'react';
import { FaArrowRight, FaCheck, FaTimes } from 'react-icons/fa';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { tr } from '../i18n/language';
import { ExerciseInteraction } from '../components/learning/ExerciseInteraction';
import { getUserId, withUser } from '../utils/user';

export const Checkpoint: React.FC = () => {
  const { level = 'A1' } = useParams();
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const draftKey = `deutschiq-checkpoint-draft-${getUserId()}-${level}`;
  const initialDraft = useRef<any>(null);
  if (initialDraft.current === null) {
    try { initialDraft.current = JSON.parse(localStorage.getItem(draftKey) || 'false') || {}; } catch { initialDraft.current = {}; }
  }
  const restored = useRef(Boolean(initialDraft.current.savedAt));
  const [data, setData] = useState<any>(null);
  const [index, setIndex] = useState(() => Number(initialDraft.current.index || 0));
  const [answers, setAnswers] = useState<string[]>(() => initialDraft.current.answers || []);
  const [answer, setAnswer] = useState(() => String(initialDraft.current.answer || ''));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.getCheckpoint(getUserId(), level, lang).then(value => {
      setData(value);
      if (restored.current) {
        void api.trackEvent({ user_id: getUserId(), event_name: 'checkpoint_draft_restored', properties: { level, question: Number(initialDraft.current.index || 0) + 1 } });
        restored.current = false;
      }
    }).catch(() => setError(tr(lang, 'Тест пока недоступен. Сначала заверши маршрут.', 'Der Test ist noch nicht verfügbar. Schließe zuerst deinen Lernweg ab.', 'The checkpoint is not available yet. Complete your learning path first.')));
  }, [lang, level]);

  useEffect(() => {
    if (!data || result) return;
    try { localStorage.setItem(draftKey, JSON.stringify({ index, answers, answer, savedAt: Date.now() })); } catch { /* Recovery is best-effort. */ }
  }, [answer, answers, data, draftKey, index, result]);

  const item = data?.items?.[index];
  const next = async () => {
    const updated = [...answers];
    updated[index] = answer;
    setAnswers(updated);
    setAnswer('');
    if (index + 1 < (data?.items?.length || 0)) { setIndex(index + 1); return; }
    setSubmitting(true);
    try {
      const value = await api.submitCheckpoint({ user_id: getUserId(), level, answers: updated, language: lang });
      setResult(value);
      try { localStorage.removeItem(draftKey); } catch { /* Ignore unavailable storage. */ }
    } catch {
      setError(tr(lang, 'Не удалось сохранить результат. Ответы остались на устройстве — попробуй ещё раз.', 'Das Ergebnis konnte nicht gespeichert werden. Deine Antworten bleiben auf dem Gerät – versuche es erneut.', 'Could not save the result. Your answers remain on this device—try again.'));
    } finally { setSubmitting(false); }
  };

  if (error) return <main className="app-shell checkpoint-page"><div className="rc-notice error">{error}</div><button className="rc-primary" onClick={() => navigate(withUser('/plan'))}>{tr(lang, 'Вернуться к плану', 'Zurück zum Plan', 'Back to plan')}</button></main>;
  if (!data) return <main className="app-shell checkpoint-page"><div className="skeleton rc-hero-skeleton" /></main>;
  if (result) {
    const dimensionLabels: Record<string, string> = {
      task_completion: tr(lang, 'Задача', 'Aufgabe', 'Task'), grammar: tr(lang, 'Грамматика', 'Grammatik', 'Grammar'),
      vocabulary: tr(lang, 'Слова', 'Wortschatz', 'Vocabulary'), coherence: tr(lang, 'Связность', 'Zusammenhang', 'Coherence'),
      register: tr(lang, 'Уместность', 'Register', 'Register'),
    };
    return <main className={`app-shell checkpoint-page checkpoint-result ${result.passed ? 'graduated' : 'repair-needed'}`}>
      <div className="checkpoint-celebration" aria-hidden="true"><i /><i /><i /></div>
      <span className={`result-icon ${result.passed ? '' : 'needs-practice'}`}>{result.passed ? <FaCheck /> : <FaTimes />}</span>
      <p className="eyebrow">{result.passed ? tr(lang, `${level} ЗАВЕРШЁН`, `${level} ABGESCHLOSSEN`, `${level} COMPLETE`) : tr(lang, 'ТОЧЕЧНОЕ ВОССТАНОВЛЕНИЕ', 'GEZIELTE WIEDERHOLUNG', 'FOCUSED REPAIR')}</p>
      <h1>{result.passed ? tr(lang, 'Ты справился самостоятельно', 'Du hast es selbstständig geschafft', 'You handled it independently') : tr(lang, 'Почти готово', 'Fast geschafft', 'Almost there')}</h1>
      <p className="checkpoint-result-copy">{result.passed
        ? tr(lang, 'Ты выполнил реальные коммуникативные задачи без модели ответа.', 'Du hast echte Kommunikationsaufgaben ohne Antwortmodell gelöst.', 'You completed real communication tasks without an answer model.')
        : tr(lang, 'Не нужно повторять весь уровень. Сначала укрепим только слабые места.', 'Du musst nicht das ganze Niveau wiederholen. Wir stärken nur die schwachen Stellen.', 'You do not need to repeat the whole level. We will strengthen only the weak areas.')}</p>
      <div className="checkpoint-score"><strong>{result.score}%</strong><span>{tr(lang, 'по независимым миссиям', 'aus unabhängigen Missionen', 'from independent missions')}</span></div>
      <div className="checkpoint-dimensions">{Object.entries(result.dimensions || {}).map(([key, value]) => <span key={key}><small>{dimensionLabels[key] || key}</small><b>{Number(value)}%</b><i><em style={{ width: `${Number(value)}%` }} /></i></span>)}</div>
      {!result.passed && result.recovery_topics?.length > 0 && <div className="checkpoint-recovery"><small>{tr(lang, 'СНАЧАЛА УЛУЧШИМ', 'ZUERST VERBESSERN WIR', 'FIRST WE WILL IMPROVE')}</small>{result.recovery_topics.map((topic: string) => <span key={topic}>{topic}</span>)}</div>}
      {result.unlocked_level && <div className="level-unlocked"><small>{tr(lang, 'ТВОЙ НОВЫЙ МАРШРУТ', 'DEIN NEUER LERNWEG', 'YOUR NEW PATH')}</small><strong>{result.completed_level} <i>✓</i> · 0% → {result.unlocked_level}</strong><span>{tr(lang, 'Следующая миссия уже готова.', 'Die nächste Mission ist schon bereit.', 'Your next mission is ready.')}</span></div>}
      <button className="rc-primary" onClick={() => navigate(withUser(result.passed ? '/plan' : result.recovery_lesson_id ? `/lesson/${result.recovery_lesson_id}` : '/review'))}>{result.passed ? tr(lang, `Начать ${result.unlocked_level}`, `${result.unlocked_level} starten`, `Start ${result.unlocked_level}`) : tr(lang, 'Исправить слабую миссию', 'Schwache Mission verbessern', 'Repair weakest mission')} <FaArrowRight /></button>
    </main>;
  }
  return <main className="app-shell checkpoint-page"><header><p className="eyebrow">{level} · {tr(lang, 'ВЫПУСКНАЯ МИССИЯ', 'ABSCHLUSSMISSION', 'GRADUATION MISSION')}</p><h1>{index + 1}/{data.items.length}</h1><p className="checkpoint-intro">{tr(lang, 'Без подсказок. Ответь своими словами — личные детали могут отличаться.', 'Ohne Hinweise. Antworte mit deinen eigenen Worten – persönliche Angaben dürfen anders sein.', 'No hints. Answer in your own words—personal details may differ.')}</p><div className="progress-bar"><div className="progress-bar-fill" style={{ width: `${((index + 1) / data.items.length) * 100}%` }} /></div></header><section className="checkpoint-card"><small className="checkpoint-mission-label">{tr(lang, 'РЕАЛЬНАЯ СИТУАЦИЯ', 'ECHTE SITUATION', 'REAL SITUATION')}</small><h2>{item?.question}</h2>{item && <ExerciseInteraction exercise={{ ...item, id: `checkpoint-${level}-${index}` }} answer={answer} onAnswer={setAnswer} lang={lang} />}<button className="rc-primary" disabled={!answer.trim() || submitting} onClick={next}>{submitting ? tr(lang, 'Оцениваем…', 'Wird bewertet…', 'Evaluating…') : index + 1 === data.items.length ? tr(lang, 'Завершить уровень', 'Niveau abschließen', 'Complete level') : tr(lang, 'Следующая ситуация', 'Nächste Situation', 'Next situation')} {!submitting && <FaArrowRight />}</button></section></main>;
};
