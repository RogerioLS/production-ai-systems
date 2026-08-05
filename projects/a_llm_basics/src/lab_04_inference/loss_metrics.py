"""Information theory metrics, loss analysis, PPL, and inference hardware cost modeling."""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from loguru import logger

from projects.a_llm_basics.src.lab_04_inference.exceptions import (
    InferenceError,
    MetricComputationError,
)


def compute_cross_entropy_loss(logits: torch.Tensor, targets: torch.Tensor) -> float:
    """Computes mean cross-entropy loss over target tokens.

    Args:
        logits: Tensor of shape (batch_size, seq_len, vocab_size) or (N, vocab_size).
        targets: Target token IDs of shape (batch_size, seq_len) or (N,).

    Returns:
        Cross-entropy loss scalar value.

    Raises:
        MetricComputationError: If shapes are incompatible or logits contain NaNs.
    """
    if torch.isnan(logits).any():
        raise MetricComputationError("Logits contain NaN values during loss calculation")

    try:
        logits_flat = logits.view(-1, logits.size(-1))
        targets_flat = targets.view(-1)
        loss = F.cross_entropy(logits_flat, targets_flat, reduction="mean").item()
        return float(loss)
    except Exception as err:
        logger.error("Cross entropy calculation failed: {}", err)
        raise MetricComputationError(f"Cross entropy error: {err}") from err


def compute_perplexity(cross_entropy_loss: float | torch.Tensor) -> float:
    """Calculates Perplexity (PPL) from cross-entropy loss value.

    Args:
        cross_entropy_loss: Float or scalar tensor loss.

    Returns:
        Perplexity value (exp(loss)).

    Raises:
        MetricComputationError: If loss is negative or infinite.
    """
    if isinstance(cross_entropy_loss, torch.Tensor):
        val = cross_entropy_loss.item()
    else:
        val = float(cross_entropy_loss)

    if val < 0 or math.isnan(val) or math.isinf(val):
        raise MetricComputationError(f"Invalid cross entropy loss value for perplexity: {val}")

    return float(math.exp(val))


def compute_shannon_entropy(probabilities: torch.Tensor, base: float = 2.0) -> torch.Tensor:
    """Calculates Shannon Information Entropy over probability distributions.

    H(P) = - sum P(x) * log_base P(x)

    Args:
        probabilities: Softmax probability tensor summing to 1.0 along last dimension.
        base: Logarithm base (default 2.0 for bits).

    Returns:
        Entropy tensor along sequence dimensions.
    """
    eps = 1e-12
    probs_clamped = torch.clamp(probabilities, min=eps)
    log_probs = torch.log(probs_clamped) / math.log(base)
    entropy = -torch.sum(probabilities * log_probs, dim=-1)
    return entropy


def compute_bits_per_byte(loss: float, bytes_per_token: float) -> float:
    """Converts nats cross-entropy loss to Bits-Per-Byte (BPB).

    Args:
        loss: Cross-entropy loss in nats (base e).
        bytes_per_token: Mean UTF-8 bytes per token for the domain dataset.

    Returns:
        BPB metric scalar.
    """
    if bytes_per_token <= 0:
        raise MetricComputationError(f"bytes_per_token must be positive, got {bytes_per_token}")
    bits_per_token = loss / math.log(2.0)
    return bits_per_token / bytes_per_token


class LossAnalyzer:
    """Provides sequence loss, entropy, and perplexity diagnostics."""

    @staticmethod
    def analyze(logits: torch.Tensor, targets: torch.Tensor) -> dict[str, float]:
        """Calculates loss, perplexity, and mean entropy metrics."""
        loss = compute_cross_entropy_loss(logits, targets)
        ppl = compute_perplexity(loss)
        probs = F.softmax(logits, dim=-1)
        entropy = compute_shannon_entropy(probs).mean().item()

        return {
            "cross_entropy_loss": loss,
            "perplexity": ppl,
            "mean_shannon_entropy_bits": float(entropy),
        }


class InferenceCostCalculator:
    """Calculates LLM VRAM memory footprint and FLOP compute requirements."""

    def __init__(
        self,
        num_layers: int,
        num_heads: int,
        head_dim: int,
        hidden_size: int,
        num_kv_heads: int | None = None,
    ) -> None:
        if min(num_layers, num_heads, head_dim, hidden_size) <= 0:
            raise InferenceError("All architecture parameters must be strictly positive")

        self.num_layers = num_layers
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.hidden_size = hidden_size
        self.num_kv_heads = num_kv_heads if num_kv_heads is not None else num_heads
        logger.info(
            "Initialized InferenceCostCalculator (L={}, H={}, H_kv={}, D={}, Hidden={})",
            num_layers,
            num_heads,
            self.num_kv_heads,
            head_dim,
            hidden_size,
        )

    def compute_model_param_bytes(self, num_params: int, precision_bytes: float = 2.0) -> int:
        """Calculates total model weight memory in bytes."""
        if num_params <= 0 or precision_bytes <= 0:
            raise InferenceError("Params count and precision_bytes must be positive")
        return int(num_params * precision_bytes)

    def compute_kv_cache_bytes(
        self, batch_size: int, seq_len: int, precision_bytes: float = 2.0
    ) -> int:
        """Calculates dynamic KV Cache memory requirement in bytes."""
        if batch_size <= 0 or seq_len <= 0 or precision_bytes <= 0:
            raise InferenceError("Batch size, seq_len, and precision_bytes must be positive")

        # 2 (Key + Value) * num_layers * num_kv_heads * head_dim * seq_len * batch_size * bytes
        total_elements = (
            2 * self.num_layers * self.num_kv_heads * self.head_dim * seq_len * batch_size
        )
        return int(total_elements * precision_bytes)

    def estimate_flops_per_token(
        self, num_params: int, seq_len: int, is_prefill: bool = False
    ) -> int:
        """Estimates FLOPs per token during prefill vs generation decoding."""
        if num_params <= 0 or seq_len <= 0:
            raise InferenceError("num_params and seq_len must be positive")

        weight_flops = 2 * num_params
        attention_flops = 2 * self.num_layers * self.hidden_size * seq_len
        total_flops = weight_flops + attention_flops

        if is_prefill:
            return total_flops * seq_len
        return total_flops

    def compute_max_batch_size(
        self,
        vram_capacity_bytes: int,
        num_params: int,
        seq_len: int,
        precision_bytes: float = 2.0,
        activation_buffer_bytes: int = 1_073_741_824,  # 1 GB
    ) -> int:
        """Calculates maximum supportable batch size under VRAM constraint."""
        weight_bytes = self.compute_model_param_bytes(num_params, precision_bytes)
        available_vram = vram_capacity_bytes - weight_bytes - activation_buffer_bytes

        if available_vram <= 0:
            return 0

        single_seq_kv_bytes = self.compute_kv_cache_bytes(
            batch_size=1, seq_len=seq_len, precision_bytes=precision_bytes
        )
        return int(available_vram // single_seq_kv_bytes)
