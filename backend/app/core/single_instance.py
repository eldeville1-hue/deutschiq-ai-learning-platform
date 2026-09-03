import hashlib
import os
import sys


_instance_handle = None


def acquire_bot_lock(token: str) -> None:
    """Keep exactly one polling process per bot token on this machine."""
    global _instance_handle
    suffix = hashlib.sha256(token.encode("utf-8")).hexdigest()[:12]
    if sys.platform == "win32":
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.CreateMutexW(None, False, f"Local\\DeutschIQBot-{suffix}")
        if not handle or kernel32.GetLastError() == 183:
            raise SystemExit("❌ DeutschIQ bot уже запущен на этом компьютере. Закройте старое окно бота.")
        _instance_handle = handle
        return

    import fcntl

    path = f"/tmp/deutschiq-bot-{os.getuid()}-{suffix}.lock"
    handle = open(path, "w", encoding="utf-8")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        handle.close()
        raise SystemExit("❌ DeutschIQ bot уже запущен на этом компьютере.") from exc
    handle.write(str(os.getpid()))
    handle.flush()
    _instance_handle = handle
