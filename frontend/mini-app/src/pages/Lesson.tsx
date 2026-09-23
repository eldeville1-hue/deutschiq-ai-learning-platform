import React, { useEffect, useMemo, useRef, useState } from "react";
import { FaArrowRight, FaCheck, FaTimes, FaVolumeUp } from "react-icons/fa";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";
import { topicLabel } from "../i18n/topics";
import { getUserId, withUser } from "../utils/user";
import { VoiceRecorder } from "../components/VoiceRecorder";
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
  const [outcome, setOutcome] = useState<any>(null);
  const [sessionId, setSessionId] = useState("");
  const [usedTokens, setUsedTokens] = useState<number[]>(() => initialDraft.current?.usedTokens || []);
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
    try { localStorage.setItem(draftKey, JSON.stringify({ step, answer, confidence, usedTokens, savedAt: Date.now() })); } catch { /* Recovery is best-effort. */ }
  }, [answer, confidence, draftKey, lesson, step, total, usedTokens]);
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
    setUsedTokens([]);
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
      const result = await api.checkLessonAnswer({ user_id: getUserId(), lesson_id: Number(id), exercise_index: exerciseIndex, answer, session_id: sessionId, language: lang, confidence, response_ms: Date.now() - startedAt });
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
  const speak = (rate = 0.9) => {
    if (content.audio_url) {
      const audio = new Audio(content.audio_url);
      audio.playbackRate = rate;
      void audio.play();
      return;
    }
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(
      content.audio_text || content.examples?.[0] || "",
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
  const addToken = (token: string, index: number) => {
    setUsedTokens((value) => [...value, index]);
    setAnswer((value) => `${value}${value ? " " : ""}${token}`);
  };
  return (
    <main className="lesson-flow precision-lesson rc-lesson fade-up">
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
          <div className="lesson-objective">{content.objective}</div>
          {content.scenario && <div className="lesson-scenario"><small>{tr(lang, 'СИТУАЦИЯ', 'SITUATION', 'SCENARIO')}</small><span>{content.scenario}</span></div>}
          {content.assessment_rubric?.length > 0 && <div className="lesson-rubric"><small>{tr(lang, 'КРИТЕРИИ ОТВЕТА', 'ANTWORTKRITERIEN', 'RESPONSE CRITERIA')}</small><ul>{content.assessment_rubric.map((criterion: string) => <li key={criterion}>{criterion}</li>)}</ul></div>}
          <div className="rule-card">{content.rule}</div>
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
      {exercise && (
        <section className="lesson-step exercise-step">
          <div className="exercise-stage-row"><p className="eyebrow">
            {exercise.stage === "guided"
              ? tr(lang, "С ПОДСКАЗКОЙ", "MIT HILFE", "GUIDED")
              : exercise.stage === "transfer"
                ? tr(lang, "ТВОЯ ФРАЗА", "DEIN SATZ", "YOUR SENTENCE")
                : tr(lang, "САМОСТОЯТЕЛЬНО", "SELBSTSTÄNDIG", "INDEPENDENT")}
            {retried[exerciseIndex]
              ? tr(lang, " · вторая попытка", " · zweiter Versuch", " · second attempt")
              : ""}
          </p><span>{exerciseIndex + 1}/{exercises.length}</span></div>
          <div className="exercise-prompt"><small>{tr(lang, 'ЗАДАНИЕ', 'AUFGABE', 'TASK')}</small><h1>{exercise.type === "repeat" ? tr(lang, "Повтори фразу", "Sprich den Satz nach", "Repeat the sentence") : exercise.question}</h1></div>
          {exercise.type === "repeat" && <div className="example-sentence">{content.audio_text || content.examples?.[0]}</div>}
          {(exercise.type === "listening" || exercise.type === "listening_choice") && (
            <div className="listening-challenge">
              <button type="button" onClick={() => speak(0.9)}><FaVolumeUp /> {tr(lang, "Прослушать", "Anhören", "Listen")}</button>
              <button type="button" onClick={() => speak(0.7)}><FaVolumeUp /> {tr(lang, "Медленнее", "Langsamer", "Slower")}</button>
            </div>
          )}
          {Array.isArray(exercise.options) && exercise.options.length > 0 ? (
            <div className="lesson-options">
              {exercise.options.map((option: string, optionIndex: number) => (
                <button
                  key={option}
                  onClick={() => setAnswer(option)}
                  className={answer === option ? "active" : ""}
                >
                  <span className="option-letter">{String.fromCharCode(65 + optionIndex)}</span><span>{option}</span>{answer === option && <FaCheck />}
                </button>
              ))}
            </div>
          ) : exercise.type === "reorder" ? (
            <>
              <div className="reorder-answer">
                {answer ||
                  tr(lang, "Нажимай слова по порядку", "Wörter antippen", "Tap the words in order")}
              </div>
              <div className="word-tokens">
                {(exercise.tokens || []).map((token: string, index: number) => (
                  <button
                    key={`${token}-${index}`}
                    onClick={() => addToken(token, index)}
                    disabled={checked !== null || usedTokens.includes(index)}
                  >
                    {token}
                  </button>
                ))}
              </div>
              <button
                className="clear-answer"
                  onClick={() => {
                    setAnswer("");
                    setUsedTokens([]);
                  }}
                disabled={checked !== null}
              >
                {tr(lang, "Сбросить", "Löschen", "Clear")}
              </button>
            </>
          ) : (
            <>
            {exercise.type === "production" || exercise.type === "dialogue" ? <textarea
              className="lesson-answer production-answer"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder={tr(lang, "Напиши одну короткую немецкую фразу…", "Schreibe einen kurzen deutschen Satz…", "Write one short German sentence…")}
              disabled={checked !== null}
              rows={3}
            /> : <input
              className="lesson-answer compact-answer"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && answer.trim() && sessionId && !checking) void check(); }}
              placeholder={
                exercise.type === "production" || exercise.type === "dialogue"
                  ? tr(lang, "Напиши свою немецкую фразу…", "Schreibe deinen eigenen Satz…", "Write your own German sentence…")
                  : exercise.type === "listening" || exercise.type === "listening_choice"
                    ? tr(lang, "Напиши, что услышал…", "Schreibe, was du hörst…", "Type what you hear…")
                    : exercise.type === "error_repair"
                      ? tr(lang, "Напиши исправленную фразу…", "Schreibe den korrigierten Satz…", "Write the corrected sentence…")
                    : tr(lang, "Введи ответ", "Antwort eingeben", "Enter your answer")
              }
              disabled={checked !== null}
            />}
            {(exercise.type === "production" || exercise.type === "dialogue" || exercise.type === "repeat") && checked === null && (
              <VoiceRecorder lang={lang} disabled={!sessionId} onAudio={transcribe} />
            )}
            {speechResult?.transcript && (
              <div className="speech-result">
                <small>{tr(lang, "РАСПОЗНАНО", "ERKANNT", "RECOGNISED")}</small>
                <strong>“{speechResult.transcript}”</strong>
                {speechResult.match && <span>{tr(lang, `Совпадение слов: ${speechResult.match.score}%`, `Wortübereinstimmung: ${speechResult.match.score}%`, `Word match: ${speechResult.match.score}%`)}</span>}
                <em>{tr(lang, "Это оценка распознанных слов, не акцента или фонетики.", "Bewertet werden erkannte Wörter, nicht Akzent oder Phonetik.", "This measures recognised words, not accent or phonetics.")}</em>
              </div>
            )}
            </>
          )}
          {checked === null && exercise.stage === "guided" && (learningProfile.show_guided_hint || showHint) && (
            <div className="guided-hint">{exercise.hint}</div>
          )}
          {checked === null && exercise.stage === "guided" && !learningProfile.show_guided_hint && !showHint && (
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
                <p>{feedback?.explanation}</p>
                {!checked && feedback?.correct_answer && (
                  <div className="corrected-model">
                    <small>{tr(lang, 'ПРАВИЛЬНАЯ МОДЕЛЬ', 'RICHTIGES MODELL', 'CORRECT MODEL')}</small>
                    <strong>{feedback.correct_answer}</strong>
                  </div>
                )}
                {!checked && feedback?.error_type && <div className="error-diagnosis">
                  <small>{tr(lang, 'ПОДСКАЗКА', 'HINWEIS', 'TIP')}</small>
                  {Array.isArray(feedback.contrast) && feedback.contrast.map((line: string, index: number) => <p key={index}>{line}</p>)}
                  <em>{feedback.retry_instruction || tr(lang, 'Сначала назови правило, затем составь ответ заново.', 'Nenne zuerst die Regel und bilde die Antwort dann neu.', 'State the rule first, then build the answer again.')}</em>
                  {Array.isArray(feedback.repair_steps) && feedback.repair_steps.length > 0 && <ol className="repair-steps">
                    {feedback.repair_steps.map((line: string, index: number) => <li key={index}>{line}</li>)}
                  </ol>}
                </div>}
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
                <FaArrowRight />
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
          <small className="lesson-result-score-label">{tr(lang, 'РЕЗУЛЬТАТ ЗАДАНИЙ', 'ÜBUNGSERGEBNIS', 'EXERCISE SCORE')}</small>
          <h1>{outcome ? `${outcome.score}%` : "…"}</h1>
          <div className="lesson-score">
            <span>
              {tr(lang, "Освоение темы", "Themenkenntnis", "Topic mastery")}
              <b>{outcome?.mastery || 0}%</b>
            </span>
            <span>
              {tr(lang, "Получено", "Erhalten", "Earned")}
              <b>+{outcome?.xp_gained || 0} XP</b>
            </span>
          </div>
          {outcome && (
            <div className="session-summary">
              <span><b>{outcome.first_try_correct || 0}</b>{tr(lang, 'С первой попытки', 'Sofort richtig', 'Correct first try')}</span>
              <span><b>{outcome.corrected_retries || 0}</b>{tr(lang, 'Исправлено', 'Verbessert', 'Corrected')}</span>
              <span><b>{outcome.needs_review || 0}</b>{tr(lang, 'На повтор', 'Zum Wiederholen', 'To review')}</span>
            </div>
          )}
          {outcome?.unlocked_level && <div className="level-unlocked"><small>{tr(lang, 'НОВЫЙ УРОВЕНЬ', 'NEUES NIVEAU', 'NEW LEVEL')}</small><strong>{outcome.unlocked_level}</strong><span>{tr(lang, 'Твой следующий маршрут открыт.', 'Dein nächster Lernweg ist jetzt offen.', 'Your next learning path is now open.')}</span></div>}
          {outcome && !milestoneSent && <div className="beta-milestone"><small>{tr(lang,'БЫСТРЫЙ ОТЗЫВ','KURZES FEEDBACK','QUICK FEEDBACK')}</small><strong>{tr(lang,'Как прошёл первый урок?','Wie war deine erste Lektion?','How was your first lesson?')}</strong><div><button onClick={()=>sendMilestone('hard')}>{tr(lang,'Сложно','Schwer','Hard')}</button><button onClick={()=>sendMilestone('good')}>{tr(lang,'Хорошо','Gut','Good')}</button><button onClick={()=>sendMilestone('easy')}>{tr(lang,'Легко','Leicht','Easy')}</button></div></div>}
          <p>
            {outcome?.passed === false
              ? tr(lang, "Урок не завершён: повтори задания и набери 70%.", "Die Lektion bleibt offen. Wiederhole sie und erreiche 70%.", "The lesson remains open. Repeat it and reach 70%.")
              : tr(lang, "Результат рассчитан по твоим реальным ответам.", "Das Ergebnis basiert auf deinen echten Antworten.", "Your result is based on your actual answers.")}
          </p>
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
