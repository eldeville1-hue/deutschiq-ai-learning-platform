from datetime import datetime, timezone

from app.core.config import settings


PLAN_CODE = "pro_monthly"


def monthly_invoice_payload(telegram_id: int) -> str:
    return f"deutschiq:{PLAN_CODE}:{telegram_id}"


def validate_pre_checkout(query) -> str | None:
    """Return a user-safe rejection reason, or None for a valid Pro order."""
    expected = monthly_invoice_payload(query.from_user.id)
    if not settings.PAYMENTS_ENABLED:
        return "Payments are not available yet."
    if query.invoice_payload != expected:
        return "This payment link is invalid or belongs to another account."
    if query.currency != "XTR" or query.total_amount != settings.PRO_PRICE_STARS:
        return "The subscription price changed. Please request a new invoice."
    return None


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
        "payments_enabled": settings.PAYMENTS_ENABLED,
        "beta_free": settings.BETA_FREE_ACCESS,
        "pro_price_stars": settings.PRO_PRICE_STARS,
        "commerce_ready": bool(settings.PAYMENTS_ENABLED and settings.SELLER_LEGAL_NAME and settings.SELLER_POSTAL_ADDRESS and settings.SELLER_SUPPORT_EMAIL),
    }
