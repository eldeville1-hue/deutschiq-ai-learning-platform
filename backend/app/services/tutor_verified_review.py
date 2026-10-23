"""Choose review topics from verified Tutor attempts, never from AI chat."""
from collections import defaultdict

from app.services.tutor_fallback import TOPIC_LESSONS


def prioritize_verified_topics(events, limit=3):
    """Return topics with unresolved verified errors, newest attempt wins per topic.

    A later correct answer clears an earlier error for that topic. Ignore
    malformed, unrelated and unreviewed events. Does not update mastery.
    """
    latest = {}
    errors = defaultdict(int)
    for event in events:
        if getattr(event, "event_name", None) != "tutor_verified_attempt":
            continue
        props = getattr(event, "properties", None)
        if not isinstance(props, dict) or props.get("source") != "reviewed_word_order":
            continue
        topic, correct = props.get("topic"), props.get("correct")
        if topic not in TOPIC_LESSONS or type(correct) is not bool:
            continue
        errors[topic] += not correct
        timestamp = getattr(event, "created_at", None)
        key = (timestamp is not None, timestamp, getattr(event, "id", 0))
        if topic not in latest or key > latest[topic][0]:
            latest[topic] = (key, correct)
    unresolved = [topic for topic, (_, correct) in latest.items() if not correct]
    return sorted(unresolved, key=lambda topic: (-errors[topic], topic))[:limit]
