from app.services.bot_links import (
    build_web_app_url,
    invite_code_from_payload,
    parse_start_payload,
    telegram_beta_invite_url,
)


def test_parses_beta_invite_start_payload():
    payload = parse_start_payload("/start invite_eabe50d5c256")
    assert payload == "invite_eabe50d5c256"
    assert invite_code_from_payload(payload) == "EABE50D5C256"


def test_rejects_non_invite_and_malformed_payloads():
    assert invite_code_from_payload("subscribe") is None
    assert invite_code_from_payload("invite_not-a-code") is None
    assert parse_start_payload("/start") == ""


def test_carries_invite_into_web_app_url_without_losing_existing_query():
    url = build_web_app_url("https://deutschiq.example/?source=telegram", invite="EABE50D5C256")
    assert url == "https://deutschiq.example/?source=telegram&invite=EABE50D5C256"


def test_builds_telegram_native_beta_link():
    assert telegram_beta_invite_url("@DeutschIQ_bot", "eabe50d5c256") == (
        "https://t.me/DeutschIQ_bot?start=invite_EABE50D5C256"
    )
