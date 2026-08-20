"""Security helpers (token hashing, API key checks)."""

import hashlib
import hmac

from app.core.config import settings


def sign(value: str) -> str:
    return hmac.new(settings.api_secret_key.encode(), value.encode(), hashlib.sha256).hexdigest()


def verify(value: str, signature: str) -> bool:
    return hmac.compare_digest(sign(value), signature)
