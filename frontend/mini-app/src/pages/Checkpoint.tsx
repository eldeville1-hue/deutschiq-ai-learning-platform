import React, { useEffect, useState } from 'react';
import { FaArrowRight, FaCheck, FaTimes } from 'react-icons/fa';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { tr } from '../i18n/language';
import { getUserId, withUser } from '../utils/user';

export const Checkpoint: React.FC = () => {
  const { level = 'A1' } = useParams(); const { lang } = useLanguage(); const navigate = useNavigate();
  const [data,setData]=useState<any>(null); const [index,setIndex]=useState(0); const [answers,setAnswers]=useState<string[]>([]); const [answer,setAnswer]=useState(''); const [result,setResult]=useState<any>(null); const [error,setError]=useState('');
  useEffect(()=>{ api.getCheckpoint(getUserId(),level,lang).then(setData).catch(()=>setError(tr(lang,'Тест пока недоступен. Сначала заверши маршрут.','Der Test ist noch nicht verfügbar. Schließe zuerst deinen Lernweg ab.','The checkpoint is not available yet. Complete your learning path first.'))); },[lang,level]);
  const item=data?.items?.[index];
  const next=async()=>{ const updated=[...answers]; updated[index]=answer; setAnswers(updated); setAnswer(''); if(index+1<(data?.items?.length||0)){setIndex(index+1);return;} const value=await api.submitCheckpoint({user_id:getUserId(),level,answers:updated,language:lang}); setResult(value); };
  if(error) return <main className="app-shell checkpoint-page"><div className="rc-notice error">{error}</div><button className="rc-primary" onClick={()=>navigate(withUser('/plan'))}>{tr(lang,'Вернуться к плану','Zurück zum Plan','Back to plan')}</button></main>;
  if(!data) return <main className="app-shell checkpoint-page"><div className="skeleton rc-hero-skeleton" /></main>;
  if(result) return <main className="app-shell checkpoint-page checkpoint-result"><span className={`result-icon ${result.passed?'':'needs-practice'}`}>{result.passed?<FaCheck/>:<FaTimes/>}</span><p className="eyebrow">{result.passed?tr(lang,'УРОВЕНЬ ПОДТВЕРЖДЁН','NIVEAU BESTÄTIGT','LEVEL CONFIRMED'):tr(lang,'НУЖНО ЕЩЁ ПОВТОРИТЬ','NOCH ETWAS ÜBEN','MORE REVIEW NEEDED')}</p><h1>{result.score}%</h1>{result.unlocked_level&&<div className="level-unlocked"><small>{tr(lang,'ОТКРЫТ НОВЫЙ УРОВЕНЬ','NEUES NIVEAU FREIGESCHALTET','NEW LEVEL UNLOCKED')}</small><strong>{result.unlocked_level}</strong><span>{tr(lang,'Новый маршрут уже доступен.','Der neue Lernweg ist jetzt verfügbar.','Your new learning path is ready.')}</span></div>}<button className="rc-primary" onClick={()=>navigate(withUser('/plan'))}>{tr(lang,'К маршруту','Zum Lernweg','Go to journey')}</button></main>;
  return <main className="app-shell checkpoint-page"><header><p className="eyebrow">{level} · {tr(lang,'ФИНАЛЬНЫЙ ТЕСТ','ABSCHLUSSTEST','FINAL CHECKPOINT')}</p><h1>{index+1}/{data.items.length}</h1><div className="progress-bar"><div className="progress-bar-fill" style={{width:`${((index+1)/data.items.length)*100}%`}}/></div></header><section className="checkpoint-card"><h2>{item?.question}</h2>{item?.options?.length?<div className="lesson-options">{item.options.map((option:string)=><button key={option} className={answer===option?'active':''} onClick={()=>setAnswer(option)}>{option}</button>)}</div>:<textarea className="lesson-answer" value={answer} onChange={event=>setAnswer(event.target.value)} placeholder={tr(lang,'Напиши ответ…','Schreibe deine Antwort…','Type your answer…')}/>}<button className="rc-primary" disabled={!answer.trim()} onClick={next}>{index+1===data.items.length?tr(lang,'Завершить','Abschließen','Finish'):tr(lang,'Дальше','Weiter','Next')} <FaArrowRight/></button></section></main>;
};
