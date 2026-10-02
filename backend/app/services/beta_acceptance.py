"""Required human acceptance checks for the closed A1 beta.

Automated browser checks are useful, but they cannot certify Telegram WebView,
permission, interruption, or hardware behavior. These checks stay false until an
owner records a successful run on a real device.
"""

ACCEPTANCE_CATALOG = (
    ("iphone_journey", "iPhone Telegram: diagnostic → lesson → review → checkpoint"),
    ("android_journey", "Android Telegram: diagnostic → lesson → review → checkpoint"),
    ("small_screen", "320–375 px: no clipped controls or horizontal scrolling"),
    ("offline_recovery", "Offline/reconnect: saved progress resumes without a reload loop"),
    ("audio_interruption", "Audio interruption/minimize: playback pauses and resumes safely"),
    ("microphone_denied", "Microphone denied: learner can continue without a dead end"),
    ("cold_reopen", "Telegram closed/reopened: active lesson and draft are restored"),
)


def acceptance_report(rows) -> dict:
    stored = {row.check_id: row for row in rows}
    checks = []
    for check_id, label in ACCEPTANCE_CATALOG:
        row = stored.get(check_id)
        checks.append({
            "id": check_id,
            "label": label,
            "passed": bool(row and row.passed),
            "notes": (row.notes or "") if row else "",
            "updated_at": row.updated_at.isoformat() if row and row.updated_at else None,
        })
    passed = sum(item["passed"] for item in checks)
    return {"checks": checks, "passed": passed, "required": len(checks), "complete": passed == len(checks)}
