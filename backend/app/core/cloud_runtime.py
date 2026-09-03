import secrets
from urllib.parse import urlsplit


def public_origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}" if parts.scheme and parts.netloc else url


def secret_matches(received: str | None, expected: str) -> bool:
    return bool(received and expected and secrets.compare_digest(received, expected))
