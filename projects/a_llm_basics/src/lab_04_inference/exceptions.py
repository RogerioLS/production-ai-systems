"""Domain custom exceptions for LAB-04 Inference Math."""


class InferenceError(Exception):
    """Base exception class for all inference math module errors."""

    pass


class SamplingError(InferenceError):
    """Raised when sampling parameters are invalid or logits processing fails."""

    pass


class QuantizationError(InferenceError):
    """Raised when quantization parameters or bounds are violated."""

    pass


class MetricComputationError(InferenceError):
    """Raised when metric calculations encounter numerical instabilities."""

    pass
