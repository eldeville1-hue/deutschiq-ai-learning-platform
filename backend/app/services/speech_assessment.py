import re
from difflib import SequenceMatcher


def normalize_speech(value: str) -> str:
    value = value.lower().replace("ß", "ss")
    return " ".join(re.findall(r"[a-zäöü0-9]+", value))


def assess_speech_match(transcript: str, target: str) -> dict:
    heard = normalize_speech(transcript)
    expected = normalize_speech(target)
    if not heard or not expected:
        return {"score": 0, "label": "try_again", "missing_words": expected.split()}
    expected_words = expected.split()
    heard_words = set(heard.split())
    coverage = sum(word in heard_words for word in expected_words) / max(len(expected_words), 1)
    sequence = SequenceMatcher(None, heard, expected).ratio()
    score = round((coverage * 0.6 + sequence * 0.4) * 100)
    label = "clear_match" if score >= 85 else "close_match" if score >= 65 else "try_again"
    return {
        "score": score,
        "label": label,
        "missing_words": [word for word in expected_words if word not in heard_words][:5],
    }
