import React, { useState } from 'react';
import { FaCheckCircle, FaFlask } from 'react-icons/fa';
import { api } from '../services/api';
import { getUserId } from '../utils/user';
import { useLanguage } from '../context/LanguageContext';
import { tr } from '../i18n/language';

export const BetaAccess: React.FC<{ onDone: () => void }> = ({ onDone }) => {
  const { lang } = useLanguage();
  const [code, setCode] = useState(() => new URLSearchParams(location.search).get('invite') || '');
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false);
  const submit = async () => { setBusy(true); setError(''); try { await api.claimBetaInvite({ user_id: getUserId(), code, language: lang }); onDone(); } catch { setError(tr(lang, 'Код недействителен или лимит исчерпан.', 'Der Code ist ungültig oder voll.', 'This code is invalid or has reached its limit.')); } finally { setBusy(false); } };
  return <main className="beta-gate"><section><FaFlask /><small>DEUTSCHIQ CLOSED BETA</small><h1>{tr(lang,'Войди в закрытую бету','Zur geschlossenen Beta','Join the closed beta')}</h1><p>{tr(lang,'Введи код приглашения. Твои отзывы помогут улучшить курс.','Gib deinen Einladungscode ein. Dein Feedback verbessert den Kurs.','Enter your invite code. Your feedback will help shape the course.')}</p><input value={code} onChange={e=>setCode(e.target.value.toUpperCase())} placeholder="BETA CODE" maxLength={32}/><button onClick={submit} disabled={busy || code.trim().length < 4}>{busy ? '…' : tr(lang,'Продолжить','Weiter','Continue')}</button>{error && <div className="beta-error">{error}</div>}</section></main>;
};

export const BetaOnboarding: React.FC<{ onDone: () => void }> = ({ onDone }) => {
  const { lang } = useLanguage(); const [goal,setGoal]=useState('conversation'); const [minutes,setMinutes]=useState(15); const [consent,setConsent]=useState(false); const [busy,setBusy]=useState(false); const [error,setError]=useState('');
  const submit=async()=>{setBusy(true);setError('');try{await api.completeBetaOnboarding({user_id:getUserId(),goal,study_minutes:minutes,consent});onDone();}catch{setError(tr(lang,'Не удалось сохранить. Попробуй снова.','Speichern fehlgeschlagen.','Could not save. Try again.'));}finally{setBusy(false)}};
  return <main className="beta-gate"><section><FaCheckCircle/><small>2-MINUTE SETUP</small><h1>{tr(lang,'Настроим твою бету','Deine Beta einrichten','Set up your beta')}</h1><label>{tr(lang,'Главная цель','Hauptziel','Primary goal')}<select value={goal} onChange={e=>setGoal(e.target.value)}><option value="conversation">Conversation</option><option value="work">Work / study</option><option value="exam">Exam</option><option value="daily-life">Daily life</option></select></label><label>{tr(lang,'Минут в день','Minuten pro Tag','Minutes per day')}<select value={minutes} onChange={e=>setMinutes(Number(e.target.value))}><option value={10}>10</option><option value={15}>15</option><option value={20}>20</option><option value={30}>30</option></select></label><label className="beta-consent"><input type="checkbox" checked={consent} onChange={e=>setConsent(e.target.checked)}/><span>{tr(lang,'Я согласен участвовать и отправлять данные об использовании и отзывы.','Ich stimme der Teilnahme und der Übermittlung von Nutzungsdaten und Feedback zu.','I agree to participate and share usage data and feedback.')}</span></label><button onClick={submit} disabled={!consent||busy}>{tr(lang,'Начать обучение','Lernen starten','Start learning')}</button>{error&&<div className="beta-error">{error}</div>}</section></main>;
};
