"""Small, testable HTTP hardening helpers."""


SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), geolocation=(), payment=()",
    "Cross-Origin-Opener-Policy": "same-origin-allow-popups",
}


def apply_security_headers(response, *, secure: bool) -> None:
    for name, value in SECURITY_HEADERS.items():
        response.headers[name] = value
    if secure:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
