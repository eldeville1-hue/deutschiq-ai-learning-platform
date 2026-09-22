import React, { useState } from 'react';
import { FaBug, FaCheck, FaPaperPlane, FaTimes } from 'react-icons/fa';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { getUserId } from '../utils/user';
import { tr } from '../i18n/language';

export const BetaIssueReporter: React.FC = () => {
  const { lang } = useLanguage();
  const [open, setOpen] = useState(false);
  const [category, setCategory] = useState('problem');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState<'idle'|'sending'|'sent'|'error'>('idle');
  const submit = async () => {
    if (!message.trim()) return;
    setStatus('sending');
    try {
      let context: any = {};
      try { context = JSON.parse(sessionStorage.getItem('deutschiq-beta-context') || '{}'); } catch { /* Context is optional. */ }
      await api.reportBetaIssue({ user_id: getUserId(), category, message: message.trim(), page: location.pathname, ...context });
      setStatus('sent'); setMessage('');
      window.setTimeout(() => { setOpen(false); setStatus('idle'); }, 1100);
    } catch { setStatus('error'); }
  };
  return <div className="beta-reporter">
    <button className="beta-report-trigger" type="button" aria-label={tr(lang,'Сообщить о проблеме','Problem melden','Report a problem')} onClick={()=>setOpen(true)}><FaBug /></button>
    {open && <div className="beta-report-backdrop" role="presentation" onClick={()=>setOpen(false)}><section role="dialog" aria-modal="true" aria-labelledby="beta-report-title" onClick={event=>event.stopPropagation()}>
      <header><div><small>BETA FEEDBACK</small><h2 id="beta-report-title">{tr(lang,'Что случилось?','Was ist passiert?','What happened?')}</h2></div><button aria-label={tr(lang,'Закрыть','Schließen','Close')} onClick={()=>setOpen(false)}><FaTimes/></button></header>
      <select value={category} onChange={e=>setCategory(e.target.value)}><option value="problem">{tr(lang,'Что-то не работает','Etwas funktioniert nicht','Something is broken')}</option><option value="unclear">{tr(lang,'Непонятное задание','Unklare Aufgabe','Unclear exercise')}</option><option value="idea">{tr(lang,'Идея улучшения','Verbesserungsidee','Improvement idea')}</option></select>
      <textarea autoFocus maxLength={800} value={message} onChange={e=>setMessage(e.target.value)} placeholder={tr(lang,'Опиши коротко — урок и задание добавятся автоматически.','Beschreibe es kurz – Lektion und Aufgabe werden automatisch ergänzt.','Describe it briefly — the lesson and exercise are added automatically.')} />
      <button className="beta-report-submit" disabled={!message.trim()||status==='sending'} onClick={submit}>{status==='sent'?<><FaCheck/> {tr(lang,'Отправлено','Gesendet','Sent')}</>:<><FaPaperPlane/> {status==='sending'?tr(lang,'Отправляем…','Wird gesendet…','Sending…'):tr(lang,'Отправить','Senden','Send')}</>}</button>
      {status==='error'&&<p role="alert">{tr(lang,'Не удалось отправить. Попробуй ещё раз.','Senden fehlgeschlagen. Versuche es erneut.','Could not send. Try again.')}</p>}
    </section></div>}
  </div>;
};
