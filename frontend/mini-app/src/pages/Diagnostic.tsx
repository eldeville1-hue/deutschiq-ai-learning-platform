// frontend/mini-app/src/pages/Diagnostic.tsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { getText } from '../i18n/translations';
import { api } from '../services/api';
import { getUserId, withUser } from '../utils/user';

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
  }, []);

  useEffect(() => {
    if (userId === null) return;
    api.getQuestions(lang)
      .then(data => { setQuestions((Array.isArray(data) ? data : []).slice(0, 15)); setLoading(false); })
      .catch(() => setLoading(false));
  }, [userId, lang]);

  const submitTest = async (finalAnswers: Record<number, string>) => {
    if (!userId || submitting) return;
    setSubmitting(true);
    setSubmitError('');
    try {
      const result = await api.submitDiagnostic({ user_id: userId, answers: finalAnswers });
      sessionStorage.setItem(`deutschiq-result-${userId}`, JSON.stringify(result));
      navigate(withUser('/result'), { replace: true, state: { result } });
    } catch {
      setSubmitError(lang === 'de' ? 'Die Auswertung konnte nicht geladen werden. Bitte versuche es erneut.' : 'Не удалось отправить тест. Проверьте соединение и попробуйте ещё раз.');
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

  if (loading) return <main className="diagnostic-shell"><div className="skeleton diagnostic-skeleton" /></main>;

  if (questions.length === 0) {
    return (
      <main className="diagnostic-shell diagnostic-empty">
        <p>{t.diagnostic.noQuestions}</p>
        <button onClick={() => navigate('/')} className="btn-gold">{t.common.back}</button>
      </main>
    );
  }

  const q = questions[current];
  const progress = ((current + 1) / questions.length) * 100;

  return (
    <main className="diagnostic-shell diagnostic-page precision-diagnostic page-enter">
      <header className="diagnostic-header">
      <span className="diagnostic-index">{String(current + 1).padStart(2, '0')}</span>
      <div><h2>{t.diagnostic.title}</h2><p>
        {t.diagnostic.question.replace('{current}', String(current + 1)).replace('{total}', String(questions.length))}
      </p></div></header>
      <div className="progress-bar diagnostic-progress">
        <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
      </div>

      <section className="diagnostic-question" key={q.id}>
        <span className="difficulty-pill">{q.difficulty}</span>
        <h1>{q.text}</h1>
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
          <p>{lang === 'de' ? 'Deine Antworten werden ausgewertet…' : 'Анализируем ваши ответы…'}</p>
        </div>
      )}

      {submitError && <p className="diagnostic-error">{submitError}</p>}

      {current === questions.length - 1 && (
        <button onClick={() => submitTest(answers)} disabled={submitting} className="primary-action diagnostic-finish">
          {submitting ? (lang === 'de' ? 'Wird ausgewertet…' : 'Анализируем…') : t.diagnostic.finish}
        </button>
      )}
    </main>
  );
};
