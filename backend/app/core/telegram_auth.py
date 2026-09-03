import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from fastapi import Header, HTTPException

from app.core.config import settings


def verify_telegram_init_data(init_data: str) -> int:
    values = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = values.pop("hash", "")
    if not received_hash:
        raise HTTPException(status_code=401, detail="Telegram authentication required")
    data_check_string = "\n".join(f"{key}={values[key]}" for key in sorted(values))
    secret = hmac.new(b"WebAppData", settings.BOT_TOKEN.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        raise HTTPException(status_code=401, detail="Invalid Telegram signature")
    try:
        return int(json.loads(values["user"])["id"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Telegram user is missing")


async def telegram_user_id(
    x_telegram_init_data: str | None = Header(default=None),
    x_dev_user_id: int | None = Header(default=None),
) -> int:
    if settings.DEBUG and x_dev_user_id:
        return x_dev_user_id
    if not x_telegram_init_data:
        raise HTTPException(status_code=401, detail="Open DeutschIQ from Telegram")
    return verify_telegram_init_data(x_telegram_init_data)


def assert_owner(authenticated_id: int, claimed_id: int) -> None:
    if authenticated_id != claimed_id:
        raise HTTPException(status_code=403, detail="User identity mismatch")
