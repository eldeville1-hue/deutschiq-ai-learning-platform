// frontend/mini-app/src/pages/Diagnostic.tsx
import React, { useState, useEffect } from 'react';
import { FaBrain, FaComments, FaHeadphones, FaLanguage, FaVolumeUp } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { getText } from '../i18n/translations';
import { api } from '../services/api';
import { getUserId, withUser } from '../utils/user';
import './Diagnostic.css';
import { tr } from '../i18n/language';

export const Diagnostic: React.FC = () => {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const t = getText(lang);
  const [questions, setQuestions] = useState<any[]>([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState<number | null>(null);
  const [answerLocked, setAnswerLocked] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [questionError, setQuestionError] = useState(false);
  const [questionRetry, setQuestionRetry] = useState(0);
  const [pendingRecovery, setPendingRecovery] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const resolvedId = getUserId();
    const isRetake = params.get('retake') === 'true';
    api.getUserState(resolvedId).then(state => {
      if (state?.diagnostic_completed && !isRetake) {
        navigate(withUser('/dashboard'), { replace: true });
        return;
      }
      setUserId(resolvedId);
    }).catch(() => setUserId(resolvedId));
  }, [navigate]);

  useEffect(() => {
    if (userId === null) return;
    void api.trackEvent({ user_id: userId, event_name: 'diagnostic_started', properties: { language: lang } });
    setLoading(true);
    setQuestionError(false);
    setCurrent(0);
    setAnswers({});
    setAnswerLocked(false);
    api.getQuestions(lang)
      .then(data => {
        const loaded = Array.isArray(data) ? data : [];
        setQuestions(loaded);
        try {
          const pending = JSON.parse(localStorage.getItem(`deutschiq-pending-diagnostic-${userId}`) || 'null');
          if (pending?.answers && Object.keys(pending.answers).length === loaded.length) {
            setAnswers(pending.answers);
            setCurrent(Math.max(0, loaded.length - 1));
            setAnswerLocked(true);
            setPendingRecovery(true);
            setSubmitError(tr(lang, 'Результат ещё не сохранён. Ответы восстановлены.', 'Das Ergebnis ist noch nicht gespeichert. Deine Antworten wurden wiederhergestellt.', 'The result is not saved yet. Your answers were restored.'));
          }
        } catch { /* A damaged recovery draft should not block a fresh test. */ }
        setLoading(false);
      })
      .catch(() => { setQuestions([]); setQuestionError(true); setLoading(false); });
  }, [userId, lang, questionRetry]);

  const submitTest = async (finalAnswers: Record<number, string>) => {
    if (!userId || submitting) return;
    setSubmitting(true);
    setSubmitError('');
    try { localStorage.setItem(`deutschiq-pending-diagnostic-${userId}`, JSON.stringify({ answers: finalAnswers, savedAt: Date.now() })); } catch { /* Retry still works in memory. */ }
    try {
      const result = await api.submitDiagnostic({ user_id: userId, answers: finalAnswers, language: lang });
      if (!result?.persisted) {
        setPendingRecovery(true);
        setSubmitError(tr(lang, 'Результат рассчитан, но не сохранён.', 'Das Ergebnis wurde berechnet, aber nicht gespeichert.', 'The result was calculated but not saved.'));
        setSubmitting(false);
        setAnswerLocked(true);
        return;
      }
      try { localStorage.removeItem(`deutschiq-pending-diagnostic-${userId}`); } catch { /* Ignore unavailable storage. */ }
      setPendingRecovery(false);
      sessionStorage.setItem(`deutschiq-result-${userId}`, JSON.stringify(result));
      navigate(withUser('/result'), { replace: true, state: { result } });
    } catch {
      setPendingRecovery(true);
      setSubmitError(tr(lang, 'Не удалось отправить тест. Проверь соединение и попробуй ещё раз.', 'Die Auswertung konnte nicht geladen werden. Bitte versuche es erneut.', 'Could not submit the test. Check your connection and try again.'));
      setSubmitting(false);
      setAnswerLocked(false);
    }
  };

  const handleSelect = (option: string) => {
    if (answerLocked) return;
    const q = questions[current];
    setAnswerLocked(true);
    const nextAnswers = { ...answers, [q.id]: option };
    setAnswers(nextAnswers);
    if (current < questions.length - 1) {
      setTimeout(() => {
        setCurrent(prev => prev + 1);
        setAnswerLocked(false);
      }, 360);
    } else {
      window.setTimeout(() => submitTest(nextAnswers), 360);
    }
  };

  const playListeningPrompt = () => {
    const text = questions[current]?.audio_text;
    if (!text || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'de-DE';
    utterance.rate = .82;
    window.speechSynthesis.speak(utterance);
  };

  if (loading) return <main className="diagnostic-shell"><div className="skeleton diagnostic-skeleton" /></main>;

  if (questions.length === 0) {
    return (
      <main className="diagnostic-shell diagnostic-empty">
        <p>{questionError ? tr(lang, 'Не удалось загрузить вопросы.', 'Fragen konnten nicht geladen werden.', 'Could not load the questions.') : t.diagnostic.noQuestions}</p>
        {questionError
          ? <button type="button" onClick={() => setQuestionRetry(value => value + 1)} className="btn-gold">{tr(lang, 'Повторить', 'Erneut versuchen', 'Try again')}</button>
          : <button type="button" onClick={() => navigate('/')} className="btn-gold">{t.common.back}</button>}
      </main>
    );
  }

  const q = questions[current];
  const progress = ((current + 1) / questions.length) * 100;
  const pillar = ({
    grammar: { icon: <FaLanguage />, label: tr(lang, 'Грамматика', 'Grammatik', 'Grammar') },
    vocabulary: { icon: <FaBrain />, label: tr(lang, 'Словарь', 'Wortschatz', 'Vocabulary') },
    listening: { icon: <FaHeadphones />, label: tr(lang, 'Аудирование', 'Hörverstehen', 'Listening') },
    speaking: { icon: <FaComments />, label: tr(lang, 'Использование языка', 'Sprachgebrauch', 'Language use') },
  } as Record<string, { icon: React.ReactNode; label: string }>)[q.pillar] || { icon: <FaBrain />, label: tr(lang, 'Немецкий язык', 'Deutsch', 'German') };

  return (
    <main className="diagnostic-shell diagnostic-page precision-diagnostic page-enter">
      <header className="diagnostic-header">
      <span className="diagnostic-index">{String(current + 1).padStart(2, '0')}</span>
      <div><small>{tr(lang, 'АДАПТИВНАЯ ДИАГНОСТИКА', 'ADAPTIVE EINSTUFUNG', 'ADAPTIVE PLACEMENT')}</small><h2>{t.diagnostic.title}</h2><p>
        {t.diagnostic.question.replace('{current}', String(current + 1)).replace('{total}', String(questions.length))}
      </p></div></header>
      <div className="progress-bar diagnostic-progress">
        <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
      </div>

      <section className="diagnostic-question" key={q.id}>
        <div className="diagnostic-skill"><span>{pillar.icon}{pillar.label}</span><small>{tr(lang, 'Сложность меняется по твоим ответам', 'Die Schwierigkeit passt sich deinen Antworten an', 'Difficulty adapts to your answers')}</small></div>
        <h1>{q.text}</h1>
        {q.pillar === 'listening' && <button type="button" className="diagnostic-listen" onClick={playListeningPrompt}><FaVolumeUp />{tr(lang, 'Прослушать ещё раз', 'Noch einmal anhören', 'Listen again')}</button>}
        <div className="diagnostic-options">
          {q.options.map((opt: string, index: number) => (
            <button
              key={opt}
              onClick={() => handleSelect(opt)}
              disabled={answerLocked || submitting}
              className={answers[q.id] === opt ? 'selected' : ''}
            >
              <span>{String.fromCharCode(65 + index)}</span><b>{opt}</b>
            </button>
          ))}
        </div>
      </section>

      {submitting && (
        <div className="diagnostic-evaluating">
          <div className="analysis-loader" aria-hidden="true" />
          <p>{tr(lang, 'Анализируем твои ответы…', 'Deine Antworten werden ausgewertet…', 'Analysing your answers…')}</p>
        </div>
      )}

      {submitError && <p className="diagnostic-error">{submitError}</p>}
      {submitError && pendingRecovery && <button type="button" className="primary-action diagnostic-save-retry" disabled={submitting} onClick={() => submitTest(answers)}>{submitting ? tr(lang, 'Сохраняем…', 'Wird gespeichert…', 'Saving…') : tr(lang, 'Повторить сохранение', 'Speichern erneut versuchen', 'Retry saving')}</button>}

    </main>
  );
};
