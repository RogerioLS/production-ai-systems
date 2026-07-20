import pytest
import torch

from projects.a_llm_basics.src.lab_03_attention.attention import (
    MultiHeadAttention,
    ScaledDotProductAttention,
)
from projects.a_llm_basics.src.lab_03_attention.exceptions import (
    DimensionMismatchError,
    InvalidMaskError,
)


def test_scaled_dot_product_attention_shapes():
    attention = ScaledDotProductAttention()

    batch_size = 2
    seq_len = 5
    d_k = 8
    d_v = 10

    q = torch.randn(batch_size, seq_len, d_k)
    k = torch.randn(batch_size, seq_len, d_k)
    v = torch.randn(batch_size, seq_len, d_v)

    output, weights = attention(q, k, v)

    assert output.shape == (batch_size, seq_len, d_v)
    assert weights.shape == (batch_size, seq_len, seq_len)


def test_attention_weights_sum_to_one():
    attention = ScaledDotProductAttention()

    q = torch.randn(1, 3, 4)
    k = torch.randn(1, 3, 4)
    v = torch.randn(1, 3, 4)

    _, weights = attention(q, k, v)

    # Weights along the key sequence length (dim=-1) should sum to 1.0
    summed_weights = weights.sum(dim=-1)
    assert torch.allclose(summed_weights, torch.ones_like(summed_weights))


def test_causal_masking():
    attention = ScaledDotProductAttention()

    seq_len = 4
    d_k = 6

    q = torch.randn(1, seq_len, d_k)
    k = torch.randn(1, seq_len, d_k)
    v = torch.randn(1, seq_len, d_k)

    # Causal mask: Lower triangular matrix of ones
    # 1 0 0 0
    # 1 1 0 0
    # 1 1 1 0
    # 1 1 1 1
    mask = torch.tril(torch.ones(seq_len, seq_len)).bool()

    _, weights = attention(q, k, v, mask=mask)

    # For the first query token, it can only attend to the first key token (index 0)
    # The rest (1, 2, 3) must be masked out (0.0 attention)
    assert torch.allclose(weights[0, 0, 1:], torch.zeros(3))

    # For the second query token, it can attend to indexes 0 and 1, but not 2 and 3
    assert torch.allclose(weights[0, 1, 2:], torch.zeros(2))

    # For the third query token, index 3 must be 0
    assert pytest.approx(weights[0, 2, 3].item()) == 0.0


def test_dimension_mismatch_raises_exception():
    attention = ScaledDotProductAttention()

    q = torch.randn(1, 3, 4)
    k = torch.randn(1, 3, 5)  # d_k mismatch (5 != 4)
    v = torch.randn(1, 3, 4)

    with pytest.raises(DimensionMismatchError):
        attention(q, k, v)

    k_correct = torch.randn(1, 3, 4)
    v_wrong_len = torch.randn(1, 4, 4)  # seq_len mismatch (4 != 3)

    with pytest.raises(DimensionMismatchError):
        attention(q, k_correct, v_wrong_len)


def test_invalid_mask_shape_raises_exception():
    attention = ScaledDotProductAttention()

    q = torch.randn(1, 3, 4)
    k = torch.randn(1, 3, 4)
    v = torch.randn(1, 3, 4)

    # Mask shape is incompatible (cannot be broadcast)
    invalid_mask = torch.ones(2, 5).bool()

    with pytest.raises(InvalidMaskError):
        attention(q, k, v, mask=invalid_mask)


def test_multi_head_attention_shapes():
    mha = MultiHeadAttention(d_model=16, n_heads=4)

    batch_size = 3
    seq_len_q = 6
    seq_len_k = 8

    q = torch.randn(batch_size, seq_len_q, 16)
    k = torch.randn(batch_size, seq_len_k, 16)
    v = torch.randn(batch_size, seq_len_k, 16)

    output, weights = mha(q, k, v)

    assert output.shape == (batch_size, seq_len_q, 16)
    assert weights.shape == (batch_size, 4, seq_len_q, seq_len_k)


def test_multi_head_attention_invalid_d_model():
    with pytest.raises(DimensionMismatchError):
        # 16 is not divisible by 5
        MultiHeadAttention(d_model=16, n_heads=5)


def test_multi_head_attention_forward_dimension_mismatch():
    mha = MultiHeadAttention(d_model=16, n_heads=4)

    q = torch.randn(2, 4, 16)
    k = torch.randn(2, 4, 15)  # wrong d_model (15 != 16)
    v = torch.randn(2, 4, 16)

    with pytest.raises(DimensionMismatchError):
        mha(q, k, v)
