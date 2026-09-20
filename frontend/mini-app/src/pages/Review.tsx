import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaRedo, FaTimes } from 'react-icons/fa';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { tr } from '../i18n/language';

export const Review: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [items, setItems] = useState<any[] | null>(null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState<any>(null);
  const [startedAt, setStartedAt] = useState(Date.now());
  const [sessionId, setSessionId] = useState('');
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => { void api.trackEvent({ user_id: getUserId(), event_name: 'review_started' }); api.getReviews(getUserId(), lang).then(data => setItems(data.reviews || [])).catch(() => { setItems([]); setError(tr(lang, 'Не удалось загрузить повторения.', 'Wiederholungen konnten nicht geladen werden.', 'Could not load reviews.')); }); }, [lang]);

  const nextLesson = Number(searchParams.get('nextLesson') || 0);
  const leave = () => navigate(withUser('/dashboard'));
  const continueSession = () => navigate(withUser(nextLesson ? `/lesson/${nextLesson}` : '/dashboard'));
  if (items === null) return <main className="lesson-flow rc-review"><div className="skeleton rc-hero-skeleton" /></main>;
  if (!items.length) return <main className="lesson-flow rc-review rc-review-state"><span className="rc-state-icon"><FaCheck /></span><p>{tr(lang, 'ПОВТОРЕНИЕ', 'WIEDERHOLUNG', 'REVIEW')}</p><h1>{error ? tr(lang, 'Не удалось загрузить', 'Laden fehlgeschlagen', 'Could not load') : tr(lang, 'На сегодня всё', 'Für heute erledigt', 'All done for today')}</h1><span>{error || tr(lang, 'Новые карточки появятся после урока.', 'Neue Karten erscheinen nach der Lektion.', 'New cards appear after a lesson.')}</span><button type="button" className="rc-primary" onClick={error ? leave : continueSession}>{nextLesson && !error ? tr(lang, 'Перейти к новому навыку', 'Zum neuen Lernziel', 'Continue to new skill') : tr(lang, 'На главную', 'Zur Übersicht', 'Back to overview')}</button></main>;
  if (index >= items.length) return <main className="lesson-flow rc-review rc-review-state"><span className="rc-state-icon success"><FaCheck /></span><p>{tr(lang, 'ГОТОВО', 'FERTIG', 'DONE')}</p><h1>{tr(lang, 'Память укреплена', 'Erinnerung gefestigt', 'Memory strengthened')}</h1><span>{tr(lang, `${items.length} тем повторено.`, `${items.length} Themen wiederholt.`, `${items.length} topics reviewed.`)}</span><button type="button" className="rc-primary" onClick={() => { void api.trackEvent({ user_id: getUserId(), event_name: 'review_completed', properties: { count: items.length } }); continueSession(); }}>{nextLesson ? tr(lang, 'Новый навык', 'Neues Lernziel', 'New skill') : tr(lang, 'Продолжить', 'Weiter', 'Continue')} <FaArrowRight /></button></main>;

  const item = items[index];
  const ensureSession = async () => {
    if (sessionId) return sessionId;
    const session = await api.startLesson({ user_id: getUserId(), lesson_id: item.lesson_id });
    setSessionId(session.session_id);
    return session.session_id;
  };
  const check = async () => {
    if (!answer.trim() || checking) return;
    setChecking(true);
    setError('');
    try {
      const activeSession = await ensureSession();
      const result = await api.checkLessonAnswer({ user_id: getUserId(), lesson_id: item.lesson_id, exercise_index: item.exercise_index, answer, session_id: activeSession, language: lang, confidence: 'okay', response_ms: Date.now() - startedAt });
      setFeedback(result);
    } catch {
      setError(tr(lang, 'Ответ не отправился. Проверь соединение и повтори.', 'Die Antwort wurde nicht gesendet. Prüfe die Verbindung und versuche es erneut.', 'Your answer was not sent. Check the connection and try again.'));
    } finally { setChecking(false); }
  };
  const next = () => { setIndex(value => value + 1); setAnswer(''); setFeedback(null); setSessionId(''); setError(''); setStartedAt(Date.now()); };
  const progress = ((index + (feedback ? 1 : 0)) / items.length) * 100;

  return (
    <main className="lesson-flow rc-review page-enter">
      <header className="rc-review-top"><button type="button" onClick={leave} aria-label={tr(lang, 'Закрыть повторение', 'Wiederholung schließen', 'Close review')}><FaTimes /></button><div><span>{tr(lang, 'ПОВТОРЕНИЕ', 'WIEDERHOLUNG', 'REVIEW')}</span><small>{index + 1} / {items.length}</small></div></header>
      <div className="rc-review-progress"><i style={{ width: `${progress}%` }} /></div>

      <section className="rc-review-question">
        <div className="rc-retrieval-label"><FaRedo /><span>{tr(lang, 'Вспомни', 'Erinnere dich', 'Recall')}</span></div>
        <p>{topicLabel(item.topic, lang)}</p>
        <h1>{item.question}</h1>

        {!feedback && (item.type === 'choose' && item.options?.length
          ? <div className="rc-review-options">{item.options.map((option: string) => <button type="button" key={option} className={answer === option ? 'selected' : ''} onClick={() => setAnswer(option)}><span>{option}</span>{answer === option && <FaCheck />}</button>)}</div>
          : <label className="rc-review-input"><span>{tr(lang, 'Твой ответ', 'Deine Antwort', 'Your answer')}</span><input value={answer} onChange={event => setAnswer(event.target.value)} onKeyDown={event => { if (event.key === 'Enter') void check(); }} placeholder={tr(lang, 'Напиши по памяти…', 'Aus dem Gedächtnis…', 'Type from memory…')} /></label>)}

        {error && <div className="rc-notice error"><span>{error}</span></div>}

        {!feedback
          ? <button type="button" className="rc-primary" disabled={!answer.trim() || checking} onClick={check}>{checking ? tr(lang, 'Проверяем…', 'Wird geprüft…', 'Checking…') : tr(lang, 'Проверить', 'Prüfen', 'Check')}</button>
          : <div className={`rc-review-feedback ${feedback.correct ? 'correct' : 'wrong'}`}><header><span>{feedback.correct ? <FaCheck /> : <FaRedo />}</span><strong>{feedback.correct ? tr(lang, 'Верно', 'Richtig', 'Correct') : tr(lang, 'Закрепим ещё раз', 'Noch einmal festigen', 'Let’s reinforce it')}</strong></header><div><small>{tr(lang, 'ПРАВИЛЬНЫЙ ОТВЕТ', 'RICHTIGE ANTWORT', 'CORRECT ANSWER')}</small><strong>{feedback.correct_answer}</strong><p>{feedback.explanation}</p></div><button type="button" className="rc-primary" onClick={next}>{index + 1 === items.length ? tr(lang, 'Завершить', 'Abschließen', 'Finish') : tr(lang, 'Следующая карточка', 'Nächste Karte', 'Next card')} <FaArrowRight /></button></div>}
      </section>
    </main>
  );
};
