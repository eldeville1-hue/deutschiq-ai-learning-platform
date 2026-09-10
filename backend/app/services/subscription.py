from datetime import datetime, timezone


def has_active_pro(user, now: datetime | None = None) -> bool:
    """Return the effective paid state and expire stale monthly access."""
    if not user or user.subscription_status not in {"pro", "premium"}:
        return False
    if not user.subscription_end_date:
        return True
    current = now or datetime.now(timezone.utc)
    end = user.subscription_end_date
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return end > current


def subscription_payload(user) -> dict:
    active = has_active_pro(user)
    return {
        "subscription_status": "pro" if active else "free",
        "subscription_end_date": user.subscription_end_date.isoformat() if active and user.subscription_end_date else None,
    }
