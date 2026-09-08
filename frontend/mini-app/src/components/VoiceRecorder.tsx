import React, { useEffect, useRef, useState } from "react";
import { FaMicrophone, FaStop } from "react-icons/fa";

type Props = {
  disabled?: boolean;
  lang: "ru" | "de";
  onAudio: (blob: Blob) => Promise<void>;
};

export const VoiceRecorder: React.FC<Props> = ({ disabled, lang, onAudio }) => {
  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const chunks = useRef<Blob[]>([]);
  const stopTimer = useRef<number | null>(null);
  const [state, setState] = useState<"idle" | "recording" | "sending" | "error">("idle");
  const [seconds, setSeconds] = useState(0);

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
        } catch {
          setState("error");
        }
      };
      mediaRecorder.start();
      stopTimer.current = window.setTimeout(() => {
        if (mediaRecorder.state === "recording") mediaRecorder.stop();
      }, 20000);
      setState("recording");
    } catch {
      setState("error");
    }
  };

  const stop = () => recorder.current?.state === "recording" && recorder.current.stop();

  return (
    <div className={`voice-recorder ${state}`}>
      {state === "recording" ? (
        <button type="button" onClick={stop} className="voice-button recording"><FaStop /> {seconds}s</button>
      ) : (
        <button type="button" onClick={start} disabled={disabled || state === "sending"} className="voice-button">
          <FaMicrophone /> {state === "sending" ? (lang === "ru" ? "Распознаём…" : "Wird erkannt…") : (lang === "ru" ? "Ответить голосом" : "Mit Stimme antworten")}
        </button>
      )}
      {state === "error" && <p>{lang === "ru" ? "Не удалось распознать речь. Можно напечатать ответ." : "Spracherkennung nicht verfügbar. Du kannst tippen."}</p>}
      <small>{lang === "ru" ? "До 20 секунд · аудиозапись не сохраняется" : "Bis 20 Sekunden · Audio wird nicht gespeichert"}</small>
    </div>
  );
};
