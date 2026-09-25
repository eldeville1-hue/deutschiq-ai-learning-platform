import React, { useEffect, useMemo, useState } from 'react';
import { FaArrowRight, FaCheck, FaExchangeAlt, FaMicrophone, FaRedo, FaTimes, FaUndo } from 'react-icons/fa';
import type { AppLanguage } from '../../i18n/language';
import { tr } from '../../i18n/language';
import { exerciseKind, type LearningExercise } from '../../learning/exercises';
import { VoiceRecorder } from '../VoiceRecorder';

type Props = {
  exercise: LearningExercise;
  answer: string;
  onAnswer: (answer: string) => void;
  disabled?: boolean;
  lang: AppLanguage;
  onAudio?: (blob: Blob) => Promise<void>;
};

export const ExerciseInteraction: React.FC<Props> = ({ exercise, answer, onAnswer, disabled = false, lang, onAudio }) => {
  const kind = exerciseKind(exercise);
  const [selectedTokens, setSelectedTokens] = useState<number[]>([]);
  const [conversationStep, setConversationStep] = useState(0);
  const [conversationDraft, setConversationDraft] = useState('');
  const [conversationReplies, setConversationReplies] = useState<string[]>([]);
  const tokens = useMemo(() => Array.isArray(exercise.tokens) ? exercise.tokens : [], [exercise.tokens]);
  const turns = useMemo(() => Array.isArray(exercise.conversation_turns) ? exercise.conversation_turns : [], [exercise.conversation_turns]);

  useEffect(() => {
    setSelectedTokens([]);
    setConversationStep(0);
    setConversationDraft('');
    setConversationReplies([]);
  }, [exercise.id, exercise.question]);

  const chooseToken = (_token: string, index: number) => {
    if (disabled || selectedTokens.includes(index)) return;
    const next = [...selectedTokens, index];
    setSelectedTokens(next);
    onAnswer(next.map(item => tokens[item]).join(' '));
  };
  const undoToken = (position: number) => {
    if (disabled) return;
    const next = selectedTokens.filter((_, index) => index !== position);
    setSelectedTokens(next);
    onAnswer(next.map(item => tokens[item]).join(' '));
  };
  const clearTokens = () => { setSelectedTokens([]); onAnswer(''); };

  const addConversationReply = () => {
    const reply = conversationDraft.trim();
    if (!reply) return;
    const next = [...conversationReplies, reply];
    setConversationReplies(next);
    setConversationDraft('');
    if (next.length >= turns.length) onAnswer(next.join('\n'));
    else setConversationStep(next.length);
  };
  const resetConversation = () => {
    setConversationStep(0);
    setConversationDraft('');
    setConversationReplies([]);
    onAnswer('');
  };

  if (kind === 'analogy') return (
    <div className="exercise-analogy">
      <div className="analogy-bridge">
        <div><small>{tr(lang, 'ЗНАКОМАЯ МОДЕЛЬ', 'BEKANNTES MODELL', 'KNOWN MODEL')}</small><strong>{exercise.analogy_source}</strong></div>
        <FaExchangeAlt aria-hidden="true" />
        <div><small>{tr(lang, 'НОВАЯ СИТУАЦИЯ', 'NEUE SITUATION', 'NEW SITUATION')}</small><strong>{exercise.analogy_target}</strong></div>
      </div>
      <p>{exercise.pattern_label || tr(lang, 'Сохрани структуру, но измени смысл под ситуацию.', 'Behalte das Muster und passe die Bedeutung an.', 'Keep the pattern and adapt the meaning.')}</p>
      <div className="exercise-choice" role="radiogroup">
        {(exercise.options || []).map((option) => {
          const active = answer === option;
          return <button type="button" role="radio" aria-checked={active} key={option} disabled={disabled} className={active ? 'active' : ''} onClick={() => onAnswer(option)}>
            <span className="option-dot">{active && <FaCheck />}</span><span>{option}</span>
          </button>;
        })}
      </div>
    </div>
  );

  if (kind === 'choice' || kind === 'listen_choice') return (
    <div className="exercise-choice" role="radiogroup">
      {(exercise.options || []).map((option) => {
        const active = answer === option;
        return <button type="button" role="radio" aria-checked={active} key={option} disabled={disabled} className={active ? 'active' : ''} onClick={() => onAnswer(option)}>
          <span className="option-dot">{active && <FaCheck />}</span><span>{option}</span>
        </button>;
      })}
    </div>
  );

  if (kind === 'reorder') return (
    <div className="exercise-reorder">
      <div className={`reorder-built${selectedTokens.length ? '' : ' empty'}`} aria-live="polite">
        {selectedTokens.length ? selectedTokens.map((tokenIndex, position) => <button type="button" key={`${tokenIndex}-${position}`} disabled={disabled} onClick={() => undoToken(position)}>{tokens[tokenIndex]} <FaTimes /></button>) : <span>{tr(lang, 'Нажимай слова в правильном порядке', 'Tippe die Wörter in der richtigen Reihenfolge an', 'Tap the words in the correct order')}</span>}
      </div>
      <div className="reorder-bank">{tokens.map((token, index) => <button type="button" key={`${token}-${index}`} disabled={disabled || selectedTokens.includes(index)} onClick={() => chooseToken(token, index)}>{token}</button>)}</div>
      {selectedTokens.length > 0 && !disabled && <button type="button" className="reorder-clear" onClick={clearTokens}><FaUndo /> {tr(lang, 'Начать заново', 'Neu beginnen', 'Start again')}</button>}
    </div>
  );

  if (kind === 'write' && turns.length > 0) return (
    <div className="exercise-conversation" aria-label={tr(lang, 'Разговор', 'Gespräch', 'Conversation')}>
      <div className="conversation-progress"><span>{tr(lang, 'МИНИ-ДИАЛОГ', 'MINI-DIALOG', 'MINI DIALOGUE')}</span><b>{Math.min(conversationReplies.length + 1, turns.length)}/{turns.length}</b></div>
      <div className="conversation-thread" aria-live="polite">
        {turns.map((turn, index) => index <= conversationStep ? <React.Fragment key={`${turn.partner}-${index}`}>
          <div className="conversation-bubble partner"><small>{tr(lang, 'СОБЕСЕДНИК', 'GESPRÄCHSPARTNER', 'PARTNER')}</small><p>{turn.partner}</p></div>
          {conversationReplies[index] && <div className="conversation-bubble learner"><small>{tr(lang, 'ТЫ', 'DU', 'YOU')}</small><p>{conversationReplies[index]}</p></div>}
        </React.Fragment> : null)}
      </div>
      {!disabled && conversationReplies.length < turns.length && <div className="conversation-compose">
        <small>{turns[conversationStep]?.goal}</small>
        <textarea rows={2} value={conversationDraft} onChange={event => setConversationDraft(event.target.value)} placeholder={turns[conversationStep]?.placeholder || tr(lang, 'Ответь по-немецки…', 'Antworte auf Deutsch…', 'Reply in German…')} />
        <button type="button" onClick={addConversationReply} disabled={!conversationDraft.trim()}>{conversationStep + 1 === turns.length ? tr(lang, 'Завершить диалог', 'Dialog abschließen', 'Finish dialogue') : tr(lang, 'Отправить ответ', 'Antwort senden', 'Send reply')} <FaArrowRight /></button>
      </div>}
      {!disabled && conversationReplies.length === turns.length && <div className="conversation-ready"><FaCheck /><span>{tr(lang, 'Диалог готов к проверке', 'Dialog ist bereit zur Prüfung', 'Dialogue ready to check')}</span><button type="button" onClick={resetConversation}><FaRedo /> {tr(lang, 'Начать заново', 'Neu beginnen', 'Restart')}</button></div>}
    </div>
  );

  if (kind === 'write') return (
    <label className="exercise-text-answer">
      <span>{tr(lang, 'Одна короткая фраза', 'Ein kurzer Satz', 'One short sentence')}</span>
      <textarea rows={3} value={answer} disabled={disabled} onChange={event => onAnswer(event.target.value)} placeholder={tr(lang, 'Напиши по-немецки…', 'Schreibe auf Deutsch…', 'Write in German…')} />
      {!disabled && onAudio && <VoiceRecorder compact lang={lang} onAudio={onAudio} />}
    </label>
  );

  if (kind === 'speak') return (
    <div className="exercise-speak">
      <FaMicrophone />
      <strong>{tr(lang, 'Прочитай вслух', 'Lies laut vor', 'Read aloud')}</strong>
      <span>{exercise.audio_text || exercise.model_answer || exercise.answer}</span>
      {!disabled && onAudio && <VoiceRecorder lang={lang} onAudio={onAudio} />}
      {!disabled && <details className="speak-fallback"><summary>{tr(lang, 'Не работает микрофон?', 'Mikrofon funktioniert nicht?', 'Microphone not working?')}</summary><label><small>{tr(lang, 'Напиши фразу', 'Satz schreiben', 'Type the sentence')}</small><input value={answer} onChange={event => onAnswer(event.target.value)} /></label></details>}
    </div>
  );

  return (
    <label className="exercise-short-answer">
      <span>{kind === 'repair' ? tr(lang, 'Исправленный вариант', 'Korrigierte Fassung', 'Corrected version') : tr(lang, 'Твой ответ', 'Deine Antwort', 'Your answer')}</span>
      <input value={answer} disabled={disabled} onChange={event => onAnswer(event.target.value)} placeholder={kind === 'repair' ? tr(lang, 'Исправь только ошибку…', 'Korrigiere den Fehler…', 'Correct the error…') : tr(lang, 'Короткий ответ…', 'Kurze Antwort…', 'Short answer…')} />
    </label>
  );
};
