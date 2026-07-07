import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger

from projects.a_llm_basics.src.embeddings import WordCategoryEmbedder
from projects.a_llm_basics.src.reducer import DimensionalityReducer
from projects.a_llm_basics.src.semantic_search import cosine_similarity_matrix

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
    """Runs the Embedding Geometry visualization and Semantic Search experiment."""
    logger.info("Starting Embedding Geometry & Manifold Hypothesis Experiment (LAB-04/LAB-05)...")

    # 1. Instantiate the semantic category embedder
    embedder = WordCategoryEmbedder(dimension=100, noise_std=0.08, seed=42)

    # Gather words and group them by category for visualization
    words = []
    labels = []
    colors = []
    color_map = {
        "food": "#ff7f0e",  # Orange
        "tech": "#1f77b4",  # Blue
        "sports": "#2ca02c",  # Green
        "animals": "#d62728",  # Red
    }

    for category, cat_words in embedder.categories.items():
        for word in cat_words:
            words.append(word)
            labels.append(category)
            colors.append(color_map[category])

    # 2. Extract embeddings
    embeddings = embedder.embed_batch(words)
    logger.info(f"Generated {len(words)} embeddings of dimension {embeddings.shape[1]}.")

    # 3. Compute Similarity Matrix
    sim_matrix = cosine_similarity_matrix(embeddings)

    # Calculate average similarity within categories vs across categories
    intra_similarities = []
    inter_similarities = []

    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            sim = sim_matrix[i, j]
            if labels[i] == labels[j]:
                intra_similarities.append(sim)
            else:
                inter_similarities.append(sim)

    avg_intra = np.mean(intra_similarities)
    avg_inter = np.mean(inter_similarities)

    logger.info("=== Embedding Space Statistics ===")
    logger.info(f"Average Similarity within same category (Intra): {avg_intra:.4f}")
    logger.info(f"Average Similarity across different categories (Inter): {avg_inter:.4f}")
    logger.info(f"Discriminative Margin: {avg_intra - avg_inter:.4f}")

    # 4. Dimensionality Reduction (PCA & t-SNE)
    pca_reducer = DimensionalityReducer(method="pca", n_components=2)
    tsne_reducer = DimensionalityReducer(method="tsne", n_components=2, perplexity=5)

    reduced_pca = pca_reducer.fit_transform(embeddings)
    reduced_tsne = tsne_reducer.fit_transform(embeddings)

    # 5. Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # PCA Plot
    for cat, col in color_map.items():
        indices = [i for i, label in enumerate(labels) if label == cat]
        ax1.scatter(
            reduced_pca[indices, 0],
            reduced_pca[indices, 1],
            c=col,
            label=cat.capitalize(),
            edgecolors="k",
            s=120,
            alpha=0.85,
        )
    ax1.set_title("PCA Projection (Global Geometry)", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Principal Component 1", fontsize=11)
    ax1.set_ylabel("Principal Component 2", fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Annotate points in PCA plot
    for i, word in enumerate(words):
        ax1.annotate(
            word,
            (reduced_pca[i, 0], reduced_pca[i, 1]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
            fontweight="semibold",
        )

    # t-SNE Plot
    for cat, col in color_map.items():
        indices = [i for i, label in enumerate(labels) if label == cat]
        ax2.scatter(
            reduced_tsne[indices, 0],
            reduced_tsne[indices, 1],
            c=col,
            label=cat.capitalize(),
            edgecolors="k",
            s=120,
            alpha=0.85,
        )
    ax2.set_title("t-SNE Projection (Local Neighborhoods)", fontsize=14, fontweight="bold")
    ax2.set_xlabel("t-SNE Dimension 1", fontsize=11)
    ax2.set_ylabel("t-SNE Dimension 2", fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.5)

    # Annotate points in t-SNE plot
    for i, word in enumerate(words):
        ax2.annotate(
            word,
            (reduced_tsne[i, 0], reduced_tsne[i, 1]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
            fontweight="semibold",
        )

    # Legend & Layout
    handles, labels_legend = ax1.get_legend_handles_labels()
    fig.legend(
        handles, labels_legend, loc="upper center", bbox_to_anchor=(0.5, 0.96), ncol=4, fontsize=12
    )
    plt.tight_layout(rect=[0, 0, 1, 0.90])

    # Save Output
    assets_dir = (
        "/mnt/c/Users/rogerio.silva/projetos/production-ai-systems/docs/assets/a_llm_basics"
    )
    os.makedirs(assets_dir, exist_ok=True)
    plot_path = os.path.join(assets_dir, "embedding_geometry.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    logger.info(f"Plot successfully saved to: {plot_path}")
    logger.info("Embedding Geometry & Manifold Hypothesis Experiment completed successfully!")


if __name__ == "__main__":
    run_experiment()
