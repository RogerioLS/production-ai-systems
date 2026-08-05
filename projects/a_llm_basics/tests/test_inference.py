"""Comprehensive unit test suite for LAB-04 Inference Math."""

import math

import pytest
import torch

from projects.a_llm_basics.src.lab_04_inference.exceptions import (
    InferenceError,
    QuantizationError,
    SamplingError,
)
from projects.a_llm_basics.src.lab_04_inference.loss_metrics import (
    InferenceCostCalculator,
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
)

# ============================================================================
# 1. Sampling & Logit Processing Tests
# ============================================================================


def test_temperature_scaling_valid():
    logits = torch.tensor([2.0, 4.0, 6.0])
    scaled = apply_temperature(logits, temperature=2.0)
    assert torch.allclose(scaled, torch.tensor([1.0, 2.0, 3.0]))


def test_temperature_scaling_invalid_bounds():
    logits = torch.tensor([1.0, 2.0])
    with pytest.raises(SamplingError, match="Temperature must be strictly positive"):
        apply_temperature(logits, temperature=0.0)

    with pytest.raises(SamplingError, match="Temperature must be strictly positive"):
        apply_temperature(logits, temperature=-0.5)


def test_temperature_scaling_nan_inf_guard():
    nan_logits = torch.tensor([1.0, float("nan")])
    inf_logits = torch.tensor([float("inf"), 2.0])

    with pytest.raises(SamplingError, match="NaN or Inf"):
        apply_temperature(nan_logits, temperature=1.0)

    with pytest.raises(SamplingError, match="NaN or Inf"):
        apply_temperature(inf_logits, temperature=1.0)


def test_repetition_penalty():
    logits = torch.tensor([2.0, -1.0, 4.0])
    input_ids = torch.tensor([0, 1])  # Token 0 (>0) and token 1 (<0)

    penalized = apply_repetition_penalty(logits, input_ids, penalty=2.0)
    # Token 0 (2.0 > 0) -> 2.0 / 2.0 = 1.0
    # Token 1 (-1.0 < 0) -> -1.0 * 2.0 = -2.0
    # Token 2 (unpenalized) -> 4.0
    assert torch.allclose(penalized, torch.tensor([1.0, -2.0, 4.0]))


def test_repetition_penalty_invalid():
    logits = torch.tensor([1.0, 2.0])
    input_ids = torch.tensor([0])
    with pytest.raises(SamplingError, match="Repetition penalty must be >= 1.0"):
        apply_repetition_penalty(logits, input_ids, penalty=0.5)


def test_top_k_filtering():
    logits = torch.tensor([1.0, 5.0, 2.0, 10.0, 0.5])
    filtered = apply_top_k(logits, top_k=2)

    # Top 2 are 10.0 and 5.0. Others should be -inf
    assert filtered[3] == 10.0
    assert filtered[1] == 5.0
    assert filtered[0] == float("-inf")
    assert filtered[2] == float("-inf")
    assert filtered[4] == float("-inf")


def test_top_k_invalid():
    logits = torch.tensor([1.0, 2.0])
    with pytest.raises(SamplingError, match="top_k must be >= 0"):
        apply_top_k(logits, top_k=-1)


def test_top_p_nucleus_filtering():
    logits = torch.tensor([10.0, 1.0, 0.1, 0.01])
    filtered = apply_top_p(logits, top_p=0.6)

    # Token 0 covers > 60% mass, others masked to -inf
    assert filtered[0] == 10.0
    assert torch.isinf(filtered[1])
    assert torch.isinf(filtered[2])
    assert torch.isinf(filtered[3])


def test_top_p_invalid():
    logits = torch.tensor([1.0, 2.0])
    with pytest.raises(SamplingError, match="top_p must be in"):
        apply_top_p(logits, top_p=0.0)

    with pytest.raises(SamplingError, match="top_p must be in"):
        apply_top_p(logits, top_p=1.5)


def test_min_p_filtering():
    # Logits where max prob is high
    logits = torch.tensor([10.0, 5.0, 1.0])
    filtered = apply_min_p(logits, min_p=0.1)
    # Should filter low probability tail
    assert not torch.isinf(filtered[0])


def test_min_p_invalid():
    logits = torch.tensor([1.0, 2.0])
    with pytest.raises(SamplingError, match="min_p must be in"):
        apply_min_p(logits, min_p=-0.1)


def test_sampling_engine_greedy():
    logits = torch.tensor([[1.0, 5.0, 2.0]])
    engine = SamplingEngine(temperature=1.0)
    token = engine.sample(logits, do_sample=False)
    assert token.item() == 1


def test_sampling_engine_stochastic():
    logits = torch.tensor([[10.0, 0.1, 0.1]])
    engine = SamplingEngine(temperature=0.1, top_k=2, top_p=0.9)
    token = engine.sample(logits, do_sample=True)
    assert token.item() == 0


# ============================================================================
# 2. Quantization & Precision Loss Tests
# ============================================================================


def test_symmetric_quantization_roundtrip():
    tensor = torch.tensor([-1.0, 0.0, 0.5, 1.0])
    q_tensor, scale, zero_point = quantize_symmetric(tensor, num_bits=8)
    assert zero_point == 0
    recon = dequantize_symmetric(q_tensor, scale)

    mse = torch.mean((tensor - recon) ** 2).item()
    assert mse < 1e-3


def test_asymmetric_quantization_roundtrip():
    tensor = torch.tensor([0.0, 2.0, 4.0, 8.0])
    q_tensor, scale, zero_point = quantize_asymmetric(tensor, num_bits=8)
    assert zero_point >= 0
    recon = dequantize_asymmetric(q_tensor, scale, zero_point)

    mse = torch.mean((tensor - recon) ** 2).item()
    assert mse < 1e-3


def test_quantization_error_metrics():
    original = torch.tensor([1.0, 2.0, 3.0, 4.0])
    dequantized = torch.tensor([1.01, 1.99, 3.02, 3.98])
    metrics = compute_quantization_error(original, dequantized)

    assert "mse" in metrics
    assert "mae" in metrics
    assert "cosine_similarity" in metrics
    assert "sqnr_db" in metrics
    assert metrics["cosine_similarity"] > 0.99
    assert metrics["sqnr_db"] > 30.0


def test_uniform_quantizer_class():
    quantizer = UniformQuantizer(num_bits=8, symmetric=True)
    tensor = torch.randn(10, 10)
    metrics = quantizer.evaluate(tensor)

    assert metrics["cosine_similarity"] > 0.99


def test_quantization_invalid_bits():
    tensor = torch.tensor([1.0, 2.0])
    with pytest.raises(QuantizationError, match="Supported bits are"):
        quantize_symmetric(tensor, num_bits=5)


# ============================================================================
# 3. Loss, Information Theory & Cost Calculator Tests
# ============================================================================


def test_cross_entropy_loss_and_perplexity():
    logits = torch.tensor([[[2.0, 0.0], [0.0, 2.0]]])
    targets = torch.tensor([[0, 1]])

    loss = compute_cross_entropy_loss(logits, targets)
    ppl = compute_perplexity(loss)

    assert loss > 0.0
    assert ppl > 1.0
    assert math.isclose(ppl, math.exp(loss), rel_tol=1e-5)


def test_shannon_entropy():
    # Uniform probability distribution over 4 classes -> 2.0 bits of entropy
    probs = torch.tensor([[0.25, 0.25, 0.25, 0.25]])
    entropy = compute_shannon_entropy(probs, base=2.0)
    assert math.isclose(entropy.item(), 2.0, abs_tol=1e-4)


def test_bits_per_byte():
    loss = 2.0  # nats
    bpb = compute_bits_per_byte(loss, bytes_per_token=4.0)
    expected_bpt = 2.0 / math.log(2.0)
    expected_bpb = expected_bpt / 4.0
    assert math.isclose(bpb, expected_bpb, rel_tol=1e-5)


def test_inference_cost_calculator():
    calc = InferenceCostCalculator(
        num_layers=32, num_heads=32, head_dim=128, hidden_size=4096, num_kv_heads=8
    )

    # 1. Weights memory (7B params in FP16 -> 14 GB)
    param_bytes = calc.compute_model_param_bytes(7_000_000_000, precision_bytes=2.0)
    assert param_bytes == 14_000_000_000

    # 2. KV Cache memory (GQA with 8 KV heads)
    kv_bytes = calc.compute_kv_cache_bytes(batch_size=2, seq_len=1024, precision_bytes=2.0)
    expected_kv = 2 * 32 * 8 * 128 * 1024 * 2 * 2
    assert kv_bytes == expected_kv

    # 3. FLOPs per token
    gen_flops = calc.estimate_flops_per_token(
        num_params=7_000_000_000, seq_len=1024, is_prefill=False
    )
    assert gen_flops > 14_000_000_000

    # 4. Max batch size under 24 GB VRAM
    max_b = calc.compute_max_batch_size(
        vram_capacity_bytes=24 * 1024**3,
        num_params=7_000_000_000,
        seq_len=2048,
        precision_bytes=2.0,
    )
    assert max_b > 0


def test_inference_cost_calculator_invalid_init():
    with pytest.raises(InferenceError, match="strictly positive"):
        InferenceCostCalculator(num_layers=0, num_heads=8, head_dim=64, hidden_size=512)
