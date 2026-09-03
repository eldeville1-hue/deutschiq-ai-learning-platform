import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaRedo } from 'react-icons/fa';
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
  useEffect(() => { api.getReviews(getUserId()).then(data => setItems(data.reviews || [])).catch(() => setItems([])); }, []);
  if (items === null) return <main className="lesson-flow"><div className="skeleton hero-skeleton" /></main>;
  if (!items.length) return <main className="lesson-flow review-empty"><FaCheck /><p className="eyebrow">{lang === 'ru' ? 'ПАМЯТЬ В ПОРЯДКЕ' : 'ALLES WIEDERHOLT'}</p><h1>{lang === 'ru' ? 'Сегодня повторений нет' : 'Heute ist nichts fällig'}</h1><p>{lang === 'ru' ? 'Вернись после следующего урока — DeutschIQ сам выберет нужный момент.' : 'Nach der nächsten Lektion plant DeutschIQ den richtigen Zeitpunkt.'}</p><button className="primary-action" onClick={() => navigate(withUser('/dashboard'))}>{lang === 'ru' ? 'На главную' : 'Zur Übersicht'}</button></main>;
  if (index >= items.length) return <main className="lesson-flow review-empty"><FaCheck /><p className="eyebrow">{lang === 'ru' ? 'ПОВТОРЕНИЕ ЗАВЕРШЕНО' : 'WIEDERHOLUNG FERTIG'}</p><h1>{lang === 'ru' ? `${items.length} тем закреплено` : `${items.length} Themen gefestigt`}</h1><button className="primary-action" onClick={() => navigate(withUser('/dashboard'))}>{lang === 'ru' ? 'Продолжить' : 'Weiter'} <FaArrowRight /></button></main>;
  const item = items[index];
  const ensureSession = async () => sessionId || (await api.startLesson({user_id:getUserId(), lesson_id:item.lesson_id})).session_id;
  const check = async () => { if (!answer.trim()) return; const activeSession = await ensureSession(); setSessionId(activeSession); setFeedback(await api.checkLessonAnswer({ user_id:getUserId(), lesson_id:item.lesson_id, exercise_index:item.exercise_index, answer, session_id:activeSession, confidence:'okay', response_ms:Date.now()-startedAt })); };
  const next = () => { setIndex(value => value + 1); setAnswer(''); setFeedback(null); setSessionId(''); setStartedAt(Date.now()); };
  return <main className="lesson-flow review-page"><header><span>{index + 1} {lang === 'ru' ? 'из' : 'von'} {items.length}</span><div className="progress-bar"><div className="progress-bar-fill" style={{width:`${(index + 1) / items.length * 100}%`}} /></div></header><section className="review-card"><div className="retrieval-label"><FaRedo /><span>{lang === 'ru' ? 'Вспомни без подсказки' : 'Ohne Hinweis erinnern'}</span></div><p className="eyebrow">{topicLabel(item.topic, lang)} · {lang === 'ru' ? `освоено ${item.mastery}%` : `${item.mastery}% beherrscht`}</p><h1>{item.question}</h1>{item.type === 'choose' && item.options?.length ? <div className="lesson-options">{item.options.map((option:string) => <button key={option} className={answer === option ? 'active' : ''} onClick={() => setAnswer(option)}>{option}</button>)}</div> : <input className="lesson-answer" value={answer} onChange={event => setAnswer(event.target.value)} placeholder={lang === 'ru' ? 'Ответ по памяти' : 'Antwort aus dem Gedächtnis'} />}{!feedback ? <button className="primary-action" onClick={check}>{lang === 'ru' ? 'Проверить память' : 'Erinnerung prüfen'}</button> : <div className={`review-reveal ${feedback.correct ? 'correct' : 'wrong'}`}><small>{feedback.correct ? (lang === 'ru' ? 'Вспомнил правильно' : 'Richtig erinnert') : (lang === 'ru' ? 'Повторим снова завтра' : 'Morgen noch einmal')}</small><strong>{feedback.correct_answer}</strong><p>{feedback.explanation}</p><button className="primary-action" onClick={next}>{lang === 'ru' ? 'Дальше' : 'Weiter'} <FaArrowRight /></button></div>}</section></main>;
};
