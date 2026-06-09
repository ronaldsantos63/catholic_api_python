class LiturgyError(Exception):
    """Base exception for liturgy extraction failures."""


class LiturgyNotFoundError(LiturgyError):
    """Raised when the requested liturgy cannot be found."""


class ExternalSourceError(LiturgyError):
    """Raised when the external liturgy source cannot be reached."""


class InvalidLiturgySourceError(LiturgyError):
    """Raised when the external source response is not in the expected shape."""

