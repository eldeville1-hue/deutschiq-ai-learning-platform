import React, { useEffect, useState } from 'react';
import { FaPaperPlane, FaRobot, FaVolumeUp } from 'react-icons/fa';
import { api } from '../services/api';
import { BottomNav } from '../components/BottomNav';
import { useLanguage } from '../context/LanguageContext';
import { topicLabel } from '../i18n/topics';
import { getUserId } from '../utils/user';
import { VoiceRecorder } from '../components/VoiceRecorder';

type Message = { role: 'user' | 'assistant'; content: string };
export const Tutor: React.FC = () => {
  const { lang } = useLanguage();
  const userId = getUserId();
  const [context, setContext] = useState<any>({ level: 'A1', weaknesses: [] });
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [remaining, setRemaining] = useState(0);
  useEffect(() => { Promise.all([api.getDashboard(userId), api.getTutorState(userId)]).then(([dashboard, tutor]) => { setContext(dashboard); setMessages(Array.isArray(tutor.messages) ? tutor.messages : []); setRemaining(Number(tutor.remaining || 0)); }).catch(() => undefined); }, [userId]);
  const send = async (text = question) => {
    if (!text.trim() || loading || remaining <= 0) return;
    const next = [...messages, { role: 'user' as const, content: text.trim() }];
    setMessages(next); setQuestion(''); setLoading(true);
    try { const result = await api.askTutor({ user_id: userId, question: text.trim() }); setMessages([...next, { role: 'assistant', content: result.answer || result.response || String(result) }]); setRemaining(Number(result.remaining ?? Math.max(0, remaining - 1))); }
    catch { setMessages([...next, { role: 'assistant', content: lang === 'ru' ? 'Не удалось получить ответ. Попробуй ещё раз.' : 'Die Antwort konnte nicht geladen werden. Versuche es noch einmal.' }]); }
    finally { setLoading(false); }
  };
  const quick = lang === 'ru' ? ['Объясни мою ошибку', 'Дай упражнение', 'Объясни правило'] : ['Erkläre meinen Fehler', 'Gib mir eine Übung', 'Erkläre die Regel'];
  const topics = (context.weaknesses || []).slice(0, 2).map((w: any) => topicLabel(String(w.name), lang)).join(' · ');
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
    <main className="app-shell tutor-page precision-tutor page-enter">
      <header className="page-header"><div><p className="eyebrow">{lang === 'ru' ? 'ИИ-репетитор' : 'KI-Tutor'}</p><h1>{lang === 'ru' ? 'Разберём немецкий вместе' : 'Lass uns Deutsch üben'}</h1></div><span className="quota">{remaining} {lang === 'ru' ? 'из 3 доступно' : 'von 3 verfügbar'}</span></header>
      <div className="context-strip"><FaRobot /><span>{lang === 'ru' ? `Уровень ${context.level || 'A1'} · Сегодня: ${topics || 'артикли'}` : `Niveau ${context.level || 'A1'} · Heute: ${topics || 'Artikel'}`}</span></div>
      {!messages.length && <div className="chat-empty"><span className="feature-icon"><FaRobot /></span><h2>{lang === 'ru' ? 'С чего начнём?' : 'Womit fangen wir an?'}</h2><p>{lang === 'ru' ? 'Я учитываю твой уровень и последние ошибки.' : 'Ich berücksichtige dein Niveau und deine letzten Fehler.'}</p></div>}
      <div className="quick-actions">{quick.map(x => <button key={x} onClick={() => send(x)}>{x}</button>)}</div>
      <div className="chat-messages">{messages.map((m, i) => <div key={i} className={`message ${m.role}`}>{m.content}{m.role === 'assistant' && <button className="message-audio" onClick={() => speak(m.content)} aria-label={lang === 'ru' ? 'Прослушать ответ' : 'Antwort anhören'}><FaVolumeUp /></button>}</div>)}{loading && <div className="message assistant typing">•••</div>}</div>
      <VoiceRecorder lang={lang} disabled={loading || remaining <= 0} onAudio={transcribe} />
      <div className="chat-composer"><input value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder={lang === 'ru' ? 'Напиши вопрос…' : 'Schreib deine Frage…'} /><button onClick={() => send()} disabled={!question.trim() || loading}><FaPaperPlane /></button></div>
      <BottomNav />
    </main>
  );
};
