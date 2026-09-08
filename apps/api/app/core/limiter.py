"""Shared rate-limiter instance.

Imported by main.py (to register the exception handler) and by route
modules (to apply @limiter.limit decorators) — a single module avoids
the circular import that would result from importing from main.py.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Note: default_limits is omitted because SlowAPI's middleware does not resolve
# endpoints inside FastAPI's _IncludedRouter sub-routers (exempting them). All limits
# are explicitly applied via @limiter.limit decorators on individual routes.
limiter = Limiter(key_func=get_remote_address)
