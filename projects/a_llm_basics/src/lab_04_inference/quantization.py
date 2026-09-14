"""Uniform linear quantization routines, precision reduction, and reconstruction metrics."""

from __future__ import annotations

from typing import Tuple

import torch
from loguru import logger

from projects.a_llm_basics.src.lab_04_inference.exceptions import QuantizationError


def quantize_symmetric(tensor: torch.Tensor, num_bits: int = 8) -> Tuple[torch.Tensor, float, int]:
    """Quantizes floating-point tensor to symmetric integer range.

    Args:
        tensor: Input float tensor.
        num_bits: Bit precision (supported: 4, 8, 16).

    Returns:
        Tuple of (quantized_tensor, scale, zero_point=0).

    Raises:
        QuantizationError: If num_bits is invalid.
    """
    if num_bits not in (4, 8, 16):
        logger.error("Unsupported bit precision: {}", num_bits)
        raise QuantizationError(f"Supported bits are (4, 8, 16), got {num_bits}")

    q_max = (1 << (num_bits - 1)) - 1
    q_min = -(1 << (num_bits - 1))

    max_abs = torch.max(torch.abs(tensor)).item()
    if max_abs == 0.0:
        scale = 1.0
    else:
        scale = max_abs / q_max

    if scale <= 0.0:
        raise QuantizationError(f"Invalid scale factor computed: {scale}")

    q_tensor = torch.clamp(torch.round(tensor / scale), q_min, q_max)
    if num_bits == 8:
        q_tensor = q_tensor.to(torch.int8)

    logger.debug("Symmetric quantization (bits={}): scale={}", num_bits, scale)
    return q_tensor, scale, 0


def dequantize_symmetric(q_tensor: torch.Tensor, scale: float) -> torch.Tensor:
    """Dequantizes symmetric integer tensor back to float representation.

    Args:
        q_tensor: Quantized integer tensor.
        scale: Scale factor.

    Returns:
        Floating point reconstructed tensor.
    """
    if scale <= 0.0:
        raise QuantizationError(f"Scale must be positive, got {scale}")
    return q_tensor.float() * scale


def quantize_asymmetric(tensor: torch.Tensor, num_bits: int = 8) -> Tuple[torch.Tensor, float, int]:
    """Quantizes floating-point tensor to asymmetric unsigned integer range.

    Args:
        tensor: Input float tensor.
        num_bits: Bit precision (supported: 4, 8, 16).

    Returns:
        Tuple of (quantized_tensor, scale, zero_point).

    Raises:
        QuantizationError: If num_bits is invalid.
    """
    if num_bits not in (4, 8, 16):
        logger.error("Unsupported bit precision: {}", num_bits)
        raise QuantizationError(f"Supported bits are (4, 8, 16), got {num_bits}")

    q_min = 0
    q_max = (1 << num_bits) - 1

    x_min = tensor.min().item()
    x_max = tensor.max().item()

    denom = x_max - x_min
    if denom == 0.0:
        scale = 1.0
        zero_point = 0
    else:
        scale = denom / q_max
        zero_point = int(round(-x_min / scale))
        zero_point = max(q_min, min(q_max, zero_point))

    if scale <= 0.0:
        raise QuantizationError(f"Invalid scale factor computed: {scale}")

    q_tensor = torch.clamp(torch.round(tensor / scale) + zero_point, q_min, q_max)
    if num_bits == 8:
        q_tensor = q_tensor.to(torch.uint8)

    logger.debug(
        "Asymmetric quantization (bits={}): scale={}, zero_point={}", num_bits, scale, zero_point
    )
    return q_tensor, scale, zero_point


def dequantize_asymmetric(q_tensor: torch.Tensor, scale: float, zero_point: int) -> torch.Tensor:
    """Dequantizes asymmetric integer tensor back to float representation.

    Args:
        q_tensor: Quantized integer tensor.
        scale: Scale factor.
        zero_point: Zero-point offset.

    Returns:
        Floating point reconstructed tensor.
    """
    if scale <= 0.0:
        raise QuantizationError(f"Scale must be positive, got {scale}")
    return (q_tensor.float() - zero_point) * scale


def compute_quantization_error(
    original: torch.Tensor, dequantized: torch.Tensor
) -> dict[str, float]:
    """Calculates precision loss metrics between original and reconstructed tensors.

    Args:
        original: Original floating point tensor.
        dequantized: Dequantized reconstructed float tensor.

    Returns:
        Dictionary containing MSE, MAE, Cosine Similarity, and SQNR (dB).
    """
    orig_flat = original.view(-1).float()
    deq_flat = dequantized.view(-1).float()

    diff = orig_flat - deq_flat
    mse = torch.mean(diff**2).item()
    mae = torch.mean(torch.abs(diff)).item()

    # Cosine Similarity
    norm_orig = torch.linalg.norm(orig_flat)
    norm_deq = torch.linalg.norm(deq_flat)
    if norm_orig == 0 or norm_deq == 0:
        cos_sim = 1.0 if norm_orig == norm_deq else 0.0
    else:
        cos_sim = (torch.dot(orig_flat, deq_flat) / (norm_orig * norm_deq)).item()

    # Signal-to-Quantization-Noise Ratio (SQNR in dB)
    signal_power = torch.sum(orig_flat**2).item()
    noise_power = torch.sum(diff**2).item()

    if noise_power == 0:
        sqnr_db = float("inf")
    else:
        sqnr_db = 10.0 * torch.log10(torch.tensor(signal_power / noise_power)).item()

    return {
        "mse": float(mse),
        "mae": float(mae),
        "cosine_similarity": float(cos_sim),
        "sqnr_db": float(sqnr_db),
    }


class UniformQuantizer:
    """Configurable linear uniform quantizer."""

    def __init__(self, num_bits: int = 8, symmetric: bool = True) -> None:
        if num_bits not in (4, 8, 16):
            raise QuantizationError(f"Supported bits are (4, 8, 16), got {num_bits}")

        self.num_bits = num_bits
        self.symmetric = symmetric

    def quantize(self, tensor: torch.Tensor) -> Tuple[torch.Tensor, float, int]:
        """Quantizes input tensor based on configured mode."""
        if self.symmetric:
            return quantize_symmetric(tensor, self.num_bits)
        return quantize_asymmetric(tensor, self.num_bits)

    def dequantize(self, q_tensor: torch.Tensor, scale: float, zero_point: int = 0) -> torch.Tensor:
        """Dequantizes input integer tensor based on configured mode."""
        if self.symmetric:
            return dequantize_symmetric(q_tensor, scale)
        return dequantize_asymmetric(q_tensor, scale, zero_point)

    def evaluate(self, tensor: torch.Tensor) -> dict[str, float]:
        """Quantizes, dequantizes, and evaluates signal preservation metrics."""
        q_tensor, scale, zero_point = self.quantize(tensor)
        deq_tensor = self.dequantize(q_tensor, scale, zero_point)
        return compute_quantization_error(tensor, deq_tensor)
