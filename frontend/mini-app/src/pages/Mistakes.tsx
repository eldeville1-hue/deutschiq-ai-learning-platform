import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaTimes } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId } from '../utils/user';

export const Mistakes: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [items, setItems] = useState<any[] | null>(null);
  useEffect(() => { api.getMistakes(getUserId()).then(data => setItems(Array.isArray(data.mistakes) ? data.mistakes : [])).catch(() => setItems([])); }, []);
  if (items === null) return <main className="app-shell"><div className="skeleton analysis-skeleton" /></main>;
  return <main className="app-shell mistakes-page page-enter"><header><p className="eyebrow">{lang === 'ru' ? 'МОИ ОШИБКИ' : 'MEINE FEHLER'}</p><h1>{lang === 'ru' ? 'Разберём, что пошло не так' : 'Verstehe deine Fehler'}</h1><p>{lang === 'ru' ? 'Здесь только реальные ответы из последней диагностики.' : 'Hier stehen nur echte Antworten aus deiner letzten Diagnose.'}</p></header>{items.length ? <div className="mistake-cards">{items.map((item, index) => <article key={item.id || index}><small>0{index + 1} · {topicLabel(item.topic, lang)}</small><h2>{item.question}</h2><div className="answer-line wrong"><FaTimes /><span>{item.user_answer}</span></div><div className="answer-line correct"><FaCheck /><span>{item.correct_answer}</span></div>{item.explanation && <p>{item.explanation}</p>}</article>)}</div> : <section className="empty-panel"><FaCheck /><h2>{lang === 'ru' ? 'Ошибок пока нет' : 'Noch keine Fehler'}</h2><p>{lang === 'ru' ? 'После диагностики или уроков здесь появится разбор.' : 'Nach Diagnose oder Lektionen erscheint hier deine Analyse.'}</p></section>}<button className="primary-action" onClick={() => navigate('/review')}>{lang === 'ru' ? 'Повторить ошибки' : 'Fehler wiederholen'} <FaArrowRight /></button></main>;
};
