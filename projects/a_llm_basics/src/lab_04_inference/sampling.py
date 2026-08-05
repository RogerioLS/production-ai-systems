"""Logit transformation pipelines and categorical token sampling algorithms."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from loguru import logger

from projects.a_llm_basics.src.lab_04_inference.exceptions import SamplingError


def apply_temperature(logits: torch.Tensor, temperature: float) -> torch.Tensor:
    """Scales raw logits by inverse temperature.

    Args:
        logits: Tensor of unnormalized log probabilities.
        temperature: Temperature parameter T > 0.

    Returns:
        Scaled logits tensor.

    Raises:
        SamplingError: If temperature <= 0 or logits contain NaN/Inf.
    """
    if temperature <= 0.0:
        logger.error("Invalid temperature factor: {}", temperature)
        raise SamplingError(f"Temperature must be strictly positive, got {temperature}")

    if torch.isnan(logits).any() or torch.isinf(logits).any():
        logger.error("Logits contain NaN or Inf values")
        raise SamplingError("Logits contain NaN or Inf values")

    logger.debug("Applying temperature scaling T={} to logits shape {}", temperature, logits.shape)
    return logits / temperature


def apply_repetition_penalty(
    logits: torch.Tensor, input_ids: torch.Tensor, penalty: float = 1.0
) -> torch.Tensor:
    """Applies repetition penalty to logits corresponding to previously generated tokens.

    Args:
        logits: Logits tensor of shape (batch_size, vocab_size) or (vocab_size,).
        input_ids: Previously generated token IDs.
        penalty: Penalty factor theta >= 1.0.

    Returns:
        Logits tensor with penalized values.

    Raises:
        SamplingError: If penalty < 1.0.
    """
    if penalty < 1.0:
        logger.error("Invalid repetition penalty factor: {}", penalty)
        raise SamplingError(f"Repetition penalty must be >= 1.0, got {penalty}")

    if penalty == 1.0 or input_ids.numel() == 0:
        return logits

    logits_clone = logits.clone()
    unique_ids = torch.unique(input_ids)

    if logits_clone.ndim == 1:
        score = logits_clone[unique_ids]
        logits_clone[unique_ids] = torch.where(score < 0, score * penalty, score / penalty)
    else:
        for b in range(logits_clone.size(0)):
            b_unique = torch.unique(input_ids[b])
            score = logits_clone[b, b_unique]
            logits_clone[b, b_unique] = torch.where(score < 0, score * penalty, score / penalty)

    return logits_clone


def apply_top_k(logits: torch.Tensor, top_k: int) -> torch.Tensor:
    """Masks logits outside the top K candidate values to -inf.

    Args:
        logits: Logits tensor.
        top_k: Top K threshold.

    Returns:
        Filtered logits tensor.

    Raises:
        SamplingError: If top_k < 0.
    """
    if top_k < 0:
        logger.error("Invalid top_k: {}", top_k)
        raise SamplingError(f"top_k must be >= 0, got {top_k}")

    if top_k == 0 or top_k >= logits.size(-1):
        return logits

    logits_clone = logits.clone()
    top_k_val = min(top_k, logits_clone.size(-1))
    top_k_values, _ = torch.topk(logits_clone, top_k_val, dim=-1)
    cutoff = top_k_values[..., -1:]
    logits_clone[logits_clone < cutoff] = float("-inf")
    return logits_clone


def apply_top_p(logits: torch.Tensor, top_p: float) -> torch.Tensor:
    """Applies Top-P (Nucleus) filtering by cumulative probability cutoff.

    Args:
        logits: Logits tensor.
        top_p: Cumulative probability mass threshold in range (0.0, 1.0].

    Returns:
        Filtered logits tensor.

    Raises:
        SamplingError: If top_p <= 0.0 or top_p > 1.0.
    """
    if not (0.0 < top_p <= 1.0):
        logger.error("Invalid top_p: {}", top_p)
        raise SamplingError(f"top_p must be in (0.0, 1.0], got {top_p}")

    if top_p == 1.0:
        return logits

    logits_clone = logits.clone()
    sorted_logits, sorted_indices = torch.sort(logits_clone, descending=True, dim=-1)
    sorted_probs = F.softmax(sorted_logits, dim=-1)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

    # Mask out tokens whose cumulative probability exceeds top_p
    sorted_indices_to_remove = cumulative_probs > top_p
    # Keep the first token that exceeds top_p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = False

    indices_to_remove = sorted_indices_to_remove.scatter(
        dim=-1, index=sorted_indices, src=sorted_indices_to_remove
    )
    logits_clone[indices_to_remove] = float("-inf")
    return logits_clone


def apply_min_p(logits: torch.Tensor, min_p: float) -> torch.Tensor:
    """Filters tokens whose probability is below min_p * max_prob.

    Args:
        logits: Logits tensor.
        min_p: Min-P relative threshold in range [0.0, 1.0).

    Returns:
        Filtered logits tensor.

    Raises:
        SamplingError: If min_p < 0.0 or min_p >= 1.0.
    """
    if not (0.0 <= min_p < 1.0):
        logger.error("Invalid min_p: {}", min_p)
        raise SamplingError(f"min_p must be in [0.0, 1.0), got {min_p}")

    if min_p == 0.0:
        return logits

    probs = F.softmax(logits, dim=-1)
    max_probs, _ = torch.max(probs, dim=-1, keepdim=True)
    scaled_min_p = max_probs * min_p

    logits_clone = logits.clone()
    logits_clone[probs < scaled_min_p] = float("-inf")
    return logits_clone


def sample_next_token(
    logits: torch.Tensor,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    min_p: float = 0.0,
    repetition_penalty: float = 1.0,
    input_ids: torch.Tensor | None = None,
    do_sample: bool = True,
) -> torch.Tensor:
    """Executes the full logit transformation pipeline and samples token IDs.

    Args:
        logits: Unnormalized log probability tensor.
        temperature: Temperature factor.
        top_k: Top-K filter threshold.
        top_p: Top-P nucleus threshold.
        min_p: Min-P relative threshold.
        repetition_penalty: Repetition penalty multiplier.
        input_ids: Previously generated sequence tokens for penalty application.
        do_sample: If False, performs deterministic greedy decoding (argmax).

    Returns:
        Sampled token index tensor of shape (batch_size, 1).
    """
    if not do_sample:
        return torch.argmax(logits, dim=-1, keepdim=True)

    if input_ids is not None and repetition_penalty > 1.0:
        logits = apply_repetition_penalty(logits, input_ids, repetition_penalty)

    logits = apply_temperature(logits, temperature)
    logits = apply_top_k(logits, top_k)
    logits = apply_top_p(logits, top_p)
    logits = apply_min_p(logits, min_p)

    probs = F.softmax(logits, dim=-1)

    if logits.ndim == 1:
        return torch.multinomial(probs, num_samples=1)
    return torch.multinomial(probs, num_samples=1)


class SamplingEngine:
    """Configurable sampling engine encapsulating logit transformations."""

    def __init__(
        self,
        temperature: float = 1.0,
        top_k: int = 0,
        top_p: float = 1.0,
        min_p: float = 0.0,
        repetition_penalty: float = 1.0,
    ) -> None:
        if temperature <= 0.0:
            raise SamplingError(f"Temperature must be positive, got {temperature}")
        if not (0.0 < top_p <= 1.0):
            raise SamplingError(f"top_p must be in (0.0, 1.0], got {top_p}")

        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.min_p = min_p
        self.repetition_penalty = repetition_penalty
        logger.info(
            "Initialized SamplingEngine (T={}, top_k={}, top_p={}, min_p={})",
            temperature,
            top_k,
            top_p,
            min_p,
        )

    def sample(
        self,
        logits: torch.Tensor,
        input_ids: torch.Tensor | None = None,
        do_sample: bool = True,
    ) -> torch.Tensor:
        """Samples next token IDs given input logits."""
        return sample_next_token(
            logits=logits,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            min_p=self.min_p,
            repetition_penalty=self.repetition_penalty,
            input_ids=input_ids,
            do_sample=do_sample,
        )
