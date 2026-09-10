import React, { useCallback, useEffect, useRef, useState } from 'react';
import { FaPaperPlane, FaRobot, FaVolumeUp } from 'react-icons/fa';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { getUserId } from '../utils/user';
import { VoiceRecorder } from '../components/VoiceRecorder';

type Message = { role: 'user' | 'assistant'; content: string };
export const Tutor: React.FC = () => {
  const { lang } = useLanguage();
  const userId = getUserId();
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [remaining, setRemaining] = useState(0);
  const [ready, setReady] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [sendError, setSendError] = useState('');
  const conversationEnd = useRef<HTMLDivElement>(null);
  const loadTutor = useCallback(() => {
    setReady(false);
    return api.getTutorState(userId)
      .then((tutor) => {
        setMessages(Array.isArray(tutor.messages) ? tutor.messages : []);
        setRemaining(Number(tutor.remaining || 0));
        setLoadError(false);
      })
      .catch(() => setLoadError(true))
      .finally(() => setReady(true));
  }, [userId]);
  useEffect(() => { void loadTutor(); }, [loadTutor]);
  useEffect(() => { conversationEnd.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, [messages, loading]);
  const send = async (text = question) => {
    if (!text.trim() || loading) return;
    const next = [...messages, { role: 'user' as const, content: text.trim() }];
    setMessages(next); setQuestion(''); setLoading(true); setSendError('');
    try { const result = await api.askTutor({ user_id: userId, question: text.trim(), history: messages.slice(-10) }); setMessages([...next, { role: 'assistant', content: result.answer || result.response || String(result) }]); setRemaining(Number(result.remaining ?? Math.max(0, remaining - 1))); }
    catch (error: any) {
      const limited = error?.response?.status === 429;
      const message = limited ? (lang === 'ru' ? 'Достигнут защитный лимит бета‑тестирования. Продолжим завтра.' : 'Das Schutzlimit der Beta ist erreicht. Morgen geht es weiter.') : (lang === 'ru' ? 'Связь прервалась. Вопрос сохранён — нажми «Повторить».' : 'Die Verbindung wurde unterbrochen. Tippe auf „Erneut senden“.');
      setMessages(next); setQuestion(text.trim()); setSendError(message);
      if (limited) setRemaining(0);
    }
    finally { setLoading(false); }
  };
  const quick = lang === 'ru'
    ? [{ title: 'Ошибка', prompt: 'Объясни мою последнюю ошибку и дай пример' }, { title: 'Задание', prompt: 'Дай мне одно упражнение по теме дня' }, { title: 'Правило', prompt: 'Объясни правило сегодняшней темы простыми словами' }]
    : [{ title: 'Fehler', prompt: 'Erkläre meinen letzten Fehler und gib ein Beispiel' }, { title: 'Aufgabe', prompt: 'Gib mir eine Aufgabe zum heutigen Thema' }, { title: 'Regel', prompt: 'Erkläre die heutige Regel einfach' }];
  const transcribe = async (audio: Blob) => {
    const result = await api.transcribeTutorSpeech(userId, audio);
    setQuestion(result.transcript || '');
  };
  const speak = (text: string) => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = /[äöüß]|\b(ich|du|der|die|das|und)\b/i.test(text) ? 'de-DE' : (lang === 'ru' ? 'ru-RU' : 'de-DE');
    utterance.rate = .92;
    window.speechSynthesis.speak(utterance);
  };
  return (
    <main className="app-shell tutor-page precision-tutor v30-page v30-tutor page-enter">
      <header className="page-header"><div><p className="eyebrow">{lang === 'ru' ? 'ИИ-ПОМОЩНИК' : 'KI-HILFE'}</p><h1>{lang === 'ru' ? 'Репетитор' : 'Tutor'}</h1></div><span className="quota">BETA</span></header>
      {!ready && <div className="rc-notice"><span>{lang === 'ru' ? 'Подготавливаем репетитора…' : 'Tutor wird vorbereitet…'}</span></div>}
      {loadError && <div className="rc-notice error"><span>{lang === 'ru' ? 'Не удалось загрузить историю' : 'Verlauf konnte nicht geladen werden'}</span><button type="button" onClick={loadTutor}>{lang === 'ru' ? 'Повторить' : 'Erneut laden'}</button></div>}
      <section className={`tutor-workspace${messages.length ? ' has-messages' : ''}`}>
        {!messages.length && <div className="chat-empty"><span className="feature-icon"><FaRobot /></span><h2>{lang === 'ru' ? 'Чем помочь?' : 'Wobei helfen?'}</h2><div className="quick-actions">{quick.map(item => <button type="button" key={item.title} disabled={!ready || loading} onClick={() => send(item.prompt)}>{item.title}</button>)}</div></div>}
        <div className="chat-messages" aria-live="polite">{messages.map((m, i) => <div key={i} className={`message ${m.role}`}>{m.content}{m.role === 'assistant' && <button type="button" className="message-audio" onClick={() => speak(m.content)} aria-label={lang === 'ru' ? 'Прослушать ответ' : 'Antwort anhören'}><FaVolumeUp /></button>}</div>)}{loading && <div className="message assistant typing">•••</div>}<div ref={conversationEnd} /></div>
      </section>
      <section className="tutor-dock">
        {sendError && <div className="rc-notice error"><span>{sendError}</span><button type="button" disabled={loading} onClick={() => send()}>{lang === 'ru' ? 'Повторить' : 'Erneut senden'}</button></div>}
        <div className="chat-composer"><input aria-label={lang === 'ru' ? 'Вопрос репетитору' : 'Frage an den Tutor'} value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); send(); } }} placeholder={lang === 'ru' ? 'Спроси о немецком…' : 'Frage auf Deutsch…'} /><button type="button" aria-label={lang === 'ru' ? 'Отправить' : 'Senden'} onClick={() => send()} disabled={!ready || !question.trim() || loading}><FaPaperPlane /></button></div>
        <VoiceRecorder compact lang={lang} disabled={loading} onAudio={transcribe} />
      </section>
    </main>
  );
};
