import React, { useEffect, useMemo, useState } from "react";
import { FaArrowRight, FaCheck, FaTimes, FaVolumeUp } from "react-icons/fa";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";
import { topicLabel } from "../i18n/topics";
import { getUserId, withUser } from "../utils/user";

export const Lesson: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const [lesson, setLesson] = useState<any>(null);
  const [step, setStep] = useState(0);
  const [answer, setAnswer] = useState("");
  const [checked, setChecked] = useState<boolean | null>(null);
  const [feedback, setFeedback] = useState<any>(null);
  const [confidence, setConfidence] = useState<"guess" | "okay" | "sure">(
    "okay",
  );
  const [startedAt, setStartedAt] = useState(() => Date.now());
  const [retried, setRetried] = useState<Record<number, boolean>>({});
  const [outcome, setOutcome] = useState<any>(null);
  const [sessionId, setSessionId] = useState("");
  const [usedTokens, setUsedTokens] = useState<number[]>([]);
  const exercises = useMemo(
    () => (lesson?.content?.exercises || []).slice(0, 3),
    [lesson],
  );
  const total = 4 + exercises.length;
  useEffect(() => {
    Promise.all([
      api.getLesson(Number(id)),
      api.startLesson({ user_id: getUserId(), lesson_id: Number(id) }),
    ])
      .then(([lessonData, session]) => {
        setLesson(lessonData);
        setSessionId(session.session_id);
      })
      .catch(() => setLesson(false));
  }, [id]);
  if (lesson === null)
    return (
      <div className="app-shell">
        <div className="skeleton hero-skeleton" />
      </div>
    );
  if (!lesson)
    return (
      <div className="app-shell empty-state">
        {lang === "ru" ? "Урок не найден" : "Lektion nicht gefunden"}
      </div>
    );
  const content = lesson.content || {};
  const exerciseIndex = step - 4;
  const exercise = exercises[exerciseIndex];
  const resetAnswer = () => {
    setAnswer("");
    setUsedTokens([]);
    setChecked(null);
    setFeedback(null);
    setConfidence("okay");
    setStartedAt(Date.now());
  };
  const next = async () => {
    if (exercise && checked === false && !retried[exerciseIndex]) {
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
    }
  };
  const check = async () => {
    if (!answer.trim() || !sessionId) return;
    const result = await api.checkLessonAnswer({
      user_id: getUserId(),
      lesson_id: Number(id),
      exercise_index: exerciseIndex,
      answer,
      session_id: sessionId,
      confidence,
      response_ms: Date.now() - startedAt,
    });
    setChecked(Boolean(result.correct));
    setFeedback(result);
  };
  const finish = () =>
    navigate(withUser(outcome?.passed ? "/plan" : `/lesson/${id}`), {
      replace: true,
    });
  const speak = (rate = 0.9) => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(
      content.audio_text || content.examples?.[0] || "",
    );
    utterance.lang = "de-DE";
    utterance.rate = rate;
    window.speechSynthesis.speak(utterance);
  };
  const addToken = (token: string, index: number) => {
    setUsedTokens((value) => [...value, index]);
    setAnswer((value) => `${value}${value ? " " : ""}${token}`);
  };
  return (
    <main className="lesson-flow precision-lesson fade-up">
      <header>
        <span>
          {Math.min(step + 1, total)} {lang === "ru" ? "из" : "von"} {total}
        </span>
        <div className="progress-bar">
          <div
            className="progress-bar-fill"
            style={{ width: `${Math.min(((step + 1) / total) * 100, 100)}%` }}
          />
        </div>
      </header>
      {step === 0 && (
        <section className="lesson-step">
          <p className="eyebrow">
            {lang === "ru" ? "ЦЕЛЬ УРОКА" : "LERNZIEL"} ·{" "}
            {content.cefr || lesson.level}
          </p>
          <h1>{topicLabel(content.title || lesson.topic, lang)}</h1>
          <div className="lesson-objective">{content.objective}</div>
          <div className="rule-card">{content.rule}</div>
          <button className="primary-action" onClick={next}>
            {lang === "ru" ? "Показать пример" : "Beispiel ansehen"}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {step === 1 && (
        <section className="lesson-step">
          <p className="eyebrow">
            {lang === "ru" ? "СЛУШАЙ И ЗАМЕЧАЙ" : "HÖREN UND ERKENNEN"}
          </p>
          <h1>
            {lang === "ru"
              ? "Сначала услышь структуру"
              : "Höre zuerst die Struktur"}
          </h1>
          <div className="example-sentence">
            {content.examples?.[0] || "Heute lerne ich Deutsch."}
          </div>
          <div className="audio-controls">
            <button onClick={() => speak(0.9)}>
              <FaVolumeUp /> {lang === "ru" ? "Обычная скорость" : "Normal"}
            </button>
            <button onClick={() => speak(0.65)}>
              <FaVolumeUp /> {lang === "ru" ? "Медленно" : "Langsam"}
            </button>
          </div>
          <button className="primary-action" onClick={next}>
            {lang === "ru" ? "Понять ошибку" : "Fehler verstehen"}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {step === 2 && (
        <section className="lesson-step">
          <p className="eyebrow">
            {lang === "ru" ? "НЕ ПУТАЙ" : "NICHT VERWECHSELN"}
          </p>
          <h1>{lang === "ru" ? "Типичная ошибка" : "Typischer Fehler"}</h1>
          <div className="mistake-contrast">
            {(content.common_mistakes || []).map(
              (item: string, index: number) => (
                <div
                  key={index}
                  className={item.includes("❌") ? "bad" : "good"}
                >
                  {item}
                </div>
              ),
            )}
          </div>
          <button className="primary-action" onClick={next}>
            {lang === "ru" ? "Я вижу разницу" : "Ich sehe den Unterschied"}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {step === 3 && (
        <section className="lesson-step retrieval-gate">
          <p className="eyebrow">
            {lang === "ru" ? "ПЕРЕД ПРАКТИКОЙ" : "VOR DER ÜBUNG"}
          </p>
          <h1>
          {lang === "ru"
            ? content.recall_prompt || "Закрой пример и вспомни правило своими словами"
            : "Erinnere dich an die Regel mit eigenen Worten"}
          </h1>
          <p>
            {lang === "ru"
              ? "Этот короткий момент воспроизведения помогает запомнить лучше, чем повторное чтение."
              : "Aktives Erinnern wirkt stärker als erneutes Lesen."}
          </p>
          <button className="primary-action" onClick={next}>
            {lang === "ru" ? "Готов к заданиям" : "Bereit für Aufgaben"}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
      {exercise && (
        <section className="lesson-step">
          <p className="eyebrow">
            {exercise.stage === "guided"
              ? lang === "ru"
                ? "С ПОДДЕРЖКОЙ"
                : "MIT HILFE"
              : exercise.stage === "transfer"
                ? lang === "ru"
                  ? "ТВОЯ ФРАЗА"
                  : "DEIN SATZ"
                : lang === "ru"
                  ? "БЕЗ ПОДСКАЗКИ"
                  : "OHNE HILFE"}{" "}
            · {exerciseIndex + 1}/{exercises.length}
            {retried[exerciseIndex]
              ? lang === "ru"
                ? " · вторая попытка"
                : " · zweiter Versuch"
              : ""}
          </p>
          <h1>{exercise.question}</h1>
          {exercise.type === "choose" && Array.isArray(exercise.options) ? (
            <div className="lesson-options">
              {exercise.options.map((option: string) => (
                <button
                  key={option}
                  onClick={() => setAnswer(option)}
                  className={answer === option ? "active" : ""}
                >
                  {option}
                </button>
              ))}
            </div>
          ) : exercise.type === "reorder" ? (
            <>
              <div className="reorder-answer">
                {answer ||
                  (lang === "ru"
                    ? "Нажимай слова по порядку"
                    : "Wörter antippen")}
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
                {lang === "ru" ? "Сбросить" : "Löschen"}
              </button>
            </>
          ) : (
            <textarea
              className="lesson-answer production-answer"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder={
                exercise.type === "production"
                  ? lang === "ru"
                    ? "Напиши свою немецкую фразу…"
                    : "Schreibe deinen eigenen Satz…"
                  : lang === "ru"
                    ? "Введи ответ"
                    : "Antwort eingeben"
              }
              disabled={checked !== null}
            />
          )}
          {checked === null && exercise.stage === "guided" && (
            <div className="guided-hint">{exercise.hint}</div>
          )}
          {checked === null && (
            <div className="confidence-check">
              <small>
                {lang === "ru" ? "Насколько ты уверен?" : "Wie sicher bist du?"}
              </small>
              <div>
                <button
                  className={confidence === "guess" ? "active" : ""}
                  onClick={() => setConfidence("guess")}
                >
                  {lang === "ru" ? "Угадываю" : "Geraten"}
                </button>
                <button
                  className={confidence === "okay" ? "active" : ""}
                  onClick={() => setConfidence("okay")}
                >
                  {lang === "ru" ? "Не совсем" : "Nicht ganz"}
                </button>
                <button
                  className={confidence === "sure" ? "active" : ""}
                  onClick={() => setConfidence("sure")}
                >
                  {lang === "ru" ? "Уверен" : "Sicher"}
                </button>
              </div>
            </div>
          )}
          {checked === null ? (
            <button className="primary-action" onClick={check}>
              {lang === "ru" ? "Проверить" : "Prüfen"}
            </button>
          ) : (
            <div className={`answer-feedback ${checked ? "correct" : "wrong"}`}>
              {checked ? <FaCheck /> : <FaTimes />}
              <div>
                <b>
                  {checked
                    ? lang === "ru"
                      ? `Верно · освоено ${feedback?.mastery || 0}%`
                      : `Richtig · ${feedback?.mastery || 0}% beherrscht`
                    : lang === "ru"
                      ? "Разберём ошибку"
                      : "Fehler verstehen"}
                </b>
                <p>{feedback?.explanation}</p>
                {feedback?.production && (
                  <small>
                    {lang === "ru"
                      ? `${feedback.production_score != null ? `Оценка фразы: ${feedback.production_score}% · ` : ""}Исправленная модель: ${feedback.correct_answer}`
                      : `${feedback.production_score != null ? `Satzbewertung: ${feedback.production_score}% · ` : ""}Korrigiertes Modell: ${feedback.correct_answer}`}
                  </small>
                )}
                {!checked && !retried[exerciseIndex] && (
                  <small>
                    {lang === "ru"
                      ? "Сейчас попробуешь ещё раз без подсказки."
                      : "Du versuchst es gleich noch einmal ohne Hinweis."}
                  </small>
                )}
              </div>
              <button onClick={next}>
                <FaArrowRight />
              </button>
            </div>
          )}
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
              ? lang === "ru"
                ? "НУЖНО ЕЩЁ ЗАКРЕПИТЬ"
                : "NOCH EINMAL FESTIGEN"
              : lang === "ru"
                ? "УРОК ОСВОЕН"
                : "LEKTION GESCHAFFT"}
          </p>
          <h1>{outcome ? `${outcome.score}%` : "…"}</h1>
          <div className="lesson-score">
            <span>
              {lang === "ru" ? "Освоение темы" : "Themenkenntnis"}
              <b>{outcome?.mastery || 0}%</b>
            </span>
            <span>
              {lang === "ru" ? "Получено" : "Erhalten"}
              <b>+{outcome?.xp_gained || 0} XP</b>
            </span>
          </div>
          <p>
            {outcome?.passed === false
              ? lang === "ru"
                ? "Урок не отмечен завершённым: повтори задания и достигни 70%."
                : "Die Lektion bleibt offen. Wiederhole sie und erreiche 70%."
              : lang === "ru"
                ? "Результат рассчитан по твоим реальным ответам."
                : "Das Ergebnis basiert auf deinen echten Antworten."}
          </p>
          <button className="primary-action" onClick={finish}>
            {outcome?.passed === false
              ? lang === "ru"
                ? "Повторить урок"
                : "Lektion wiederholen"
              : lang === "ru"
                ? "Вернуться к плану"
                : "Zurück zum Lernplan"}{" "}
            <FaArrowRight />
          </button>
        </section>
      )}
    </main>
  );
};
