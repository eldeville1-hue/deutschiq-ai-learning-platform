import React, { useCallback, useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaTimes } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId, withUser } from '../utils/user';
import { tr } from '../i18n/language';

export const Mistakes: React.FC = () => {
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const [items, setItems] = useState<any[] | null>(null);
  const [loadError, setLoadError] = useState(false);
  const load = useCallback(() => {
    setItems(null);
    setLoadError(false);
    api.getMistakes(getUserId(), lang)
      .then(data => setItems(Array.isArray(data.mistakes) ? data.mistakes : []))
      .catch(() => { setItems([]); setLoadError(true); });
  }, [lang]);
  useEffect(() => { load(); }, [load]);
  if (items === null) return <main className="app-shell"><div className="skeleton analysis-skeleton" /></main>;
  return <main className="app-shell mistakes-page page-enter"><header><p className="eyebrow">{tr(lang, 'ОШИБКИ', 'FEHLER', 'MISTAKES')}</p><h1>{tr(lang, 'Разбор ответов', 'Antworten verstehen', 'Review your answers')}</h1><p>{tr(lang, 'Смотри правило и исправляй ошибку.', 'Sieh dir die Regel an und korrigiere den Fehler.', 'See the rule, then correct the mistake.')}</p></header>{loadError ? <section className="empty-panel"><FaTimes /><h2>{tr(lang, 'Не удалось загрузить ошибки', 'Fehler konnten nicht geladen werden', 'Could not load your mistakes')}</h2><p>{tr(lang, 'Проверь соединение и попробуй ещё раз.', 'Prüfe deine Verbindung und versuche es erneut.', 'Check your connection and try again.')}</p><button type="button" className="primary-action" onClick={load}>{tr(lang, 'Повторить', 'Erneut versuchen', 'Try again')}</button></section> : items.length ? <div className="mistake-cards">{items.map((item, index) => <article key={item.id || index}><small>0{index + 1} · {topicLabel(item.topic, lang)}</small><h2>{item.question}</h2><div className="answer-line wrong"><FaTimes /><span><small>{tr(lang, 'ТВОЙ ОТВЕТ', 'DEINE ANTWORT', 'YOUR ANSWER')}</small>{item.user_answer}</span></div><div className="answer-line correct"><FaCheck /><span><small>{tr(lang, 'ПРАВИЛЬНО', 'RICHTIG', 'CORRECT')}</small>{item.correct_answer}</span></div>{item.explanation && <p>{item.explanation}</p>}</article>)}</div> : <section className="empty-panel"><FaCheck /><h2>{tr(lang, 'Ошибок пока нет', 'Noch keine Fehler', 'No mistakes yet')}</h2><p>{tr(lang, 'Они появятся здесь после заданий.', 'Sie erscheinen hier nach den Aufgaben.', 'They will appear here after exercises.')}</p></section>}{!loadError && items.length > 0 && <button className="primary-action" onClick={() => navigate(withUser('/review'))}>{tr(lang, 'Закрепить', 'Üben', 'Practice')} <FaArrowRight /></button>}</main>;
};
