import React, { useEffect, useMemo, useRef, useState } from "react";
import { FaArrowRight, FaCheck, FaTimes, FaVolumeUp } from "react-icons/fa";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";
import { topicLabel } from "../i18n/topics";
import { getUserId, withUser } from "../utils/user";
import { ExerciseInteraction } from "../components/learning/ExerciseInteraction";
import { LessonCompletion, type LessonOutcome } from "../components/learning/LessonCompletion";
import { exerciseKind } from "../learning/exercises";
import { tr } from "../i18n/language";
import { clearDailySession, saveDailySession } from "../learning/dailySession";
import { ProductState } from "../components/ProductState";

export const cleanTitle = (value: string) => value.replace(/^(?:tag|day|день)\s*\d+\s*[:·—-]\s*/i, "").trim();

export const Lesson: React.FC = () => {
  const { id } = useParams();
  return <LessonScreen key={id} />;
};

const LessonScreen: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const draftKey = `deutschiq-lesson-draft-${getUserId()}-${id}`;
  const readDraft = () => {
    try { return JSON.parse(localStorage.getItem(draftKey) || 'null'); } catch { return null; }
  };
  const initialDraft = useRef<any>(readDraft());
  const resumeSessionRef = useRef<string>(initialDraft.current?.sessionId || '');
  const [loadAttempt, setLoadAttempt] = useState(0);
  const [lesson, setLesson] = useState<any>(null);
  const [step, setStep] = useState(() => Number(initialDraft.current?.step || 0));
  const [answer, setAnswer] = useState(() => String(initialDraft.current?.answer || ""));
  const [checked, setChecked] = useState<boolean | null>(() => typeof initialDraft.current?.checked === 'boolean' ? initialDraft.current.checked : null);
  const [feedback, setFeedback] = useState<any>(initialDraft.current?.feedback || null);
  const [confidence, setConfidence] = useState<"guess" | "okay" | "sure">(initialDraft.current?.confidence || "okay");
  const [startedAt, setStartedAt] = useState(() => Date.now());
  const [retried, setRetried] = useState<Record<number, boolean>>(initialDraft.current?.retried || {});
  const [retryExercises, setRetryExercises] = useState<Record<number, any>>(initialDraft.current?.retryExercises || {});
  const [outcome, setOutcome] = useState<LessonOutcome | null>(null);
  const [completionState, setCompletionState] = useState<"idle" | "saving" | "ready" | "error">("idle");
  const [sessionId, setSessionId] = useState("");
  const [speechResult, setSpeechResult] = useState<any>(null);
  const [checking, setChecking] = useState(false);
  const [checkError, setCheckError] = useState('');
  const [milestoneSent, setMilestoneSent] = useState(() => localStorage.getItem(`deutschiq-beta-milestone-${getUserId()}`) === '1');
  const [showHint, setShowHint] = useState(false);
  const [easyMode, setEasyMode] = useState(false);
  const [showTranscript, setShowTranscript] = useState(false);
  const [audioState, setAudioState] = useState<'idle' | 'loading' | 'playing' | 'paused' | 'fallback'>('idle');
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const audioUrlRef = useRef('');
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
  const activityLabel = activeExercise?.mission_role === 'final'
    ? tr(lang, 'Миссия', 'Mission', 'Mission')
    : activeExercise ? ({
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
    let cancelled = false;
    setLesson(null);
    saveDailySession(getUserId(), { nextLessonId: Number(id), stage: 'lesson' });
    Promise.all([
      api.getLesson(Number(id), lang),
      api.startLesson({ user_id: getUserId(), lesson_id: Number(id), resume_session_id: resumeSessionRef.current || undefined }),
    ])
      .then(([lessonData, session]) => {
        if (cancelled) return;
        const maxExercises = Math.min(5, lessonData.content?.exercises?.length || 0);
        const serverIndex = Number(session.next_exercise_index);
        const hasServerCursor = Number.isInteger(serverIndex) && serverIndex >= 0;
        if (!session.resumed) {
          // A new server session must never inherit feedback or position from a stale draft.
          setStep(0); setAnswer(''); setChecked(null); setFeedback(null);
          setRetried({}); setRetryExercises({});
        } else if (hasServerCursor) {
          // Server attempts are authoritative; local drafts may be stale after a reload.
          const restoredStep = 2 + Math.min(serverIndex, maxExercises);
          setStep(restoredStep);
          const draftMatchesStep = Number(initialDraft.current?.step) === restoredStep;
          if (!draftMatchesStep) {
            setAnswer(''); setChecked(null); setFeedback(null);
            setRetried({}); setRetryExercises({});
          }
        } else {
          // Compatibility with older API deployments that do not return a cursor.
          setStep(value => Math.max(0, Math.min(Number.isFinite(value) ? value : 0, 2 + maxExercises)));
        }
        resumeSessionRef.current = session.session_id;
        setLesson(lessonData);
        setSessionId(session.session_id);
        if (session.resumed && hasServerCursor && serverIndex >= maxExercises) {
          // All practice answers are saved, but completion may have been interrupted.
          setCompletionState('error');
        }
        void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_started', properties: { lesson_id: Number(id), topic: lessonData.topic } });
        if (initialDraft.current) {
          void api.trackEvent({ user_id: getUserId(), event_name: 'draft_restored', properties: { lesson_id: Number(id), step: Number(initialDraft.current.step || 0) } });
          initialDraft.current = null;
        }
      })
      .catch(() => { if (!cancelled) setLesson(false); });
    return () => { cancelled = true; };
  }, [id, lang, loadAttempt]);
  useEffect(() => {
    if (!lesson || !sessionId || completionState === 'ready') return;
    try { localStorage.setItem(draftKey, JSON.stringify({ sessionId, step, answer, confidence, checked, feedback, retried, retryExercises, savedAt: Date.now() })); } catch { /* Recovery is best-effort. */ }
  }, [answer, confidence, draftKey, lesson, step, sessionId, checked, feedback, retried, retryExercises, completionState]);
  useEffect(() => {
    if (!lesson || !sessionId) return;
    const stage = step === 0 ? 'learn' : step === 1 ? 'model' : step >= total ? 'result' : exercises[step - introSteps]?.stage || 'practice';
    void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_stage_viewed', properties: { lesson_id: Number(id), stage, step } });
  }, [exercises, id, lesson, sessionId, step, total]);
  useEffect(() => { stepRef.current = step; }, [step]);
  useEffect(() => {
    const onVisibility = () => {
      const audio = audioRef.current;
      if (document.hidden && audio && !audio.paused) {
        audio.pause();
        setAudioState('paused');
        void api.trackEvent({ user_id: getUserId(), event_name: 'audio_interrupted', properties: { lesson_id: Number(id), reason: 'app_hidden' } });
      }
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      document.removeEventListener('visibilitychange', onVisibility);
      audioRef.current?.pause();
      window.speechSynthesis?.cancel();
    };
  }, [id]);
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
        <ProductState kind="error" eyebrow={tr(lang, 'УРОК', 'LEKTION', 'LESSON')}
          title={tr(lang, 'Урок не загрузился', 'Lektion konnte nicht geladen werden', 'Could not load lesson')}
          detail={tr(lang, 'Проверь соединение и попробуй снова.', 'Prüfe die Verbindung und versuche es erneut.', 'Check your connection and try again.')}
          action={tr(lang, 'Попробовать снова', 'Erneut versuchen', 'Try again')}
          onAction={() => setLoadAttempt(value => value + 1)} />
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
    setEasyMode(false);
    setShowTranscript(false);
  };
  const completeSession = async () => {
    setCompletionState("saving");
    try {
      const result = await api.completeLesson({
        user_id: getUserId(),
        lesson_id: Number(id),
        session_id: sessionId,
      });
      setOutcome(result);
      setCompletionState("ready");
      completedRef.current = true;
      if (result.passed) clearDailySession(getUserId());
      try { localStorage.removeItem(draftKey); } catch { /* Ignore unavailable storage. */ }
      void api.trackEvent({ user_id: getUserId(), event_name: 'lesson_completed', properties: { lesson_id: Number(id), passed: Boolean(result.passed), score: Number(result.score || 0) } });
      void api.trackEvent({ user_id: getUserId(), event_name: 'session_finished', properties: { lesson_id: Number(id), duration_seconds: Number(result.duration_seconds || 0), corrected_retries: Number(result.corrected_retries || 0), needs_review: Number(result.needs_review || 0) } });
      if (result.unlocked_level) void api.trackEvent({ user_id: getUserId(), event_name: 'level_unlocked', properties: { level: String(result.unlocked_level) } });
    } catch {
      setCompletionState("error");
    }
  };
  const advance = async () => {
    const nextStep = Math.min(step + 1, total);
    setStep(nextStep);
    resetAnswer();
    if (nextStep >= total) {
      await completeSession();
    }
  };
  const next = async () => {
    if (exercise && checked === false && !retried[exerciseIndex]) {
      void api.trackEvent({ user_id: getUserId(), event_name: 'exercise_retried', properties: { lesson_id: Number(id), exercise_index: exerciseIndex } });
      setRetried((value) => ({ ...value, [exerciseIndex]: true }));
      if (feedback?.retry_exercise) setRetryExercises((value) => ({ ...value, [exerciseIndex]: feedback.retry_exercise }));
      resetAnswer();
      return;
    }
    if (exercise?.mission_role === 'final' && retried[exerciseIndex]) {
      void api.trackEvent({ user_id: getUserId(), event_name: 'mission_repair_completed', properties: { lesson_id: Number(id), exercise_index: exerciseIndex, repaired: Boolean(checked) } });
      setRetried((value) => ({ ...value, [exerciseIndex]: false }));
      setRetryExercises((value) => {
        const nextValue = { ...value };
        delete nextValue[exerciseIndex];
        return nextValue;
      });
      resetAnswer();
      return;
    }
    await advance();
  };
  const skipExercise = async (reason: string) => {
    void api.trackEvent({ user_id: getUserId(), event_name: 'exercise_skipped', properties: { lesson_id: Number(id), exercise_index: exerciseIndex, exercise_type: activeExercise?.type, reason } });
    await advance();
  };
  const check = async () => {
    if (!answer.trim() || !sessionId || checking) return;
    setChecking(true); setCheckError('');
    try {
      const result = await api.checkLessonAnswer({ user_id: getUserId(), lesson_id: Number(id), exercise_index: exerciseIndex, answer, session_id: sessionId, language: lang, confidence, response_ms: Date.now() - startedAt, retry: Boolean(retried[exerciseIndex]) });
      if (result.evaluation_status === 'uncertain' || result.evaluation_status === 'needs_review') {
        // An unverified evaluation is not a wrong answer: keep the learner on
        // the same task without activating the guided-retry/penalty flow.
        setChecked(null);
        setFeedback(null);
        setCheckError(result.retry_instruction || tr(lang,
          'Не удалось надёжно оценить ответ. Попробуй переформулировать.',
          'Die Antwort konnte nicht sicher bewertet werden. Bitte formuliere sie anders.',
          'We could not assess that answer reliably. Please rephrase it.'));
        return;
      }
      setChecked(Boolean(result.correct)); setFeedback(result);
      void api.trackEvent({ user_id: getUserId(), event_name: 'exercise_answered', properties: { lesson_id: Number(id), exercise_index: exerciseIndex, correct: Boolean(result.correct), confidence, misconception: String(result.error_type || ''), learning_mode: String(learningProfile.mode), retry: Boolean(retried[exerciseIndex]) } });
    } catch {
      setCheckError(tr(lang, 'Не удалось проверить. Попробуй ещё раз.', 'Prüfung fehlgeschlagen. Versuche es erneut.', 'Could not check your answer. Try again.'));
    } finally { setChecking(false); }
  };
  const finish = () => {
    if (outcome?.passed) { navigate(withUser('/dashboard'), { replace: true }); return; }
    resumeSessionRef.current = '';
    initialDraft.current = null;
    completedRef.current = false;
    setStep(0); resetAnswer(); setRetried({}); setRetryExercises({});
    setOutcome(null); setCompletionState('idle'); setSessionId('');
    setLoadAttempt(value => value + 1);
  };
  const sendMilestone = (rating: string) => {
    void api.submitBetaFeedback({ user_id: getUserId(), message: `First lesson rating: ${rating}`, language: lang, page: 'lesson_complete' });
    localStorage.setItem(`deutschiq-beta-milestone-${getUserId()}`, '1');
    setMilestoneSent(true);
  };
  const deviceVoiceFallback = (rate = 0.9, text?: string) => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(
      text || content.audio_text || content.examples?.[0] || "",
    );
    utterance.lang = "de-DE";
    utterance.rate = rate;
    utterance.onstart = () => setAudioState('fallback');
    utterance.onend = () => setAudioState('idle');
    window.speechSynthesis.speak(utterance);
  };
  const playAudio = (url?: string, text?: string, rate = 0.9) => {
    const resolvedUrl = url || (!text ? content.audio_url : undefined);
    if (!resolvedUrl) {
      deviceVoiceFallback(rate, text);
      return;
    }
    const current = audioRef.current;
    if (current && audioUrlRef.current === resolvedUrl && current.paused && current.currentTime > 0 && current.currentTime < current.duration) {
      current.playbackRate = rate;
      void current.play();
      return;
    }
    current?.pause();
    const audio = new Audio(resolvedUrl);
    audio.preload = 'auto';
    audio.playbackRate = rate;
    audioRef.current = audio;
    audioUrlRef.current = resolvedUrl;
    setAudioState('loading');
    audio.onplaying = () => {
      setAudioState('playing');
      void api.trackEvent({ user_id: getUserId(), event_name: 'audio_started', properties: { lesson_id: Number(id), source: 'curated_tts', rate } });
    };
    audio.onpause = () => audio.currentTime < audio.duration && setAudioState('paused');
    audio.onended = () => setAudioState('idle');
    audio.onerror = () => {
      setAudioState('fallback');
      void api.trackEvent({ user_id: getUserId(), event_name: 'audio_failed', properties: { lesson_id: Number(id), url: resolvedUrl.slice(0, 180), online: navigator.onLine } });
      deviceVoiceFallback(rate, text);
    };
    void audio.play().catch(() => audio.onerror?.(new Event('error')));
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
    <main className={`lesson-flow precision-lesson dq-lesson fade-up level-${String(lesson.level || 'a1').toLowerCase()}`}>
      <header className="dq-lesson-progress">
        <small>{step < introSteps ? tr(lang, "ПОДГОТОВКА", "VORBEREITUNG", "PREPARE") : step < total ? activityLabel : tr(lang, "ГОТОВО", "GESCHAFFT", "COMPLETE")}</small>
        <span>{Math.min(step + 1, total)}/{total}</span>
        <div className="progress-bar">
          <div
            className="progress-bar-fill"
            style={{ width: `${Math.min(((step + 1) / total) * 100, 100)}%` }}
          />
        </div>
      </header>
      {content.module_title && step === 0 && <div className="dq-lesson-module">
        <div><small>{tr(lang, "МОДУЛЬ", "MODUL", "MODULE")}</small><strong>{content.module_title}</strong></div>
        <span>{content.module_step}/{content.module_size}</span>
      </div>}
      {step === 0 && (
        <section className="lesson-step dq-lesson-intro">
          <div className="dq-lesson-label"><span>{content.cefr || lesson.level}</span><small>{content.experience_label || tr(lang, "НОВЫЙ НАВЫК", "NEUES LERNZIEL", "NEW SKILL")}</small></div>
          <h1>{cleanTitle(topicLabel(content.title || lesson.topic, lang))}</h1>
          <p className="dq-lesson-scenario">{content.scenario || tr(lang, 'Короткая реальная ситуация на немецком.', 'Eine kurze echte Situation auf Deutsch.', 'A short real-life situation in German.')}</p>
          <div className="dq-lesson-preview">
            <small>{tr(lang, 'ФРАЗА УРОКА', 'SATZ DER LEKTION', 'LESSON PHRASE')}</small>
            <strong>{content.examples?.[0] || content.audio_text || 'Heute lerne ich Deutsch.'}</strong>
            <button type="button" onClick={() => playAudio(content.audio_url, content.audio_text, 0.92)} aria-label={tr(lang, 'Прослушать пример', 'Beispiel anhören', 'Listen to example')}><FaVolumeUp /></button>
          </div>
          <div className={`lesson-mode-pill ${learningProfile.mode}`}><span>{learningProfile.mode === 'supported'
            ? tr(lang, "С подсказками", "Mit Hinweisen", "Guided")
            : learningProfile.mode === 'challenge'
              ? tr(lang, "Самостоятельно", "Selbstständig", "Challenge")
              : tr(lang, "Сбалансировано", "Ausgewogen", "Balanced")}</span><small>{exercises.length} {tr(lang, 'заданий', 'Aufgaben', 'tasks')}</small></div>
          <div className="lesson-can-do"><small>{tr(lang, "ПОСЛЕ УРОКА", "NACH DER LEKTION", "AFTER THIS LESSON")}</small><strong>{content.can_do || content.objective}</strong></div>
          {content.mission && <div className="lesson-mission-brief"><small>{tr(lang, 'ТВОЯ МИССИЯ', 'DEINE MISSION', 'YOUR MISSION')}</small><strong>{content.mission}</strong></div>}
          <details className="lesson-optional-rule"><summary>{tr(lang, 'Короткое правило', 'Kurze Regel', 'Quick rule')}</summary><div>{content.rule}</div></details>
          <div className="lesson-practice-path" aria-label={tr(lang, 'Путь урока', 'Lektionsweg', 'Lesson path')}>
            {(content.practice_path || [tr(lang, 'Услышать', 'Hören', 'Hear'), tr(lang, 'Собрать', 'Bauen', 'Build'), tr(lang, 'Ответить', 'Antworten', 'Respond'), tr(lang, 'Использовать', 'Anwenden', 'Use')]).map((label: string, index: number) => <span key={`${label}-${index}`}><i>{index + 1}</i>{label}</span>)}
          </div>
          <button className="primary-action dq-lesson-action" onClick={next}>
            {tr(lang, "Понять на примере", "Am Beispiel verstehen", "Understand with an example")}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {step === 1 && (
        <section className="lesson-step dq-lesson-model">
          <div className="dq-lesson-label"><span>01</span><small>{tr(lang, "ЗАМЕТЬ МОДЕЛЬ", "MUSTER ERKENNEN", "NOTICE THE PATTERN")}</small></div>
          <h1>{tr(lang, "Сначала услышь смысл", "Höre zuerst die Bedeutung", "Hear the meaning first")}</h1>
          <div className="example-sentence"><small>DE</small><strong>{content.examples?.[0] || "Heute lerne ich Deutsch."}</strong></div>
          <div className="audio-controls">
            <button type="button" onClick={() => playAudio(content.audio_url, content.audio_text, 0.92)}>
              <FaVolumeUp /> {tr(lang, "Обычно", "Normal", "Normal")}
            </button>
            <button type="button" onClick={() => playAudio(content.audio_url, content.audio_text, 0.72)}>
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
          <button className="primary-action dq-lesson-action" onClick={next}>
            {tr(lang, "Начать практику", "Übung starten", "Start practice")}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {activeExercise && (
        <section className="lesson-step exercise-step dq-exercise">
          <div className="exercise-stage-row"><p className="eyebrow">{activityLabel}{retried[exerciseIndex] ? tr(lang, " · ещё раз", " · noch einmal", " · try again") : ""}</p><span>{exerciseIndex + 1}/{exercises.length}</span></div>
          {activeExercise.mission_role === 'final' && <div className="mission-stage-banner"><span>{tr(lang, 'БЕЗ МОДЕЛИ', 'OHNE MODELL', 'WITHOUT THE MODEL')}</span><strong>{tr(lang, 'Покажи, что ты можешь сделать это сам', 'Zeige, dass du es selbst kannst', 'Show that you can do it independently')}</strong></div>}
          <div className="exercise-prompt"><h1>{activeExercise.type === "repeat" ? tr(lang, "Произнеси фразу", "Sprich den Satz", "Say the sentence") : activeExercise.question}</h1></div>
          {checked === null && <div className="lesson-task-surface">
          {(activeExercise.type === "listening" || activeExercise.type === "listening_choice") && (
            <div className="listening-challenge simple">
              <button type="button" className={`listen-main ${audioState}`} onClick={() => playAudio(activeExercise.audio_url, activeExercise.audio_text, 0.92)}><FaVolumeUp /> {audioState === 'loading' ? tr(lang, 'Загрузка…', 'Wird geladen…', 'Loading…') : audioState === 'paused' ? tr(lang, 'Продолжить', 'Fortsetzen', 'Continue') : tr(lang, "Слушать", "Anhören", "Listen")}</button>
              <button type="button" className="listen-slow" onClick={() => playAudio(activeExercise.audio_url, activeExercise.audio_text, 0.72)}>{tr(lang, "Медленно", "Langsam", "Slow")}</button>
            </div>
          )}
          {(showTranscript || easyMode) && activeExercise.audio_text && <div className="listening-transcript"><small>{tr(lang, 'ТЕКСТ', 'TEXT', 'TRANSCRIPT')}</small><span>{activeExercise.audio_text}</span></div>}
          <ExerciseInteraction exercise={{ ...activeExercise, id: `${id}-${exerciseIndex}-${retried[exerciseIndex] ? 'retry' : 'first'}` }} answer={answer} onAnswer={setAnswer} disabled={checked !== null} lang={lang} onAudio={sessionId ? transcribe : undefined} onPlayAudio={playAudio} guided={Boolean(retried[exerciseIndex]) || exerciseKind(activeExercise) === 'repair'} />
          </div>}
            {speechResult?.transcript && (
              <div className="speech-result">
                <small>{tr(lang, "РАСПОЗНАНО", "ERKANNT", "RECOGNISED")}</small>
                <strong>“{speechResult.transcript}”</strong>
                {speechResult.match && <span>{speechResult.match.missing_words?.length
                  ? tr(lang, 'Некоторые ключевые слова не распознаны', 'Einige Schlüsselwörter wurden nicht erkannt', 'Some key words were not recognised')
                  : tr(lang, 'Ключевые слова распознаны', 'Die Schlüsselwörter wurden erkannt', 'Key words were recognised')}</span>}
                {speechResult.match?.missing_words?.length > 0 && <div className="speech-missing-words"><small>{tr(lang, 'НЕ РАСПОЗНАНО', 'NICHT ERKANNT', 'NOT RECOGNISED')}</small>{speechResult.match.missing_words.map((word: string) => <b key={word}>{word}</b>)}</div>}
                <em>{tr(lang, "Это оценка распознанных слов, не акцента или фонетики.", "Bewertet werden erkannte Wörter, nicht Akzent oder Phonetik.", "This measures recognised words, not accent or phonetics.")}</em>
              </div>
            )}
          {checked === null && (learningProfile.show_guided_hint || showHint || easyMode || retried[exerciseIndex]) && activeExercise.hint && (
            <div className="guided-hint">{activeExercise.hint}</div>
          )}
          {checked === null && <div className="lesson-support-row" aria-label={tr(lang, 'Помощь с заданием', 'Hilfe zur Aufgabe', 'Exercise help')}>
            {activeExercise.hint && !showHint && !learningProfile.show_guided_hint && <button type="button" onClick={() => setShowHint(true)}>{tr(lang, 'Подсказка', 'Hinweis', 'Hint')}</button>}
            {!easyMode && <button type="button" onClick={() => { setEasyMode(true); setShowHint(true); }}>{tr(lang, 'Больше помощи', 'Mehr Hilfe', 'More help')}</button>}
            {(activeExercise.type === 'listening' || activeExercise.type === 'listening_choice') && !showTranscript && <button type="button" onClick={() => setShowTranscript(true)}>{tr(lang, 'Не могу слушать', 'Kann gerade nicht hören', "I can't listen")}</button>}
            {activeExercise.mission_role !== 'final' && <button type="button" className="skip" onClick={() => void skipExercise('learner_choice')}>{tr(lang, 'Пропустить', 'Jetzt überspringen', 'Skip for now')}</button>}
          </div>}
          {checked === null ? (
            <div className="lesson-action-dock"><button className="primary-action" onClick={check} disabled={!answer.trim() || !sessionId || checking}>
              {checking ? tr(lang, 'Проверяем…', 'Wird geprüft…', 'Checking…') : tr(lang, "Проверить", "Prüfen", "Check")}
            </button></div>
          ) : (
            <div className={`answer-feedback ${checked ? "correct" : "wrong"}`}>
              {checked ? <FaCheck /> : <FaTimes />}
              <div>
                <b>
                  {checked
                    ? tr(lang, "Верно", "Richtig", "Correct")
                    : tr(lang, "Почти", "Fast richtig", "Almost")}
                </b>
                {checked && <p>{feedback?.explanation}</p>}
                {!checked && feedback?.feedback_focus && <div className="feedback-focus">
                  <small>{tr(lang, 'ИСПРАВЬ ОДНО', 'EIN SCHRITT', 'ONE FIX')}</small>
                  <strong>{feedback.feedback_focus}</strong>
                </div>}
                {!checked && feedback?.correct_answer && (retried[exerciseIndex] ? (
                  <div className="corrected-model">
                    <small>{tr(lang, 'СРАВНИ С МОДЕЛЬЮ', 'MIT DEM MODELL VERGLEICHEN', 'COMPARE WITH THE MODEL')}</small>
                    <strong>{feedback.correct_answer}</strong>
                  </div>
                ) : (
                  <details className="corrected-model model-reveal">
                    <summary>{tr(lang, 'Показать модель', 'Modell anzeigen', 'Show model')}</summary>
                    <strong>{feedback.correct_answer}</strong>
                  </details>
                ))}
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
                {!checked && !retried[exerciseIndex] && <small>{tr(lang, 'Давай соберём ответ с поддержкой.', 'Bauen wir die Antwort mit Hilfe neu.', "Let's rebuild it with support.")}</small>}
              </div>
              <button onClick={next}>
                <span>{!checked && !retried[exerciseIndex]
                  ? tr(lang, "Исправить по словам", "Mit Wörtern korrigieren", "Fix with word tiles")
                  : exercise?.mission_role === 'final' && retried[exerciseIndex]
                    ? tr(lang, "Повторить миссию самому", "Mission selbst wiederholen", "Retry the mission independently")
                    : tr(lang, "Дальше", "Weiter", "Next")}</span><FaArrowRight />
              </button>
              {!checked && activeExercise.mission_role !== 'final' && <button type="button" className="feedback-skip" onClick={() => void skipExercise('after_feedback')}>{tr(lang, 'Продолжить пока', 'Vorerst weiter', 'Continue for now')}</button>}
            </div>
          )}
          {checkError && <div className="lesson-check-error" role="alert">{checkError}</div>}
        </section>
      )}
      {step >= total && <LessonCompletion
        lang={lang}
        state={completionState}
        outcome={outcome}
        content={content}
        skillTitle={cleanTitle(topicLabel(content.title || lesson.topic, lang))}
        milestoneSent={milestoneSent}
        onRetrySave={() => void completeSession()}
        onFinish={finish}
        onBackToPlan={() => navigate(withUser('/plan'), { replace: true })}
        onRate={sendMilestone}
      />}
    </main>
  );
};
