import React, { useEffect, useMemo, useState } from 'react';
import { FaCheck, FaMicrophone, FaTimes, FaUndo } from 'react-icons/fa';
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
  const tokens = useMemo(() => Array.isArray(exercise.tokens) ? exercise.tokens : [], [exercise.tokens]);

  useEffect(() => { setSelectedTokens([]); }, [exercise.id, exercise.question]);

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
