import os

# These two values are now required by Settings (no default).
# Set them before any app module is imported so collection does not raise ValidationError.
# A real env var in the shell always wins — os.environ.setdefault only fires when nothing is set.
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/tenspilot")
os.environ.setdefault("API_SECRET_KEY", "test-secret-key-not-for-production")
