import React, { useCallback, useEffect, useRef, useState } from 'react';
import { FaPaperPlane, FaRobot, FaVolumeUp } from 'react-icons/fa';
import { api } from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import { getUserId } from '../utils/user';
import { VoiceRecorder } from '../components/VoiceRecorder';
import { tr } from '../i18n/language';

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
    return api.getTutorState(userId, lang)
      .then((tutor) => {
        setMessages(Array.isArray(tutor.messages) ? tutor.messages : []);
        setRemaining(Number(tutor.remaining || 0));
        setLoadError(false);
      })
      .catch(() => setLoadError(true))
      .finally(() => setReady(true));
  }, [lang, userId]);
  useEffect(() => { void api.trackEvent({ user_id: userId, event_name: 'tutor_opened' }); void loadTutor(); }, [loadTutor, userId]);
  useEffect(() => { conversationEnd.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, [messages, loading]);
  const send = async (text = question) => {
    if (!text.trim() || loading) return;
    const next = [...messages, { role: 'user' as const, content: text.trim() }];
    setMessages(next); setQuestion(''); setLoading(true); setSendError('');
    try { const result = await api.askTutor({ user_id: userId, question: text.trim(), language: lang, history: messages.slice(-10) }); setMessages([...next, { role: 'assistant', content: result.answer || result.response || String(result) }]); setRemaining(Number(result.remaining ?? Math.max(0, remaining - 1))); }
    catch (error: any) {
      const limited = error?.response?.status === 429;
      const message = limited
        ? tr(lang, 'Достигнут защитный лимит бета‑тестирования. Продолжим завтра.', 'Das Schutzlimit der Beta ist erreicht. Morgen geht es weiter.', 'The beta safety limit has been reached. Continue tomorrow.')
        : tr(lang, 'Связь прервалась. Вопрос сохранён — нажми «Повторить».', 'Die Verbindung wurde unterbrochen. Tippe auf „Erneut senden“.', 'The connection was interrupted. Your question is saved — tap “Try again”.');
      setMessages(next); setQuestion(text.trim()); setSendError(message);
      if (limited) setRemaining(0);
    }
    finally { setLoading(false); }
  };
  const quick = lang === 'ru'
    ? [{ title: 'Разобрать мою ошибку', prompt: 'Объясни мою последнюю ошибку и дай пример' }, { title: 'Практика на сегодня', prompt: 'Дай мне одно упражнение по теме дня' }, { title: 'Объяснить проще', prompt: 'Объясни правило сегодняшней темы простыми словами' }]
    : lang === 'de'
      ? [{ title: 'Meinen Fehler erklären', prompt: 'Erkläre meinen letzten Fehler und gib ein Beispiel' }, { title: 'Heute üben', prompt: 'Gib mir eine Aufgabe zum heutigen Thema' }, { title: 'Einfacher erklären', prompt: 'Erkläre die heutige Regel einfach' }]
      : [{ title: 'Explain my mistake', prompt: 'Explain my latest mistake and give one example' }, { title: 'Practice today', prompt: 'Give me one exercise on today’s topic' }, { title: 'Explain simply', prompt: 'Explain today’s rule in simple English' }];
  const transcribe = async (audio: Blob) => {
    const result = await api.transcribeTutorSpeech(userId, audio);
    setQuestion(result.transcript || '');
  };
  const speak = (text: string) => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = /[äöüß]|\b(ich|du|der|die|das|und)\b/i.test(text) ? 'de-DE' : (lang === 'ru' ? 'ru-RU' : lang === 'de' ? 'de-DE' : 'en-US');
    utterance.rate = .92;
    window.speechSynthesis.speak(utterance);
  };
  return (
    <main className="app-shell tutor-page precision-tutor v30-page v30-tutor page-enter">
      <header className="page-header"><div><p className="eyebrow">{tr(lang, 'ИИ-ПОМОЩНИК', 'KI-HILFE', 'AI TUTOR')}</p><h1>{tr(lang, 'Репетитор', 'Tutor', 'Tutor')}</h1></div><span className="quota">BETA</span></header>
      {!ready && <div className="rc-notice"><span>{tr(lang, 'Подготавливаем репетитора…', 'Tutor wird vorbereitet…', 'Preparing your tutor…')}</span></div>}
      {loadError && <div className="rc-notice error"><span>{tr(lang, 'Не удалось загрузить историю', 'Verlauf konnte nicht geladen werden', 'Could not load chat history')}</span><button type="button" onClick={loadTutor}>{tr(lang, 'Повторить', 'Erneut laden', 'Try again')}</button></div>}
      <section className={`tutor-workspace${messages.length ? ' has-messages' : ''}`}>
        {!messages.length && <div className="chat-empty"><span className="feature-icon"><FaRobot /></span><h2>{tr(lang, 'Что разберём?', 'Was möchtest du klären?', 'What should we work on?')}</h2><p>{tr(lang, 'Выбери быстрый вариант или задай свой вопрос.', 'Wähle einen Einstieg oder stelle deine eigene Frage.', 'Choose a quick start or ask your own question.')}</p><div className="quick-actions">{quick.map(item => <button type="button" key={item.title} disabled={!ready || loading} onClick={() => send(item.prompt)}>{item.title}</button>)}</div></div>}
        <div className="chat-messages" aria-live="polite">{messages.map((m, i) => <div key={i} className={`message ${m.role}`}>{m.content}{m.role === 'assistant' && <button type="button" className="message-audio" onClick={() => speak(m.content)} aria-label={tr(lang, 'Прослушать ответ', 'Antwort anhören', 'Listen to answer')}><FaVolumeUp /></button>}</div>)}{loading && <div className="message assistant typing">•••</div>}<div ref={conversationEnd} /></div>
      </section>
      <section className="tutor-dock">
        {sendError && <div className="rc-notice error"><span>{sendError}</span><button type="button" disabled={loading} onClick={() => send()}>{tr(lang, 'Повторить', 'Erneut senden', 'Try again')}</button></div>}
        <div className="chat-composer"><input aria-label={tr(lang, 'Вопрос репетитору', 'Frage an den Tutor', 'Question for the tutor')} value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); send(); } }} placeholder={tr(lang, 'Спроси о немецком…', 'Frage auf Deutsch…', 'Ask about German…')} /><button type="button" aria-label={tr(lang, 'Отправить', 'Senden', 'Send')} onClick={() => send()} disabled={!ready || !question.trim() || loading}><FaPaperPlane /></button></div>
        <VoiceRecorder compact lang={lang} disabled={loading} onAudio={transcribe} />
      </section>
    </main>
  );
};
