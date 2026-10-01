import secrets
from urllib.parse import urlsplit


def public_origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}" if parts.scheme and parts.netloc else url


def secret_matches(received: str | None, expected: str) -> bool:
    return bool(received and expected and secrets.compare_digest(received, expected))


def cache_control_for_path(path: str, content_type: str = "") -> str | None:
    """Keep the SPA shell fresh while fingerprinted bundles stay on-device."""
    if path.startswith("/assets/"):
        return "public, max-age=31536000, immutable"
    if path.startswith("/media/audio/"):
        # Audio URLs carry a release query version, so the relatively large
        # lesson library can stay on-device without being downloaded again.
        return "public, max-age=31536000, immutable"
    if not path.startswith("/api/") and ("text/html" in content_type or "." not in path.rsplit("/", 1)[-1]):
        return "no-cache"
    return None