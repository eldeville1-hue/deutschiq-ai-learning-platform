"""Public post-deploy check: python backend/scripts/smoke_test.py https://deutschiq.onrender.com"""
import json
import sys
from urllib.request import urlopen


def read_json(url: str) -> dict:
    with urlopen(url, timeout=30) as response:  # noqa: S310 - operator supplies the URL
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    origin = (sys.argv[1] if len(sys.argv) > 1 else "https://deutschiq.onrender.com").rstrip("/")
    live = read_json(f"{origin}/api/health/live")
    health = read_json(f"{origin}/api/health")
    release = read_json(f"{origin}/api/version")
    if live.get("status") != "ok" or health.get("status") != "ok":
        raise RuntimeError(f"Unhealthy deployment: {health}")
    if release.get("version") != "22.0.0" or release.get("release") != "balanced-placement":
        raise RuntimeError(f"Stale deployment: {release}")
    print(f"DeutschIQ {release.get('version')} ({release.get('commit')}) is healthy: database={health.get('database')}, migrations={health.get('migrations')}")


if __name__ == "__main__":
    main()
