import asyncio
import unittest
from datetime import datetime, timezone
from tests.collect_ci_evidence_v88 import verify
from tests.benchmark_ai_evaluation_v88 import measure_ai
from tests.release_readiness_v88 import build_report


class EvidenceIntegrationTests(unittest.TestCase):
    def test_job_evidence_requires_all_jobs_and_matching_sha(self):
        sha = "a" * 40
        run = {"id": 12, "head_sha": sha, "status": "completed",
               "conclusion": "success", "head_branch": "main", "event": "push",
               "updated_at": datetime.now(timezone.utc).isoformat()}
        jobs = [{"name": name, "status": "completed", "conclusion": "success"}
                for name in ("backend", "frontend", "e2e-mobile")]
        self.assertTrue(verify(run, jobs, sha)["verified"])
        self.assertFalse(verify(run, jobs[:-1], sha)["verified"])
        self.assertFalse(verify(run, jobs, "b" * 40)["verified"])

    def test_ai_timeout_counts_as_failure(self):
        async def slow(answer, exercise):
            await asyncio.sleep(0.05)
        rows = [{"learner_answer": "a", "exercise": {"answer": "a"}}]
        result = asyncio.run(measure_ai(rows, slow, timeout_seconds=0.001))
        self.assertEqual(result["failure_count"], 1)
        self.assertFalse(result["latency_gate"])

    def test_report_remains_blocked_even_with_verified_ci(self):
        sha = "a" * 40
        jobs = {name: {"status": "completed", "conclusion": "success"} for name in ("backend", "frontend", "e2e-mobile")}
        report = build_report(
            benchmark={"deterministic_latency_gate": True, "failure_rate": 0},
            linguistic={"release_checks": {}, "failed_gates": []},
            expected_sha=sha,
            job_evidence={"verified": True, "head_sha": sha, "jobs": jobs},
            ai_benchmark={"measured": True, "p95_ms": 1000, "failure_rate": 0},
        )
        self.assertTrue(report["checks"]["mobile_e2e_signoff"])
        self.assertTrue(report["checks"]["ai_assisted_performance"])
        self.assertEqual(report["release_gate"], "blocked")
        self.assertFalse(report["checks"]["external_human_signoff"])


if __name__ == "__main__":
    unittest.main()
