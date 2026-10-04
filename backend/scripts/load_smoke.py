#!/usr/bin/env python3
"""Bounded, read-only concurrency smoke for a deployed DeutschIQ service."""

import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.request
from collections import Counter


def fetch(url: str, timeout: float) -> tuple[int, float]:
    started = time.perf_counter()
    request = urllib.request.Request(url, headers={"User-Agent": "DeutschIQ-load-smoke/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response.read()
        return response.status, (time.perf_counter() - started) * 1000


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--requests", type=int, default=60)
    parser.add_argument("--concurrency", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--p95-ms", type=float, default=2500)
    args = parser.parse_args()
    if not 1 <= args.requests <= 500 or not 1 <= args.concurrency <= 50:
        raise SystemExit("Use 1-500 requests and 1-50 workers.")

    base = args.base_url.rstrip("/")
    paths = ("/api/health/live", "/api/version", "/")
    urls = [base + paths[index % len(paths)] for index in range(args.requests)]
    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(fetch, url, args.timeout) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:
                errors.append(type(exc).__name__)

    latencies = sorted(item[1] for item in results)
    p95 = latencies[max(0, int(len(latencies) * 0.95) - 1)] if latencies else float("inf")
    summary = {
        "requests": args.requests,
        "completed": len(results),
        "errors": len(errors),
        "p50_ms": round(statistics.median(latencies), 1) if latencies else None,
        "p95_ms": round(p95, 1) if latencies else None,
        "max_ms": round(max(latencies), 1) if latencies else None,
        "statuses": dict(Counter(str(status) for status, _ in results)),
    }
    print(json.dumps(summary, indent=2))
    if errors or any(status != 200 for status, _ in results) or p95 > args.p95_ms:
        raise SystemExit("Load smoke failed")


if __name__ == "__main__":
    main()
