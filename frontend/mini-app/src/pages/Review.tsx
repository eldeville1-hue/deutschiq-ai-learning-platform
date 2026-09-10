import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaRedo, FaTimes } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const Review: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [items, setItems] = useState<any[] | null>(null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState<any>(null);
  const [startedAt, setStartedAt] = useState(Date.now());
  const [sessionId, setSessionId] = useState('');
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => { api.getReviews(getUserId()).then(data => setItems(data.reviews || [])).catch(() => { setItems([]); setError(lang === 'ru' ? 'Не удалось загрузить повторения.' : 'Wiederholungen konnten nicht geladen werden.'); }); }, [lang]);

  const leave = () => navigate(withUser('/dashboard'));
  if (items === null) return <main className="lesson-flow rc-review"><div className="skeleton rc-hero-skeleton" /></main>;
  if (!items.length) return <main className="lesson-flow rc-review rc-review-state"><span className="rc-state-icon"><FaCheck /></span><p>{lang === 'ru' ? 'ПОВТОРЕНИЕ' : 'WIEDERHOLUNG'}</p><h1>{error ? (lang === 'ru' ? 'Не удалось загрузить' : 'Laden fehlgeschlagen') : (lang === 'ru' ? 'На сегодня всё' : 'Für heute erledigt')}</h1><span>{error || (lang === 'ru' ? 'Новые карточки появятся после урока.' : 'Neue Karten erscheinen nach der Lektion.')}</span><button type="button" className="rc-primary" onClick={leave}>{lang === 'ru' ? 'На главную' : 'Zur Übersicht'}</button></main>;
  if (index >= items.length) return <main className="lesson-flow rc-review rc-review-state"><span className="rc-state-icon success"><FaCheck /></span><p>{lang === 'ru' ? 'ГОТОВО' : 'FERTIG'}</p><h1>{lang === 'ru' ? 'Память укреплена' : 'Erinnerung gefestigt'}</h1><span>{lang === 'ru' ? `${items.length} тем повторено. Следующая дата рассчитана по твоим ответам.` : `${items.length} Themen wiederholt. Der nächste Termin wurde aus deinen Antworten berechnet.`}</span><button type="button" className="rc-primary" onClick={leave}>{lang === 'ru' ? 'Продолжить' : 'Weiter'} <FaArrowRight /></button></main>;

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
      const result = await api.checkLessonAnswer({ user_id: getUserId(), lesson_id: item.lesson_id, exercise_index: item.exercise_index, answer, session_id: activeSession, confidence: 'okay', response_ms: Date.now() - startedAt });
      setFeedback(result);
    } catch {
      setError(lang === 'ru' ? 'Ответ не отправился. Проверь соединение и повтори.' : 'Die Antwort wurde nicht gesendet. Prüfe die Verbindung und versuche es erneut.');
    } finally { setChecking(false); }
  };
  const next = () => { setIndex(value => value + 1); setAnswer(''); setFeedback(null); setSessionId(''); setError(''); setStartedAt(Date.now()); };
  const progress = ((index + (feedback ? 1 : 0)) / items.length) * 100;

  return (
    <main className="lesson-flow rc-review page-enter">
      <header className="rc-review-top"><button type="button" onClick={leave} aria-label={lang === 'ru' ? 'Закрыть повторение' : 'Wiederholung schließen'}><FaTimes /></button><div><span>{lang === 'ru' ? 'ПОВТОРЕНИЕ' : 'WIEDERHOLUNG'}</span><small>{index + 1} / {items.length}</small></div></header>
      <div className="rc-review-progress"><i style={{ width: `${progress}%` }} /></div>

      <section className="rc-review-question">
        <div className="rc-retrieval-label"><FaRedo /><span>{lang === 'ru' ? 'Вспомни' : 'Erinnere dich'}</span></div>
        <p>{topicLabel(item.topic, lang)}</p>
        <h1>{item.question}</h1>

        {!feedback && (item.type === 'choose' && item.options?.length
          ? <div className="rc-review-options">{item.options.map((option: string) => <button type="button" key={option} className={answer === option ? 'selected' : ''} onClick={() => setAnswer(option)}><span>{option}</span>{answer === option && <FaCheck />}</button>)}</div>
          : <label className="rc-review-input"><span>{lang === 'ru' ? 'Твой ответ' : 'Deine Antwort'}</span><input value={answer} onChange={event => setAnswer(event.target.value)} onKeyDown={event => { if (event.key === 'Enter') void check(); }} placeholder={lang === 'ru' ? 'Напиши по памяти…' : 'Aus dem Gedächtnis…'} /></label>)}

        {error && <div className="rc-notice error"><span>{error}</span></div>}

        {!feedback
          ? <button type="button" className="rc-primary" disabled={!answer.trim() || checking} onClick={check}>{checking ? (lang === 'ru' ? 'Проверяем…' : 'Wird geprüft…') : (lang === 'ru' ? 'Проверить' : 'Prüfen')}</button>
          : <div className={`rc-review-feedback ${feedback.correct ? 'correct' : 'wrong'}`}><header><span>{feedback.correct ? <FaCheck /> : <FaRedo />}</span><strong>{feedback.correct ? (lang === 'ru' ? 'Верно' : 'Richtig') : (lang === 'ru' ? 'Закрепим ещё раз' : 'Noch einmal festigen')}</strong></header><div><small>{lang === 'ru' ? 'ПРАВИЛЬНЫЙ ОТВЕТ' : 'RICHTIGE ANTWORT'}</small><strong>{feedback.correct_answer}</strong><p>{feedback.explanation}</p></div><button type="button" className="rc-primary" onClick={next}>{index + 1 === items.length ? (lang === 'ru' ? 'Завершить' : 'Abschließen') : (lang === 'ru' ? 'Следующая карточка' : 'Nächste Karte')} <FaArrowRight /></button></div>}
      </section>
    </main>
  );
};
