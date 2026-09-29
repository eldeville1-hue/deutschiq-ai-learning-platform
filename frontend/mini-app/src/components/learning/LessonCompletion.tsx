import React from 'react';
import { FaArrowRight, FaCheck, FaRedo } from 'react-icons/fa';
import type { AppLanguage } from '../../i18n/language';
import { tr } from '../../i18n/language';

export type LessonCompletionState = 'idle' | 'saving' | 'ready' | 'error';

export type LessonOutcome = {
  passed?: boolean;
  first_try_correct?: number;
  corrected_retries?: number;
  needs_review?: number;
  exercise_count?: number;
  score?: number;
  mastery?: number;
  xp_gained?: number;
  mission_attempted?: boolean;
  mission_passed?: boolean;
  mission_score?: number | null;
  mission_answer?: string | null;
  mission_prompt?: string | null;
  mission_model?: string | null;
  review_in_days?: number | null;
  review_at?: string | null;
  unlocked_level?: string | null;
};

type Content = {
  can_do?: string;
  objective?: string;
  mission?: string;
  success_evidence?: string;
  checkpoint?: boolean;
  module_title?: string;
};

type Props = {
  lang: AppLanguage;
  state: LessonCompletionState;
  outcome: LessonOutcome | null;
  content: Content;
  skillTitle: string;
  milestoneSent: boolean;
  onRetrySave: () => void;
  onFinish: () => void;
  onBackToPlan: () => void;
  onRate: (rating: string) => void;
};

export const LessonCompletion: React.FC<Props> = ({
  lang, state, outcome, content, skillTitle, milestoneSent,
  onRetrySave, onFinish, onBackToPlan, onRate,
}) => {
  if (state === 'saving' || state === 'idle') return (
    <section className="lesson-step lesson-result lesson-result-loading" aria-live="polite">
      <span className="result-loader" />
      <p className="eyebrow">{tr(lang, 'СОХРАНЯЕМ НАВЫК', 'FÄHIGKEIT WIRD GESPEICHERT', 'SAVING YOUR SKILL')}</p>
      <h1>{tr(lang, 'Собираем итог твоей миссии…', 'Dein Missionsergebnis wird vorbereitet…', 'Preparing your mission result…')}</h1>
    </section>
  );

  if (state === 'error') return (
    <section className="lesson-step lesson-result lesson-result-error" role="alert">
      <span className="result-orbit retry"><i><FaRedo /></i></span>
      <p className="eyebrow">{tr(lang, 'ПРОГРЕСС НЕ ПОТЕРЯН', 'DEIN FORTSCHRITT IST SICHER', 'YOUR WORK IS STILL HERE')}</p>
      <h1>{tr(lang, 'Не удалось сохранить результат', 'Das Ergebnis konnte nicht gespeichert werden', 'We couldn’t save the result')}</h1>
      <p>{tr(lang, 'Проверь соединение и попробуй ещё раз.', 'Prüfe deine Verbindung und versuche es erneut.', 'Check your connection and try once more.')}</p>
      <button className="primary-action" onClick={onRetrySave}>{tr(lang, 'Сохранить ещё раз', 'Erneut speichern', 'Save again')} <FaArrowRight /></button>
    </section>
  );

  const result = outcome || {};
  const passed = result.passed !== false;
  const evidence = {
    firstTry: Number(result.first_try_correct || 0),
    corrected: Number(result.corrected_retries || 0),
    review: Number(result.needs_review || 0),
    exercises: Number(result.exercise_count || 0),
    score: Number(result.score || 0),
    mastery: Number(result.mastery || 0),
    xp: Number(result.xp_gained || 0),
  };
  const missionAnswer = String(result.mission_answer || '').trim();
  const missionModel = String(result.mission_model || '').trim();
  const reviewDate = result.review_at ? new Date(result.review_at) : null;
  const reviewLabel = reviewDate && !Number.isNaN(reviewDate.getTime())
    ? new Intl.DateTimeFormat(lang === 'ru' ? 'ru-RU' : lang === 'de' ? 'de-DE' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short' }).format(reviewDate)
    : result.review_in_days === 1
      ? tr(lang, 'Завтра', 'Morgen', 'Tomorrow')
      : tr(lang, `Через ${result.review_in_days || 1} дн.`, `In ${result.review_in_days || 1} Tagen`, `In ${result.review_in_days || 1} days`);

  return (
    <section className={`lesson-step lesson-result dq-lesson-result mission-result mission-result-${passed ? 'success' : 'retry'}`}>
      <div className="dq-result-glow" aria-hidden="true"><i /><i /><i /></div>
      <header className="mission-result-hero">
        <span className={`result-orbit ${passed ? 'success' : 'retry'}`}><i>{passed ? <FaCheck /> : <FaRedo />}</i></span>
        <p className="eyebrow">{passed
          ? tr(lang, 'МИССИЯ ВЫПОЛНЕНА', 'MISSION GESCHAFFT', 'MISSION COMPLETE')
          : tr(lang, 'ЕЩЁ ОДНА ПОПЫТКА', 'NOCH EIN VERSUCH', 'ONE MORE TRY')}</p>
        <h1>{passed
          ? tr(lang, 'Это уже твой немецкий', 'Das ist jetzt dein Deutsch', 'This is your German now')
          : tr(lang, 'Навык почти готов', 'Die Fähigkeit ist fast da', 'The skill is almost there')}</h1>
        <p>{passed
          ? (content.success_evidence || content.can_do || content.objective || skillTitle)
          : tr(lang, 'Повторим только финальную ситуацию — без лишних карточек.', 'Wir wiederholen nur die letzte Situation – ohne unnötige Karten.', 'We’ll repeat only the final situation—without extra cards.')}</p>
        {evidence.xp > 0 && <span className="mission-xp">+{evidence.xp} XP</span>}
      </header>

      <article className={`mission-proof ${passed ? 'demonstrated' : 'needs-work'}`}>
        <header><small>{passed
          ? tr(lang, 'ТВОЙ ОТВЕТ', 'DEINE ANTWORT', 'YOUR ANSWER')
          : tr(lang, 'ФИНАЛЬНАЯ МИССИЯ', 'ABSCHLUSSMISSION', 'FINAL MISSION')}</small>
          {result.mission_score != null && <b>{result.mission_score}%</b>}
        </header>
        <blockquote>{missionAnswer || result.mission_prompt || content.mission || skillTitle}</blockquote>
        {!passed && missionModel && <details><summary>{tr(lang, 'Показать модель', 'Modell anzeigen', 'Show model')}</summary><p>{missionModel}</p></details>}
      </article>

      <div className="mission-next">
        <span><small>{passed
          ? tr(lang, 'ПОВТОРЕНИЕ', 'WIEDERHOLUNG', 'REVIEW')
          : tr(lang, 'СЛЕДУЮЩИЙ ШАГ', 'NÄCHSTER SCHRITT', 'NEXT STEP')}</small>
          <strong>{passed
            ? `${reviewLabel} · ${tr(lang, '2 минуты', '2 Minuten', '2 minutes')}`
            : tr(lang, 'Повтори разговор с подсказкой', 'Wiederhole das Gespräch mit Hilfe', 'Repeat the dialogue with support')}</strong></span>
        <FaArrowRight />
      </div>

      {content.checkpoint && passed && <div className="module-checkpoint-complete"><small>{tr(lang, 'МОДУЛЬ ЗАВЕРШЁН', 'MODUL ABGESCHLOSSEN', 'MODULE COMPLETE')}</small><strong>{content.module_title}</strong><span>{tr(lang, 'Ты можешь провести короткий первый разговор.', 'Du kannst jetzt ein kurzes erstes Gespräch führen.', 'You can now have a short first conversation.')}</span></div>}
      {result.unlocked_level && <div className="level-unlocked"><small>{tr(lang, 'НОВЫЙ УРОВЕНЬ', 'NEUES NIVEAU', 'NEW LEVEL')}</small><strong>{result.unlocked_level}</strong><span>{tr(lang, 'Твой следующий маршрут открыт.', 'Dein nächster Lernweg ist jetzt offen.', 'Your next learning path is now open.')}</span></div>}

      <details className="lesson-result-details"><summary>{tr(lang, 'Как прошёл урок', 'Lektionsdetails', 'Lesson details')}</summary><div><span>{tr(lang, 'С первой попытки', 'Beim ersten Versuch', 'First try')} <b>{evidence.firstTry}/{evidence.exercises}</b></span><span>{tr(lang, 'Исправлено', 'Korrigiert', 'Corrected')} <b>{evidence.corrected}</b></span><span>{tr(lang, 'Освоение', 'Beherrschung', 'Mastery')} <b>{evidence.mastery}%</b></span></div></details>

      <div className="lesson-result-actions">
        <button className="primary-action" onClick={onFinish}>{passed
          ? tr(lang, 'Продолжить маршрут', 'Lernweg fortsetzen', 'Continue my path')
          : tr(lang, 'Повторить финальную миссию', 'Mission erneut versuchen', 'Retry final mission')} <FaArrowRight /></button>
        {!passed && <button type="button" className="lesson-result-secondary" onClick={onBackToPlan}>{tr(lang, 'Вернуться к плану', 'Zurück zum Lernplan', 'Back to plan')}</button>}
      </div>

      {!milestoneSent && <details className="beta-milestone compact"><summary>{tr(lang, 'Оценить урок', 'Lektion bewerten', 'Rate lesson')}</summary><div><button onClick={() => onRate('hard')}>{tr(lang, 'Сложно', 'Schwer', 'Hard')}</button><button onClick={() => onRate('good')}>{tr(lang, 'Хорошо', 'Gut', 'Good')}</button><button onClick={() => onRate('easy')}>{tr(lang, 'Легко', 'Leicht', 'Easy')}</button></div></details>}
    </section>
  );
};
