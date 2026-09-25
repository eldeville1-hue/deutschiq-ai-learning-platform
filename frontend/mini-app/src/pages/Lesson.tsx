import React, { useEffect, useMemo, useRef, useState } from "react";
import { FaArrowRight, FaCheck, FaTimes, FaVolumeUp } from "react-icons/fa";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";
import { topicLabel } from "../i18n/topics";
import { getUserId, withUser } from "../utils/user";
import { ExerciseInteraction } from "../components/learning/ExerciseInteraction";
import { exerciseKind } from "../learning/exercises";
import { tr } from "../i18n/language";

export const cleanTitle = (value: string) => value.replace(/^(?:tag|day|день)\s*\d+\s*[:·—-]\s*/i, "").trim();

export const Lesson: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const draftKey = `deutschiq-lesson-draft-${getUserId()}-${id}`;
  const readDraft = () => {
    try { return JSON.parse(localStorage.getItem(draftKey) || 'null'); } catch { return null; }
  };
  const initialDraft = useRef<any>(readDraft());
  const [lesson, setLesson] = useState<any>(null);
  const [step, setStep] = useState(() => Number(initialDraft.current?.step || 0));
  const [answer, setAnswer] = useState(() => String(initialDraft.current?.answer || ""));
  const [checked, setChecked] = useState<boolean | null>(null);
  const [feedback, setFeedback] = useState<any>(null);
  const [confidence, setConfidence] = useState<"guess" | "okay" | "sure">(initialDraft.current?.confidence || "okay");
  const [startedAt, setStartedAt] = useState(() => Date.now());
  const [retried, setRetried] = useState<Record<number, boolean>>({});
  const [retryExercises, setRetryExercises] = useState<Record<number, any>>({});
  const [outcome, setOutcome] = useState<any>(null);
  const [sessionId, setSessionId] = useState("");
  const [speechResult, setSpeechResult] = useState<any>(null);
  const [checking, setChecking] = useState(false);
  const [checkError, setCheckError] = useState('');
  const [milestoneSent, setMilestoneSent] = useState(() => localStorage.getItem(`deutschiq-beta-milestone-${getUserId()}`) === '1');
  const [showHint, setShowHint] = useState(false);
  const completedRef = useRef(false);
  const openedAtRef = useRef(Date.now());
  const stepRef = useRef(0);
  const exercises = useMemo(
    () => (lesson?.content?.exercises || []).slice(0, 5),
    [lesson],
  );
  const introSteps = 2;
  const total = introSteps + exercises.length;
  const exerciseIndex = step - introSteps;
  const exercise = exercises[exerciseIndex];
  const activeExercise = retried[exerciseIndex] && retryExercises[exerciseIndex] ? retryExercises[exerciseIndex] : exercise;
  const activityLabel = activeExercise ? ({
    choice: tr(lang, "Выбери", "Wähle", "Choose"),
    analogy: tr(lang, "Перенеси", "Übertrage", "Transfer"),
    cloze: tr(lang, "Допиши", "Ergänze", "Complete"),
    reorder: tr(lang, "Собери", "Ordne", "Build"),
    repair: tr(lang, "Исправь", "Korrigiere", "Fix"),
    listen_choice: tr(lang, "Послушай", "Höre", "Listen"),
    speak: tr(lang, "Скажи", "Sprich", "Speak"),
    write: tr(lang, "Напиши", "Schreibe", "Write"),
  } as const)[exerciseKind(activeExercise)] : "";
  useEffect(() => {
    Promise.all([
      api.getLesson(Number(id), lang),
      api.startLesson({ user_id: getUserId(), lesson_id: Number(id) }),
    ])
      .then(([lessonData, session]) => {
        setLesson(lessonData);
        setSessionId(session.session_id);
        void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_started', properties: { lesson_id: Number(id), topic: lessonData.topic } });
        if (initialDraft.current) {
          void api.trackEvent({ user_id: getUserId(), event_name: 'draft_restored', properties: { lesson_id: Number(id), step: Number(initialDraft.current.step || 0) } });
          initialDraft.current = null;
        }
      })
      .catch(() => setLesson(false));
  }, [id, lang]);
  useEffect(() => {
    if (!lesson || step >= total) return;
    try { localStorage.setItem(draftKey, JSON.stringify({ step, answer, confidence, savedAt: Date.now() })); } catch { /* Recovery is best-effort. */ }
  }, [answer, confidence, draftKey, lesson, step, total]);
  useEffect(() => {
    if (!lesson || !sessionId) return;
    const stage = step === 0 ? 'learn' : step === 1 ? 'model' : step >= total ? 'result' : exercises[step - introSteps]?.stage || 'practice';
    void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_stage_viewed', properties: { lesson_id: Number(id), stage, step } });
  }, [exercises, id, lesson, sessionId, step, total]);
  useEffect(() => { stepRef.current = step; }, [step]);
  useEffect(() => () => {
    if (!sessionId || completedRef.current) return;
    void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_abandoned', properties: { lesson_id: Number(id), step: stepRef.current, duration_seconds: Math.round((Date.now() - openedAtRef.current) / 1000) } });
  }, [id, sessionId]);
  useEffect(() => {
    if (!lesson) return;
    const context = {
      lesson_id: Number(id),
      exercise_index: exerciseIndex >= 0 && exercise ? exerciseIndex : undefined,
      exercise_type: exercise?.type,
      topic: String(lesson.topic || '').slice(0, 100),
    };
    try { sessionStorage.setItem('deutschiq-beta-context', JSON.stringify(context)); } catch { /* Feedback still works without context. */ }
    return () => { try { sessionStorage.removeItem('deutschiq-beta-context'); } catch { /* Ignore unavailable storage. */ } };
  }, [exercise, exerciseIndex, id, lesson]);
  if (lesson === null)
    return (
      <div className="app-shell">
        <div className="skeleton hero-skeleton" />
      </div>
    );
  if (!lesson)
    return (
      <div className="app-shell empty-state">
        {tr(lang, "Урок не найден", "Lektion nicht gefunden", "Lesson not found")}
      </div>
    );
  const content = lesson.content || {};
  const learningProfile = lesson.learning_profile || { mode: 'balanced', mastery: 0, show_guided_hint: false };
  const resetAnswer = () => {
    setAnswer("");
    setChecked(null);
    setFeedback(null);
    setConfidence("okay");
    setStartedAt(Date.now());
    setSpeechResult(null);
    setCheckError('');
    setShowHint(false);
  };
  const next = async () => {
    if (exercise && checked === false && !retried[exerciseIndex]) {
      void api.trackEvent({ user_id: getUserId(), event_name: 'exercise_retried', properties: { lesson_id: Number(id), exercise_index: exerciseIndex } });
      setRetried((value) => ({ ...value, [exerciseIndex]: true }));
      if (feedback?.retry_exercise) setRetryExercises((value) => ({ ...value, [exerciseIndex]: feedback.retry_exercise }));
      resetAnswer();
      return;
    }
    const nextStep = Math.min(step + 1, total);
    setStep(nextStep);
    resetAnswer();
    if (nextStep >= total) {
      const result = await api
        .completeLesson({
          user_id: getUserId(),
          lesson_id: Number(id),
          session_id: sessionId,
        })
        .catch(() => null);
      setOutcome(result);
      if (result) {
        completedRef.current = true;
        try { localStorage.removeItem(draftKey); } catch { /* Ignore unavailable storage. */ }
        void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_completed', properties: { lesson_id: Number(id), passed: Boolean(result.passed), score: Number(result.score || 0) } });
        void api.trackEvent({ user_id: getUserId(), event_name: 'session_finished', properties: { lesson_id: Number(id), duration_seconds: Number(result.duration_seconds || 0), corrected_retries: Number(result.corrected_retries || 0), needs_review: Number(result.needs_review || 0) } });
        if (result.unlocked_level) void api.trackEvent({ user_id: getUserId(), event_name: 'level_unlocked', properties: { level: String(result.unlocked_level) } });
      }
    }
  };
  const check = async () => {
    if (!answer.trim() || !sessionId || checking) return;
    setChecking(true); setCheckError('');
    try {
      const result = await api.checkLessonAnswer({ user_id: getUserId(), lesson_id: Number(id), exercise_index: exerciseIndex, answer, session_id: sessionId, language: lang, confidence, response_ms: Date.now() - startedAt, retry: Boolean(retried[exerciseIndex]) });
      setChecked(Boolean(result.correct)); setFeedback(result);
      void api.trackEvent({ user_id: getUserId(), event_name: 'exercise_answered', properties: { lesson_id: Number(id), exercise_index: exerciseIndex, correct: Boolean(result.correct), confidence, misconception: String(result.error_type || ''), learning_mode: String(learningProfile.mode) } });
    } catch {
      setCheckError(tr(lang, 'Не удалось проверить. Попробуй ещё раз.', 'Prüfung fehlgeschlagen. Versuche es erneut.', 'Could not check your answer. Try again.'));
    } finally { setChecking(false); }
  };
  const finish = () =>
    navigate(withUser(outcome?.passed ? "/plan" : `/lesson/${id}`), {
      replace: true,
    });
  const sendMilestone = (rating: string) => {
    void api.submitBetaFeedback({ user_id: getUserId(), message: `First lesson rating: ${rating}`, language: lang, page: 'lesson_complete' });
    localStorage.setItem(`deutschiq-beta-milestone-${getUserId()}`, '1');
    setMilestoneSent(true);
  };
  const speak = (rate = 0.9, text?: string) => {
    if (!text && content.audio_url) {
      const audio = new Audio(content.audio_url);
      audio.playbackRate = rate;
      void audio.play();
      return;
    }
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(
      text || content.audio_text || content.examples?.[0] || "",
    );
    utterance.lang = "de-DE";
    utterance.rate = rate;
    window.speechSynthesis.speak(utterance);
  };
  const transcribe = async (audio: Blob) => {
    const result = await api.transcribeSpeech({
      user_id: getUserId(), lesson_id: Number(id), exercise_index: exerciseIndex,
      session_id: sessionId, audio,
    });
    setAnswer(result.transcript || "");
    setSpeechResult(result);
  };
  return (
    <main className={`lesson-flow precision-lesson rc-lesson fade-up level-${String(lesson.level || 'a1').toLowerCase()}`}>
      <header>
        <span>
          {Math.min(step + 1, total)} {tr(lang, "из", "von", "of")} {total}
        </span>
        <div className="progress-bar">
          <div
            className="progress-bar-fill"
            style={{ width: `${Math.min(((step + 1) / total) * 100, 100)}%` }}
          />
        </div>
      </header>
      {content.module_title && step < total && <div className="lesson-module-strip">
        <div><small>{tr(lang, "МОДУЛЬ", "MODUL", "MODULE")}</small><strong>{content.module_title}</strong></div>
        <span>{content.module_step}/{content.module_size}</span>
      </div>}
      {step === 0 && <div className={`lesson-coach-mode ${learningProfile.mode}`}>
        <span>{tr(lang, "РЕЖИМ УРОКА", "LEKTIONSMODUS", "LESSON MODE")}</span>
        <strong>{learningProfile.mode === 'supported'
          ? tr(lang, "С поддержкой", "Mit Unterstützung", "Supported")
          : learningProfile.mode === 'challenge'
            ? tr(lang, "Самостоятельный вызов", "Selbstständige Herausforderung", "Independent challenge")
            : tr(lang, "Сбалансированный", "Ausgewogen", "Balanced")}</strong>
        <small>{tr(lang, `До урока: ${learningProfile.mastery}%`, `Vor der Lektion: ${learningProfile.mastery}%`, `Before lesson: ${learningProfile.mastery}%`)}</small>
      </div>}
      {step === 0 && (
        <section className="lesson-step">
          <p className="eyebrow">
            {tr(lang, "НОВЫЙ НАВЫК", "NEUES LERNZIEL", "NEW SKILL")} ·{" "}
            {content.cefr || lesson.level}
          </p>
          <h1>{cleanTitle(topicLabel(content.title || lesson.topic, lang))}</h1>
          <div className="lesson-can-do"><small>{tr(lang, "ПОСЛЕ УРОКА", "NACH DER LEKTION", "AFTER THIS LESSON")}</small><strong>{content.can_do || content.objective}</strong></div>
          {content.scenario && <div className="lesson-scenario"><small>{tr(lang, 'СИТУАЦИЯ', 'SITUATION', 'SCENARIO')}</small><span>{content.scenario}</span></div>}
          {content.assessment_rubric?.length > 0 && <div className="lesson-rubric"><small>{tr(lang, 'КРИТЕРИИ ОТВЕТА', 'ANTWORTKRITERIEN', 'RESPONSE CRITERIA')}</small><ul>{content.assessment_rubric.map((criterion: string) => <li key={criterion}>{criterion}</li>)}</ul></div>}
          <div className="rule-card">{content.rule}</div>
          {content.module_size === 5 && <div className="lesson-practice-path" aria-label={tr(lang, 'Путь урока', 'Lektionsweg', 'Lesson path')}>
            {[tr(lang, 'Понять', 'Verstehen', 'Understand'), tr(lang, 'Выбрать', 'Wählen', 'Choose'), tr(lang, 'Собрать', 'Bauen', 'Build'), tr(lang, 'Сказать', 'Sprechen', 'Speak')].map((label, index) => <span key={label}><i>{index + 1}</i>{label}</span>)}
          </div>}
          <button className="primary-action" onClick={next}>
            {tr(lang, "Показать пример", "Beispiel zeigen", "Show example")}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {step === 1 && (
        <section className="lesson-step">
          <p className="eyebrow">
            {tr(lang, "ПРИМЕР", "BEISPIEL", "EXAMPLE")}
          </p>
          <h1>
            {tr(lang, "Послушай фразу", "Höre den Satz", "Listen to the sentence")}
          </h1>
          <div className="example-sentence">
            {content.examples?.[0] || "Heute lerne ich Deutsch."}
          </div>
          <div className="audio-controls">
            <button type="button" onClick={() => speak(0.9)}>
              <FaVolumeUp /> {tr(lang, "Обычно", "Normal", "Normal")}
            </button>
            <button type="button" onClick={() => speak(0.65)}>
              <FaVolumeUp /> {tr(lang, "Медленно", "Langsam", "Slow")}
            </button>
          </div>
          {(content.common_mistakes || []).length > 0 && (
            <div className="mistake-contrast compact">
              {(content.common_mistakes || []).slice(0, 2).map((item: string, index: number) => (
                <div key={index} className={item.includes("❌") ? "bad" : "good"}>{item.includes("❌") ? <FaTimes /> : <FaCheck />}<span>{item.replace(/^[❌✅]\s*/, '')}</span></div>
              ))}
            </div>
          )}
          <button className="primary-action" onClick={next}>
            {tr(lang, "Начать практику", "Übung starten", "Start practice")}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {activeExercise && (
        <section className="lesson-step exercise-step">
          <div className="exercise-stage-row"><p className="eyebrow">{activityLabel}{retried[exerciseIndex] ? tr(lang, " · ещё раз", " · noch einmal", " · try again") : ""}</p><span>{exerciseIndex + 1}/{exercises.length}</span></div>
          <div className="exercise-prompt"><h1>{activeExercise.type === "repeat" ? tr(lang, "Произнеси фразу", "Sprich den Satz", "Say the sentence") : activeExercise.question}</h1></div>
          {(activeExercise.type === "listening" || activeExercise.type === "listening_choice") && (
            <div className="listening-challenge simple">
              <button type="button" className="listen-main" onClick={() => speak(0.9, activeExercise.audio_text)}><FaVolumeUp /> {tr(lang, "Слушать", "Anhören", "Listen")}</button>
              <button type="button" className="listen-slow" onClick={() => speak(0.7, activeExercise.audio_text)}>{tr(lang, "Медленно", "Langsam", "Slow")}</button>
            </div>
          )}
          <ExerciseInteraction exercise={{ ...activeExercise, id: `${id}-${exerciseIndex}-${retried[exerciseIndex] ? 'retry' : 'first'}` }} answer={answer} onAnswer={setAnswer} disabled={checked !== null} lang={lang} onAudio={sessionId ? transcribe : undefined} />
            {speechResult?.transcript && (
              <div className="speech-result">
                <small>{tr(lang, "РАСПОЗНАНО", "ERKANNT", "RECOGNISED")}</small>
                <strong>“{speechResult.transcript}”</strong>
                {speechResult.match && <span>{tr(lang, `Совпадение слов: ${speechResult.match.score}%`, `Wortübereinstimmung: ${speechResult.match.score}%`, `Word match: ${speechResult.match.score}%`)}</span>}
                <em>{tr(lang, "Это оценка распознанных слов, не акцента или фонетики.", "Bewertet werden erkannte Wörter, nicht Akzent oder Phonetik.", "This measures recognised words, not accent or phonetics.")}</em>
              </div>
            )}
          {checked === null && activeExercise.stage === "guided" && (learningProfile.show_guided_hint || showHint || retried[exerciseIndex]) && (
            <div className="guided-hint">{activeExercise.hint}</div>
          )}
          {checked === null && activeExercise.stage === "guided" && !retried[exerciseIndex] && !learningProfile.show_guided_hint && !showHint && (
            <button type="button" className="lesson-hint-toggle" onClick={() => setShowHint(true)}>
              {tr(lang, "Показать подсказку", "Hinweis anzeigen", "Show hint")}
            </button>
          )}
          {checked === null ? (
            <button className="primary-action" onClick={check} disabled={!answer.trim() || !sessionId || checking}>
              {checking ? tr(lang, 'Проверяем…', 'Wird geprüft…', 'Checking…') : tr(lang, "Проверить", "Prüfen", "Check")}
            </button>
          ) : (
            <div className={`answer-feedback ${checked ? "correct" : "wrong"}`}>
              {checked ? <FaCheck /> : <FaTimes />}
              <div>
                <b>
                  {checked
                    ? tr(lang, "Верно", "Richtig", "Correct")
                    : tr(lang, "Попробуй ещё раз", "Noch einmal", "Try again")}
                </b>
                {checked && <p>{feedback?.explanation}</p>}
                {!checked && feedback?.correct_answer && (
                  <div className="corrected-model">
                    <small>{tr(lang, 'ПРАВИЛЬНАЯ МОДЕЛЬ', 'RICHTIGES MODELL', 'CORRECT MODEL')}</small>
                    <strong>{feedback.correct_answer}</strong>
                  </div>
                )}
                {!checked && feedback?.error_type && <details className="error-diagnosis"><summary>{tr(lang, 'Почему?', 'Warum?', 'Why?')}</summary>
                  {Array.isArray(feedback.contrast) && feedback.contrast.map((line: string, index: number) => <p key={index}>{line}</p>)}
                  <em>{feedback.retry_instruction || tr(lang, 'Сначала назови правило, затем составь ответ заново.', 'Nenne zuerst die Regel und bilde die Antwort dann neu.', 'State the rule first, then build the answer again.')}</em>
                  {Array.isArray(feedback.repair_steps) && feedback.repair_steps.length > 0 && <ol className="repair-steps">
                    {feedback.repair_steps.map((line: string, index: number) => <li key={index}>{line}</li>)}
                  </ol>}
                </details>}
                {feedback?.production && (
                  <div className="production-assessment">
                    <header><small>{tr(lang, `${feedback.cefr_standard || ''} ОЦЕНКА`, `${feedback.cefr_standard || ''} BEWERTUNG`, `${feedback.cefr_standard || ''} ASSESSMENT`)}</small><strong>{feedback.production_score}%</strong><span>{tr(lang, `проходной ${feedback.pass_mark}%`, `Bestanden ab ${feedback.pass_mark}%`, `pass mark ${feedback.pass_mark}%`)}</span></header>
                    {feedback.dimension_scores && <div className="assessment-grid">{[
                      ['task_completion', tr(lang, 'Задача', 'Aufgabe', 'Task')],
                      ['grammar', tr(lang, 'Грамматика', 'Grammatik', 'Grammar')],
                      ['vocabulary', tr(lang, 'Лексика', 'Wortschatz', 'Vocabulary')],
                      ['coherence', tr(lang, 'Связность', 'Kohärenz', 'Coherence')],
                      ['register', tr(lang, 'Регистр', 'Register', 'Register')],
                    ].map(([key, label]) => <span key={key}><small>{label}</small><b>{feedback.dimension_scores[key]}%</b></span>)}</div>}
                    {feedback.improvement && <p><b>{tr(lang, 'Следующий шаг:', 'Nächster Schritt:', 'Next step:')}</b> {feedback.improvement}</p>}
                    {!checked && feedback.correct_answer && <small>{tr(lang, 'Возможный вариант:', 'Mögliche Fassung:', 'Possible revision:')} {feedback.correct_answer}</small>}
                  </div>
                )}
                {!checked && !retried[exerciseIndex] && (
                  <small>
                    {tr(lang, "Исправь ответ и попробуй снова.", "Korrigiere die Antwort und versuche es erneut.", "Correct your answer and try again.")}
                  </small>
                )}
              </div>
              <button onClick={next}>
                <span>{!checked && !retried[exerciseIndex] ? tr(lang, "Исправить", "Korrigieren", "Fix it") : tr(lang, "Дальше", "Weiter", "Next")}</span><FaArrowRight />
              </button>
            </div>
          )}
          {checkError && <div className="lesson-check-error" role="alert">{checkError}</div>}
        </section>
      )}
      {step >= total && (
        <section className="lesson-step lesson-result">
          <span
            className={`result-icon ${outcome?.passed === false ? "needs-practice" : ""}`}
          >
            {outcome?.passed === false ? <FaTimes /> : <FaCheck />}
          </span>
          <p className="eyebrow">
            {outcome?.passed === false
              ? tr(lang, "НУЖНО ЕЩЁ ЗАКРЕПИТЬ", "NOCH EINMAL FESTIGEN", "MORE PRACTICE NEEDED")
              : tr(lang, "УРОК ОСВОЕН", "LEKTION GESCHAFFT", "LESSON COMPLETE")}
          </p>
          <h1>{outcome?.passed === false ? tr(lang, 'Закрепим это ещё раз', 'Wir festigen das noch einmal', 'Let’s strengthen this once more') : (content.can_do || content.objective || tr(lang, 'Новый навык готов к использованию', 'Die neue Fähigkeit ist einsatzbereit', 'Your new skill is ready to use'))}</h1>
          <div className="lesson-proof">
            <span>
              {tr(lang, 'Задания', 'Aufgaben', 'Exercises')}
              <b>{outcome ? `${outcome.score}%` : '…'}</b>
            </span><span>
              {tr(lang, "Освоение", "Beherrschung", "Mastery")}
              <b>{outcome?.mastery || 0}%</b>
            </span>
            <span>
              {tr(lang, "Награда", "Belohnung", "Reward")}
              <b>+{outcome?.xp_gained || 0} XP</b>
            </span>
          </div>
          {outcome && <div className="lesson-result-next"><small>{tr(lang, 'ДАЛЬШЕ', 'ALS NÄCHSTES', 'NEXT')}</small><strong>{outcome.needs_review > 0 ? tr(lang, 'Закрепим ошибку в повторении', 'Den Fehler in der Wiederholung festigen', 'Review the point that needs practice') : tr(lang, 'Продолжить твой маршрут', 'Deinen Lernweg fortsetzen', 'Continue your learning path')}</strong></div>}
          {content.checkpoint && outcome?.passed !== false && <div className="module-checkpoint-complete"><small>{tr(lang, 'МОДУЛЬ ЗАВЕРШЁН', 'MODUL ABGESCHLOSSEN', 'MODULE COMPLETE')}</small><strong>{content.module_title}</strong><span>{tr(lang, 'Теперь ты можешь провести короткий первый разговор.', 'Du kannst jetzt ein kurzes erstes Gespräch führen.', 'You can now have a short first conversation.')}</span></div>}
          {outcome?.unlocked_level && <div className="level-unlocked"><small>{tr(lang, 'НОВЫЙ УРОВЕНЬ', 'NEUES NIVEAU', 'NEW LEVEL')}</small><strong>{outcome.unlocked_level}</strong><span>{tr(lang, 'Твой следующий маршрут открыт.', 'Dein nächster Lernweg ist jetzt offen.', 'Your next learning path is now open.')}</span></div>}
          {outcome && !milestoneSent && <details className="beta-milestone compact"><summary>{tr(lang,'Оценить урок','Lektion bewerten','Rate lesson')}</summary><div><button onClick={()=>sendMilestone('hard')}>{tr(lang,'Сложно','Schwer','Hard')}</button><button onClick={()=>sendMilestone('good')}>{tr(lang,'Хорошо','Gut','Good')}</button><button onClick={()=>sendMilestone('easy')}>{tr(lang,'Легко','Leicht','Easy')}</button></div></details>}
          <button className="primary-action" onClick={finish}>
            {outcome?.passed === false
              ? tr(lang, "Повторить урок", "Lektion wiederholen", "Repeat lesson")
              : tr(lang, "Вернуться к плану", "Zurück zum Lernplan", "Back to plan")}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
    </main>
  );
};
