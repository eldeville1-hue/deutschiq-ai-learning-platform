"""Generate stable German audio assets for the complete B1 route.

Only curated curriculum text is sent to Google TTS. No learner data,
analytics, credentials, or database content is read by this script.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content  # noqa: E402


AUDIO_ROOT = BACKEND_ROOT / "static" / "audio"


def relative_audio_path(url: str) -> Path:
    clean = url.split("?", 1)[0]
    prefix = "/media/audio/"
    if not clean.startswith(prefix):
        raise ValueError(f"Unexpected audio URL: {url}")
    return AUDIO_ROOT / clean.removeprefix(prefix)


def audio_jobs() -> dict[Path, str]:
    jobs: dict[Path, str] = {}
    for row in B1_CURRICULUM:
        content = build_b1_content(row)
        jobs[relative_audio_path(content["audio_url"])] = content["audio_text"]
        for exercise in content["exercises"]:
            if exercise.get("audio_url"):
                jobs[relative_audio_path(exercise["audio_url"])] = str(exercise.get("audio_text") or exercise.get("answer") or "")
            for turn in exercise.get("conversation_turns") or []:
                if turn.get("audio_url"):
                    jobs[relative_audio_path(turn["audio_url"])] = str(turn["partner"])
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
        gTTS(text=script, lang="de", tld="de").save(str(path))
        return path

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(generate, job) for job in ordered]
        for index, future in enumerate(as_completed(futures), start=1):
            path = future.result()
            print(f"[{index:03d}/{len(jobs)}] {path.relative_to(AUDIO_ROOT)}")
    print(f"Generated {len(jobs)} curated B1 audio files.")


if __name__ == "__main__":
    main()
