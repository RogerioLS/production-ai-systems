class AttentionError(Exception):
    """Base exception class for attention module errors."""

    pass


class DimensionMismatchError(AttentionError):
    """Exception raised when input dimensions do not match expected architecture configuration."""

    pass


class InvalidMaskError(AttentionError):
    """Exception raised when the provided mask has an invalid shape or data type."""

    pass
