"""Standalone experiment execution script for LAB-04 Inference Math."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from loguru import logger  # noqa: E402

try:
    import torch

    from projects.a_llm_basics.src.lab_04_inference import (  # noqa: E402
        InferenceCostCalculator,
        SamplingEngine,
        UniformQuantizer,
        compute_quantization_error,
    )
except ImportError as err:
    logger.error("PyTorch or LAB-04 inference dependencies not installed: {}", err)
    sys.exit(1)


def run_sampling_experiment() -> None:
    """Evaluates sampling entropy shifts across temperatures."""
    logger.info("=== Running Experiment 1: Sampling Temperature & Logits Transformation ===")
    logits = torch.tensor([[10.0, 5.0, 2.0, 0.5, 0.1]])
    temperatures = [0.1, 0.7, 1.0, 1.5, 2.0]

    header = (
        f"{'Temperature (T)':<18} | {'Top-K':<8} | {'Top-P':<8} | "
        f"{'Sampled Index':<15} | {'Behavior'}"
    )
    print(header)
    print("-" * len(header))

    for temp in temperatures:
        engine = SamplingEngine(temperature=temp, top_k=3, top_p=0.9)
        sampled = engine.sample(logits, do_sample=True)
        behavior = (
            "Greedy / Low Variance"
            if temp < 0.5
            else ("Balanced" if temp <= 1.0 else "High Entropy")
        )
        print(f"{temp:<18.1f} | {3:<8} | {0.9:<8.2f} | {sampled.item():<15} | {behavior}")


def run_quantization_experiment() -> None:
    """Evaluates quantization precision loss across FP32, INT8, and INT4 schemes."""
    logger.info("=== Running Experiment 2: FP32 to INT8/INT4 Uniform Quantization ===")
    torch.manual_seed(42)
    weights = torch.randn(100, 100)  # Simulated weight matrix

    schemes = [
        ("INT8 (Symmetric)", UniformQuantizer(num_bits=8, symmetric=True)),
        ("INT8 (Asymmetric)", UniformQuantizer(num_bits=8, symmetric=False)),
        ("INT4 (Symmetric)", UniformQuantizer(num_bits=4, symmetric=True)),
        ("INT4 (Asymmetric)", UniformQuantizer(num_bits=4, symmetric=False)),
    ]

    header = (
        f"{'Quantization Scheme':<22} | {'Bitwidth':<8} | {'MSE':<12} | "
        f"{'Cos Similarity':<15} | {'SQNR (dB)'}"
    )
    print(header)
    print("-" * len(header))

    for name, quantizer in schemes:
        q_tensor, scale, zero_point = quantizer.quantize(weights)
        deq_tensor = quantizer.dequantize(q_tensor, scale, zero_point)
        metrics = compute_quantization_error(weights, deq_tensor)

        print(
            f"{name:<22} | {quantizer.num_bits:<8} | {metrics['mse']:<12.6f} | "
            f"{metrics['cosine_similarity']:<15.6f} | {metrics['sqnr_db']:.2f} dB"
        )


def run_inference_economics_experiment() -> None:
    """Calculates LLM inference VRAM footprint and max supportable batch sizes."""
    logger.info("=== Running Experiment 3: LLM Inference Economics & KV Cache Footprint ===")
    calc = InferenceCostCalculator(
        num_layers=32, num_heads=32, head_dim=128, hidden_size=4096, num_kv_heads=8
    )

    context_lengths = [1024, 4096, 8192, 16384]
    num_params = 7_000_000_000  # 7B model

    header = (
        f"{'Context Length (S)':<18} | {'Weights VRAM':<15} | "
        f"{'KV Cache VRAM':<15} | {'Max B (24GB VRAM)'}"
    )
    print(header)
    print("-" * len(header))

    for seq_len in context_lengths:
        weights_mb = calc.compute_model_param_bytes(num_params, precision_bytes=2.0) / (1024**2)
        kv_mb = calc.compute_kv_cache_bytes(batch_size=1, seq_len=seq_len, precision_bytes=2.0) / (
            1024**2
        )
        max_b = calc.compute_max_batch_size(
            vram_capacity_bytes=24 * 1024**3,
            num_params=num_params,
            seq_len=seq_len,
            precision_bytes=2.0,
        )

        print(f"{seq_len:<18} | {weights_mb / 1024:<12.2f} GB | {kv_mb:<12.2f} MB | {max_b:<15}")


def main() -> None:
    logger.info("Starting LAB-04 Inference Math Empirical Experiments...")
    run_sampling_experiment()
    print()
    run_quantization_experiment()
    print()
    run_inference_economics_experiment()
    logger.success("LAB-04 Experiments completed successfully.")


if __name__ == "__main__":
    main()
