import os
import sys

import matplotlib.pyplot as plt
import torch
from loguru import logger

from projects.a_llm_basics.src.lab_03_attention.attention import ScaledDotProductAttention

# Configure loguru logger
logger.remove()
logger.add(
    sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:5}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    level="INFO",
)


def run_experiment() -> None:
    """Runs Scaled Dot-Product Attention experiment comparing bidirectional/causal masks."""
    logger.info("Starting Attention from Scratch Experiment (LAB-03)...")

    # Define a sample input sequence of words
    tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    seq_len = len(tokens)
    d_model = 16

    # For visualization, we'll create a synthetic query, key, value tensors
    # To simulate actual attention weights, we'll initialize them deterministically
    torch.manual_seed(42)
    q = torch.randn(1, seq_len, d_model)
    k = torch.randn(1, seq_len, d_model)
    v = torch.randn(1, seq_len, d_model)

    attention = ScaledDotProductAttention()

    # 1. Compute bidirectional attention (No Mask)
    logger.info("Computing bidirectional self-attention...")
    _, attn_weights_bidir = attention(q, k, v)
    attn_weights_bidir = attn_weights_bidir.squeeze(0).detach().numpy()

    # 2. Compute causal attention (Causal Mask)
    logger.info("Computing causal/autoregressive masked self-attention...")
    causal_mask = torch.tril(torch.ones(seq_len, seq_len)).bool()
    _, attn_weights_causal = attention(q, k, v, mask=causal_mask)
    attn_weights_causal = attn_weights_causal.squeeze(0).detach().numpy()

    # 3. Create visualization plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Bidirectional heat map
    im1 = ax1.imshow(attn_weights_bidir, cmap="viridis", vmin=0, vmax=1)
    ax1.set_title("Bidirectional Self-Attention Weights", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xticks(range(seq_len))
    ax1.set_yticks(range(seq_len))
    ax1.set_xticklabels(tokens, rotation=45, ha="right", fontsize=11)
    ax1.set_yticklabels(tokens, fontsize=11)
    ax1.set_xlabel("Key / Value Tokens", fontsize=12)
    ax1.set_ylabel("Query Tokens", fontsize=12)
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # Causal heat map
    im2 = ax2.imshow(attn_weights_causal, cmap="viridis", vmin=0, vmax=1)
    ax2.set_title("Causal Masked Self-Attention Weights", fontsize=14, fontweight="bold", pad=15)
    ax2.set_xticks(range(seq_len))
    ax2.set_yticks(range(seq_len))
    ax2.set_xticklabels(tokens, rotation=45, ha="right", fontsize=11)
    ax2.set_yticklabels(tokens, fontsize=11)
    ax2.set_xlabel("Key / Value Tokens", fontsize=12)
    ax2.set_ylabel("Query Tokens", fontsize=12)
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    plt.tight_layout()

    # Save Output
    assets_dir = (
        "/mnt/c/Users/rogerio.silva/projetos/production-ai-systems/docs/assets/a_llm_basics"
    )
    os.makedirs(assets_dir, exist_ok=True)
    plot_path = os.path.join(assets_dir, "attention_weights.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    logger.info(f"Attention heatmaps successfully saved to: {plot_path}")
    logger.info("Attention from Scratch Experiment completed successfully!")


if __name__ == "__main__":
    run_experiment()
