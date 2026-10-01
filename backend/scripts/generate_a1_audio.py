"""Generate stable, pre-rendered German audio assets for the complete A1 route.

This is a release-authoring tool, not a production dependency. Install gTTS
locally before running it; the generated MP3 files are committed with the app.
"""

from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from gtts import gTTS


BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.content.foundation_curriculum import A1_CURRICULUM, build_foundation_content  # noqa: E402


AUDIO_ROOT = BACKEND_ROOT / "static" / "audio"


def relative_audio_path(url: str) -> Path:
    clean = url.split("?", 1)[0]
    prefix = "/media/audio/"
    if not clean.startswith(prefix):
        raise ValueError(f"Unexpected audio URL: {url}")
    return AUDIO_ROOT / clean.removeprefix(prefix)


def audio_jobs() -> dict[Path, str]:
    jobs: dict[Path, str] = {}
    for row in A1_CURRICULUM:
        content = build_foundation_content(row, "A1")
        jobs[relative_audio_path(content["audio_url"])] = content["audio_text"]
        for exercise in content["exercises"]:
            if exercise.get("audio_url"):
                jobs[relative_audio_path(exercise["audio_url"])] = str(
                    exercise.get("audio_text") or exercise.get("answer") or ""
                )
            for turn in exercise.get("conversation_turns") or []:
                if turn.get("audio_url"):
                    jobs[relative_audio_path(turn["audio_url"])] = str(turn["partner"])
    return jobs


def main() -> None:
    jobs = audio_jobs()
    ordered = sorted(jobs.items())
    for path, text in ordered:
        if not text.strip():
            raise ValueError(f"Missing German script for {path}")
        path.parent.mkdir(parents=True, exist_ok=True)

    def generate(job: tuple[Path, str]) -> Path:
        path, text = job
        gTTS(text=text, lang="de", tld="de").save(str(path))
        return path

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(generate, job) for job in ordered]
        for index, future in enumerate(as_completed(futures), start=1):
            path = future.result()
            print(f"[{index:02d}/{len(jobs)}] {path.relative_to(AUDIO_ROOT)}")
    print(f"Generated {len(jobs)} curated A1 audio files.")


if __name__ == "__main__":
    main()