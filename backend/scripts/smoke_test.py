"""Public post-deploy check: python backend/scripts/smoke_test.py https://deutschiq.onrender.com"""
import json
import re
import sys
import time
from urllib.request import Request, urlopen


def read(url: str, attempts: int = 4) -> tuple[bytes, dict]:
    error = None
    for index in range(attempts):
        try:
            with urlopen(Request(url, headers={"User-Agent": "DeutschIQ-release-smoke/1.0"}), timeout=30) as response:  # noqa: S310
                if response.status != 200:
                    raise RuntimeError(f"{url} returned HTTP {response.status}")
                return response.read(), dict(response.headers.items())
        except Exception as exc:  # A sleeping instance gets a bounded recovery window.
            error = exc
            if index + 1 < attempts:
                time.sleep(5 * (index + 1))
    raise RuntimeError(f"{url} failed after {attempts} attempts: {error}")


def read_json(url: str) -> dict:
    body, _ = read(url)
    return json.loads(body.decode("utf-8"))


def main() -> None:
    origin = (sys.argv[1] if len(sys.argv) > 1 else "https://deutschiq.onrender.com").rstrip("/")
    live = read_json(f"{origin}/api/health/live")
    health = read_json(f"{origin}/api/health")
    release = read_json(f"{origin}/api/version")
    if live.get("status") != "ok" or health.get("status") != "ok":
        raise RuntimeError(f"Unhealthy deployment: {health}")
    if release.get("version") != "52.0.0" or release.get("release") != "self-test-mode":
        raise RuntimeError(f"Stale deployment: {release}")
    if health.get("database") != "ok" or health.get("migrations") != "20260922_0009":
        raise RuntimeError(f"Database is not release-ready: {health}")
    html, headers = read(f"{origin}/")
    markup = html.decode("utf-8")
    asset = re.search(r'(?:src|href)="(/assets/[^"]+\.(?:js|css))"', markup)
    if not asset:
        raise RuntimeError("Production shell has no versioned JS/CSS asset")
    _, asset_headers = read(f"{origin}{asset.group(1)}")
    if "max-age" not in asset_headers.get("Cache-Control", "").lower():
        raise RuntimeError(f"Versioned asset is not cacheable: {asset_headers.get('Cache-Control')}")
    print(f"DeutschIQ {release.get('version')} ({release.get('commit')}) passed API, database, shell and asset-cache checks; shell-cache={headers.get('Cache-Control', 'unset')}")


if __name__ == "__main__":
    main()
