"""Domain errors shared by the engine modules."""


class EngineError(Exception):
    """Base class for recoverable engine failures."""


class MissingCredentialError(EngineError):
    """Raised when an engine needs an API key that is not configured."""

    def __init__(self, name: str) -> None:
        super().__init__(f"{name} is not configured")
        self.name = name


class UpstreamError(EngineError):
    """Raised when a third-party provider returns an unexpected response."""

    def __init__(self, provider: str, status_code: int) -> None:
        super().__init__(f"{provider} responded with status {status_code}")
        self.provider = provider
        self.status_code = status_code
