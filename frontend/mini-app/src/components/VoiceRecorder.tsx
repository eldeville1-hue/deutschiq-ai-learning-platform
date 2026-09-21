import React, { useEffect, useRef, useState } from "react";
import { FaMicrophone, FaStop } from "react-icons/fa";
import type { AppLanguage } from '../i18n/language';
import { tr } from '../i18n/language';
import { api } from '../services/api';
import { getUserId } from '../utils/user';

type Props = {
  compact?: boolean;
  disabled?: boolean;
  lang: AppLanguage;
  onAudio: (blob: Blob) => Promise<void>;
};

export const VoiceRecorder: React.FC<Props> = ({ compact = false, disabled, lang, onAudio }) => {
  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const chunks = useRef<Blob[]>([]);
  const stopTimer = useRef<number | null>(null);
  const [state, setState] = useState<"idle" | "recording" | "sending" | "error">("idle");
  const [seconds, setSeconds] = useState(0);
  const reportFailure = (stage: string, error?: unknown) => {
    if (!getUserId()) return;
    void api.trackEvent({ user_id: getUserId(), event_name: 'microphone_failed', properties: {
      stage, error: error instanceof Error ? error.name : String(error || 'unavailable'),
      media_recorder: typeof MediaRecorder !== 'undefined',
    }});
  };

  useEffect(() => {
    if (state !== "recording") return;
    const timer = window.setInterval(() => setSeconds(value => value + 1), 1000);
    return () => window.clearInterval(timer);
  }, [state]);

  useEffect(() => () => {
    stream.current?.getTracks().forEach(track => track.stop());
    if (stopTimer.current) window.clearTimeout(stopTimer.current);
  }, []);

  const start = async () => {
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      setState("error");
      reportFailure('unsupported');
      return;
    }
    try {
      stream.current = await navigator.mediaDevices.getUserMedia({ audio: true });
      chunks.current = [];
      setSeconds(0);
      const mediaRecorder = new MediaRecorder(stream.current);
      recorder.current = mediaRecorder;
      mediaRecorder.ondataavailable = event => event.data.size && chunks.current.push(event.data);
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks.current, { type: mediaRecorder.mimeType || "audio/webm" });
        stream.current?.getTracks().forEach(track => track.stop());
        setState("sending");
        try {
          await onAudio(blob);
          setState("idle");
        } catch (error) {
          setState("error");
          reportFailure('transcription', error);
        }
      };
      mediaRecorder.start();
      stopTimer.current = window.setTimeout(() => {
        if (mediaRecorder.state === "recording") mediaRecorder.stop();
      }, 20000);
      setState("recording");
    } catch (error) {
      setState("error");
      reportFailure('permission_or_recording', error);
    }
  };

  const stop = () => recorder.current?.state === "recording" && recorder.current.stop();

  return (
    <div className={`voice-recorder ${state}`}>
      {state === "recording" ? (
        <button type="button" onClick={stop} className="voice-button recording"><FaStop /> {seconds}s</button>
      ) : (
        <button type="button" onClick={start} disabled={disabled || state === "sending"} className="voice-button">
          <FaMicrophone /> {state === "sending" ? tr(lang, "Распознаём…", "Wird erkannt…", "Transcribing…") : compact ? tr(lang, "Голосом", "Sprechen", "Speak") : tr(lang, "Ответить голосом", "Mit Stimme antworten", "Answer by voice")}
        </button>
      )}
      {state === "error" && <p>{tr(lang, "Не удалось распознать речь. Можно напечатать ответ.", "Spracherkennung nicht verfügbar. Du kannst tippen.", "Speech recognition is unavailable. You can type your answer.")}</p>}
      {!compact && <small>{tr(lang, "До 20 секунд · аудиозапись не сохраняется", "Bis 20 Sekunden · Audio wird nicht gespeichert", "Up to 20 seconds · audio is not stored")}</small>}
    </div>
  );
};
