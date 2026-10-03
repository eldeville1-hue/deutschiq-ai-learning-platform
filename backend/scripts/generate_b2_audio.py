"""Generate stable German audio for B2 from curated curriculum copy only."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys
import time

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content  # noqa: E402

AUDIO_ROOT = BACKEND_ROOT / "static" / "audio"


def audio_jobs() -> dict[Path, str]:
    jobs: dict[Path, str] = {}
    for row in B2_CURRICULUM:
        content = build_b2_content(row)
        topic = row[2]
        base = AUDIO_ROOT / "b2" / topic
        jobs[base / "model.mp3"] = content["audio_text"]
        for exercise in content["exercises"]:
            if exercise.get("type") in {"listening_choice", "repeat"}:
                filename = "listen.mp3" if exercise["type"] == "listening_choice" else "repeat.mp3"
                jobs[base / filename] = str(exercise.get("audio_text") or exercise.get("answer") or "")
            for index, turn in enumerate(exercise.get("conversation_turns") or [], start=1):
                jobs[base / f"dialogue-{index}.mp3"] = str(turn["partner"])
    return jobs


def main() -> None:
    jobs = audio_jobs()
    ordered = sorted(jobs.items())
    for path, script in ordered:
        if not script.strip():
            raise ValueError(f"Missing German script for {path}")
        path.parent.mkdir(parents=True, exist_ok=True)

    def generate(job: tuple[Path, str]) -> Path:
        from gtts import gTTS

        path, script = job
        temporary = path.with_suffix(".mp3.part")
        for attempt in range(4):
            try:
                gTTS(text=script, lang="de", tld="de", timeout=30).save(str(temporary))
                temporary.replace(path)
                return path
            except Exception:
                temporary.unlink(missing_ok=True)
                if attempt == 3:
                    raise
                time.sleep(15 * (attempt + 1))
        return path

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(generate, job) for job in ordered]
        for index, future in enumerate(as_completed(futures), start=1):
            path = future.result()
            print(f"[{index:03d}/{len(jobs)}] {path.relative_to(AUDIO_ROOT)}")
    print(f"Generated {len(jobs)} curated B2 audio files.")


if __name__ == "__main__":
    main()
