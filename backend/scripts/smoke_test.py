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


def header(headers: dict, name: str) -> str | None:
    wanted = name.casefold()
    return next((value for key, value in headers.items() if key.casefold() == wanted), None)


def main() -> None:
    origin = (sys.argv[1] if len(sys.argv) > 1 else "https://deutschiq.onrender.com").rstrip("/")
    live = read_json(f"{origin}/api/health/live")
    health = read_json(f"{origin}/api/health")
    release = read_json(f"{origin}/api/version")
    if live.get("status") != "ok" or health.get("status") != "ok":
        raise RuntimeError(f"Unhealthy deployment: {health}")
    if release.get("version") != "79.0.0" or release.get("release") != "beta-evidence-v20":
        raise RuntimeError(f"Stale deployment: {release}")
    if health.get("database") != "ok" or health.get("migrations") != "20261003_0011":
        raise RuntimeError(f"Database is not release-ready: {health}")
    html, headers = read(f"{origin}/")
    expected_security_headers = {
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }
    for name, expected in expected_security_headers.items():
        if header(headers, name) != expected:
            raise RuntimeError(f"Missing or invalid security header {name}: {header(headers, name)}")
    markup = html.decode("utf-8")
    asset = re.search(r'(?:src|href)="(/assets/[^"]+\.(?:js|css))"', markup)
    if not asset:
        raise RuntimeError("Production shell has no versioned JS/CSS asset")
    _, asset_headers = read(f"{origin}{asset.group(1)}")
    if "max-age" not in (header(asset_headers, "Cache-Control") or "").lower():
        raise RuntimeError(f"Versioned asset is not cacheable: {header(asset_headers, 'Cache-Control')}")
    print(f"DeutschIQ {release.get('version')} ({release.get('commit')}) passed API, database, shell, security-header and asset-cache checks; shell-cache={header(headers, 'Cache-Control') or 'unset'}")


if __name__ == "__main__":
    main()
