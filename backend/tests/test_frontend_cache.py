from app.core.cloud_runtime import cache_control_for_path


def test_fingerprinted_assets_are_cached_immutably():
    assert cache_control_for_path("/assets/index-AbCd1234.js", "text/javascript") == (
        "public, max-age=31536000, immutable"
    )


def test_spa_shell_is_revalidated_without_forcing_redownload():
    assert cache_control_for_path("/dashboard", "text/html; charset=utf-8") == "no-cache"
    assert cache_control_for_path("/", "text/html; charset=utf-8") == "no-cache"


def test_versioned_lesson_audio_is_cached_immutably():
    assert cache_control_for_path("/media/audio/a1/greetings/model.mp3", "audio/mpeg") == (
        "public, max-age=31536000, immutable"
    )


def test_api_responses_do_not_receive_frontend_cache_policy():
    assert cache_control_for_path("/api/dashboard/123", "application/json") is None