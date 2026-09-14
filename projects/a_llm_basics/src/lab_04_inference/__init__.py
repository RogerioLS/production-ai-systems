"""Public API exports for LAB-04 Inference Math."""

from projects.a_llm_basics.src.lab_04_inference.exceptions import (
    InferenceError,
    MetricComputationError,
    QuantizationError,
    SamplingError,
)
from projects.a_llm_basics.src.lab_04_inference.loss_metrics import (
    InferenceCostCalculator,
    LossAnalyzer,
    compute_bits_per_byte,
    compute_cross_entropy_loss,
    compute_perplexity,
    compute_shannon_entropy,
)
from projects.a_llm_basics.src.lab_04_inference.quantization import (
    UniformQuantizer,
    compute_quantization_error,
    dequantize_asymmetric,
    dequantize_symmetric,
    quantize_asymmetric,
    quantize_symmetric,
)
from projects.a_llm_basics.src.lab_04_inference.sampling import (
    SamplingEngine,
    apply_min_p,
    apply_repetition_penalty,
    apply_temperature,
    apply_top_k,
    apply_top_p,
    sample_next_token,
)

__all__ = [
    "InferenceError",
    "SamplingError",
    "QuantizationError",
    "MetricComputationError",
    "SamplingEngine",
    "apply_temperature",
    "apply_repetition_penalty",
    "apply_top_k",
    "apply_top_p",
    "apply_min_p",
    "sample_next_token",
    "UniformQuantizer",
    "quantize_symmetric",
    "dequantize_symmetric",
    "quantize_asymmetric",
    "dequantize_asymmetric",
    "compute_quantization_error",
    "LossAnalyzer",
    "InferenceCostCalculator",
    "compute_cross_entropy_loss",
    "compute_perplexity",
    "compute_shannon_entropy",
    "compute_bits_per_byte",
]
