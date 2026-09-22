import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


INVITE_PAYLOAD_PREFIX = "invite_"


def parse_start_payload(text: str | None) -> str:
    parts = (text or "").strip().split(maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else ""


def invite_code_from_payload(payload: str) -> str | None:
    if not payload.lower().startswith(INVITE_PAYLOAD_PREFIX):
        return None
    code = payload[len(INVITE_PAYLOAD_PREFIX):].strip().upper()
    return code if re.fullmatch(r"[A-F0-9]{8,32}", code) else None


def build_web_app_url(base_url: str, route: str = "", **query_updates: str) -> str:
    parts = urlsplit(base_url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({key: value for key, value in query_updates.items() if value})
    path = route if route else parts.path
    return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), parts.fragment))


def telegram_beta_invite_url(bot_username: str, code: str) -> str:
    username = bot_username.strip().lstrip("@")
    return f"https://t.me/{username}?start={INVITE_PAYLOAD_PREFIX}{code.upper()}"
