import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaTimes } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';

export const Mistakes: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [items, setItems] = useState<any[] | null>(null);
  useEffect(() => { api.getMistakes(getUserId()).then(data => setItems(Array.isArray(data.mistakes) ? data.mistakes : [])).catch(() => setItems([])); }, []);
  if (items === null) return <main className="app-shell"><div className="skeleton analysis-skeleton" /></main>;
  return <main className="app-shell mistakes-page page-enter"><header><p className="eyebrow">{lang === 'ru' ? 'ОШИБКИ' : 'FEHLER'}</p><h1>{lang === 'ru' ? 'Разбор ответов' : 'Antworten verstehen'}</h1><p>{lang === 'ru' ? 'Смотри правило и исправляй ошибку.' : 'Sieh dir die Regel an und korrigiere den Fehler.'}</p></header>{items.length ? <div className="mistake-cards">{items.map((item, index) => <article key={item.id || index}><small>0{index + 1} · {topicLabel(item.topic, lang)}</small><h2>{item.question}</h2><div className="answer-line wrong"><FaTimes /><span><small>{lang === 'ru' ? 'ТВОЙ ОТВЕТ' : 'DEINE ANTWORT'}</small>{item.user_answer}</span></div><div className="answer-line correct"><FaCheck /><span><small>{lang === 'ru' ? 'ПРАВИЛЬНО' : 'RICHTIG'}</small>{item.correct_answer}</span></div>{item.explanation && <p>{item.explanation}</p>}</article>)}</div> : <section className="empty-panel"><FaCheck /><h2>{lang === 'ru' ? 'Ошибок пока нет' : 'Noch keine Fehler'}</h2><p>{lang === 'ru' ? 'Они появятся здесь после заданий.' : 'Sie erscheinen hier nach den Aufgaben.'}</p></section>}{items.length > 0 && <button className="primary-action" onClick={() => navigate(withUser('/review'))}>{lang === 'ru' ? 'Закрепить' : 'Üben'} <FaArrowRight /></button>}</main>;
};
