import math
from typing import Optional, Tuple

import torch
import torch.nn as nn
from loguru import logger

from projects.a_llm_basics.src.lab_03_attention.exceptions import (
    DimensionMismatchError,
    InvalidMaskError,
)


class ScaledDotProductAttention(nn.Module):
    """Computes Scaled Dot-Product Attention as described in 'Attention Is All You Need'."""

    def __init__(self, dropout: float = 0.0) -> None:
        super().__init__()
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Runs the forward pass for Scaled Dot-Product Attention.

        Args:
            query: Query tensor of shape (..., seq_len_q, d_k)
            key: Key tensor of shape (..., seq_len_k, d_k)
            value: Value tensor of shape (..., seq_len_k, d_v)
            mask: Optional mask tensor of shape (..., seq_len_q, seq_len_k)
                  or broadcastable shape. Boolean where False indicates mask.

        Returns:
            A tuple of (output, attention_weights) where:
                output: Context vector tensor of shape (..., seq_len_q, d_v)
                attention_weights: Weights of shape (..., seq_len_q, seq_len_k)
        """
        # Validate dimensions
        d_k = query.size(-1)
        if key.size(-1) != d_k:
            raise DimensionMismatchError(
                f"Query dimension d_k ({d_k}) must match Key dimension d_k ({key.size(-1)})."
            )
        if key.size(-2) != value.size(-2):
            msg = (
                f"Key sequence length ({key.size(-2)}) must match "
                f"Value sequence length ({value.size(-2)})."
            )
            raise DimensionMismatchError(msg)

        # Calculate raw attention scores: Q K^T / sqrt(d_k)
        # query shape: (..., seq_len_q, d_k)
        # key shape: (..., seq_len_k, d_k) -> transpose last two dimensions
        scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)

        # Apply mask if present
        if mask is not None:
            # Validate mask shape compatibility with scores
            try:
                # We check if mask is broadcastable to scores shape
                torch.broadcast_shapes(mask.shape, scores.shape)
            except RuntimeError as e:
                msg = (
                    f"Mask shape {mask.shape} is incompatible with "
                    f"attention scores shape {scores.shape}. Details: {e}"
                )
                raise InvalidMaskError(msg) from e

            # If mask is boolean, False means mask out. If mask is numeric, 0 means mask out.
            if mask.dtype == torch.bool:
                scores = scores.masked_fill(~mask, float("-inf"))
            else:
                scores = scores.masked_fill(mask == 0, float("-inf"))

        # Calculate attention weights (softmax over the last dimension)
        attention_weights = torch.softmax(scores, dim=-1)

        # Handle nan values that might occur if a whole row is masked out
        if torch.isnan(attention_weights).any():
            logger.warning("NaN values detected in attention weights. Replacing with 0.")
            attention_weights = torch.nan_to_num(attention_weights, nan=0.0)

        # Apply dropout if configured
        if self.dropout is not None:
            attention_weights = self.dropout(attention_weights)

        # Compute context output: AttentionWeights * V
        output = torch.matmul(attention_weights, value)

        return output, attention_weights


class MultiHeadAttention(nn.Module):
    """Implements Multi-Head Attention architecture from 'Attention Is All You Need'."""

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.0) -> None:
        """Initializes the Multi-Head Attention module.

        Args:
            d_model: Dimensionality of the model's hidden representation.
            n_heads: Number of parallel attention heads.
            dropout: Dropout probability.

        Raises:
            DimensionMismatchError: If d_model is not divisible by n_heads.
        """
        super().__init__()
        if d_model % n_heads != 0:
            raise DimensionMismatchError(
                f"d_model ({d_model}) must be divisible by n_heads ({n_heads})."
            )

        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        # Linear projections for Q, K, V
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)

        # Output projection
        self.out_proj = nn.Linear(d_model, d_model)

        # Scaled dot product attention module
        self.attention = ScaledDotProductAttention(dropout=dropout)

        logger.info(f"Initialized MHA: d_model={d_model}, n_heads={n_heads}, d_k={self.d_k}")

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Runs the forward pass for Multi-Head Attention.

        Args:
            query: Query tensor of shape (batch_size, seq_len_q, d_model)
            key: Key tensor of shape (batch_size, seq_len_k, d_model)
            value: Value tensor of shape (batch_size, seq_len_k, d_model)
            mask: Optional mask tensor. Can be causality mask or padding mask.
                  Shape is typically (batch_size, 1, 1, seq_len_k) or
                  (batch_size, 1, seq_len_q, seq_len_k) to broadcast.

        Returns:
            A tuple of (output, attention_weights) where:
                output: Context tensor of shape (batch_size, seq_len_q, d_model)
                attention_weights: Weights of shape (batch_size, n_heads, seq_len_q, seq_len_k)
        """
        batch_size, seq_len_q, d_model_q = query.size()
        _, seq_len_k, d_model_k = key.size()
        _, seq_len_v, d_model_v = value.size()

        if d_model_q != self.d_model or d_model_k != self.d_model or d_model_v != self.d_model:
            raise DimensionMismatchError(
                f"Input tensor features ({d_model_q}, {d_model_k}, {d_model_v}) "
                f"must match configured d_model ({self.d_model})."
            )

        # Linear projections & split into heads
        # (batch_size, seq_len, d_model) -> (batch_size, seq_len, n_heads, d_k) ->
        # (batch_size, n_heads, seq_len, d_k)
        q = self.q_proj(query).view(batch_size, seq_len_q, self.n_heads, self.d_k).transpose(1, 2)
        k = self.k_proj(key).view(batch_size, seq_len_k, self.n_heads, self.d_k).transpose(1, 2)
        v = self.v_proj(value).view(batch_size, seq_len_v, self.n_heads, self.d_k).transpose(1, 2)

        # Apply scaled dot product attention
        # ScaledDotProductAttention expects shape (batch_size, n_heads, seq_len_q, seq_len_k)
        attn_out, attn_weights = self.attention(q, k, v, mask=mask)

        # Concatenate heads
        # (batch_size, n_heads, seq_len_q, d_k) -> (batch_size, seq_len_q, n_heads, d_k) ->
        # (batch_size, seq_len_q, d_model)
        attn_out = attn_out.transpose(1, 2).contiguous().view(batch_size, seq_len_q, self.d_model)

        # Apply output linear projection
        output = self.out_proj(attn_out)

        return output, attn_weights
