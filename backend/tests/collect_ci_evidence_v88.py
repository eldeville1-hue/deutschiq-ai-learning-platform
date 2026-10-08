"""Fetch GitHub Actions run and all job pages; fail closed on incomplete evidence.

Usage: python -m tests.collect_ci_evidence_v88 OWNER/REPO RUN_ID EXPECTED_SHA
Requires GITHUB_TOKEN for private repositories. Does not grant human signoff.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

REQUIRED_JOBS = ("backend", "frontend", "e2e-mobile")


def verify(run, jobs, expected_sha, now=None):
    now = now or datetime.now(timezone.utc)
    reasons = []
    if not isinstance(run, dict) or not isinstance(jobs, list):
        return {"verified": False, "reasons": ["invalid_payload"]}
    if run.get("head_sha") != expected_sha or not expected_sha:
        reasons.append("commit_mismatch")
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        reasons.append("workflow_not_successful")
    if run.get("event") not in ("push", "workflow_dispatch"):
        reasons.append("untrusted_event")
    if run.get("head_branch") != "main":
        reasons.append("wrong_branch")
    try:
        finished = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
        if finished > now or (now - finished).total_seconds() > 86400:
            reasons.append("stale_run")
    except (KeyError, ValueError, TypeError):
        reasons.append("missing_timestamp")
    by_name = {job.get("name"): job for job in jobs if isinstance(job, dict)}
    for name in REQUIRED_JOBS:
        job = by_name.get(name)
        if not job or job.get("status") != "completed" or job.get("conclusion") != "success":
            reasons.append("job_not_successful:" + name)
    return {"verified": not reasons, "reasons": reasons, "run_id": run.get("id"),
            "head_sha": run.get("head_sha"),
            "jobs": {name: {"status": by_name.get(name, {}).get("status"),
                             "conclusion": by_name.get(name, {}).get("conclusion")}
                     for name in REQUIRED_JOBS}}


def collect(repo, run_id, expected_sha):
    token = os.environ.get("GITHUB_TOKEN")
    base = "https://api.github.com/repos/" + repo + "/actions/runs/" + str(int(run_id))
    def get(url):
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "DeutschIQ-v88"}
        if token:
            headers["Authorization"] = "Bearer " + token
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15) as response:
            return json.load(response)
    run = get(base)
    jobs = []
    page = 1
    while True:
        payload = get(base + "/jobs?per_page=100&page=" + str(page))
        chunk = payload.get("jobs", [])
        jobs.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
        if page > 100:
            raise ValueError("job_pagination_limit")
    return verify(run, jobs, expected_sha)


if __name__ == "__main__":
    try:
        result = collect(sys.argv[1], sys.argv[2], sys.argv[3])
    except (IndexError, ValueError, OSError) as exc:
        result = {"verified": False, "reasons": [str(exc)]}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["verified"] else 2)
