import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from sklearn.manifold import TSNE

from projects.a_llm_basics.src.lab_02_embeddings.embeddings import WordCategoryEmbedder

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


def generate_animation() -> None:
    """Generates an animated GIF of the t-SNE optimization/morphing process."""
    logger.info("Initializing animation generation for embedding clusters...")

    # 1. Generate Embeddings
    embedder = WordCategoryEmbedder(dimension=100, noise_std=0.06, seed=42)
    words = []
    categories = []
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
            categories.append(category)
            colors.append(color_map[category])

    embeddings = embedder.embed_batch(words)

    # 2. Compute Target coordinates (t-SNE final positions)
    tsne = TSNE(n_components=2, perplexity=5, random_state=42, init="random")
    final_coords = tsne.fit_transform(embeddings)

    # L2 normalize coordinates to align them nicely in the viewport [-1.5, 1.5]
    final_coords = (final_coords - np.mean(final_coords, axis=0)) / np.std(final_coords, axis=0)

    # 3. Create initial random coordinates (simulating t-SNE start state)
    rng = np.random.default_rng(42)
    start_coords = rng.normal(0, 0.4, size=final_coords.shape)

    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fcfcfc")

    # Animation configuration
    total_frames = 90

    # Generate smooth interpolation factor using a sigmoid curve
    # This creates a "slow start -> fast movement -> slow deceleration" effect (ease-in-out)
    t = np.linspace(-4, 4, total_frames)
    interpolation_factors = 1.0 / (1.0 + np.exp(-t))
    # Normalize factors to strictly span [0, 1]
    interpolation_factors = (interpolation_factors - interpolation_factors[0]) / (
        interpolation_factors[-1] - interpolation_factors[0]
    )

    scat = ax.scatter([], [], s=200, edgecolors="k", alpha=0.8)

    # Keep track of text annotations
    texts = [ax.text(0, 0, "", fontsize=9, fontweight="semibold", ha="center") for _ in words]

    def init():
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_title(
            "t-SNE Clustering Morpheme: High-Dimensional Manifold Projection",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )
        ax.set_xlabel("Dimension 1", fontsize=11)
        ax.set_ylabel("Dimension 2", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.3)

        # Add legend custom proxies
        proxies = [
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=col,
                markersize=12,
                markeredgecolor="k",
                label=cat.capitalize(),
            )
            for cat, col in color_map.items()
        ]
        ax.legend(handles=proxies, loc="upper right", fontsize=10)

        return [scat] + texts

    def update(frame):
        factor = interpolation_factors[frame]
        # Interpolate coordinates
        current_coords = (1 - factor) * start_coords + factor * final_coords

        # Update scatter point positions and colors
        scat.set_offsets(current_coords)
        scat.set_color(colors)
        scat.set_edgecolor("black")

        # Update text annotations
        for idx, (x, y) in enumerate(current_coords):
            texts[idx].set_position((x, y + 0.08))
            texts[idx].set_text(words[idx])
            # Fade in texts as the simulation converges to make it cleaner
            texts[idx].set_alpha(max(0.1, factor))

        # Draw soft hulls around cluster centers during convergence to show neighborhood partition
        if frame > 40:
            for cat, col in color_map.items():
                cat_indices = [i for i, c in enumerate(categories) if c == cat]
                cat_coords = current_coords[cat_indices]
                center = np.mean(cat_coords, axis=0)
                # Compute average radius to draw a soft boundary circle
                radius = np.max(np.linalg.norm(cat_coords - center, axis=1)) * 1.15

                # Draw a temporary circle that gets cleared next frame
                circle = plt.Circle(
                    center, radius, color=col, alpha=0.015 * (factor - 0.4), zorder=0
                )
                ax.add_patch(circle)

        # Update subtitle indicating frame progress
        ax.set_title(
            f"t-SNE Projection Morphing... Convergence Progress: {int(factor * 100)}%",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )

        # Clean up old patches (circles) to prevent overlay memory build-up
        # Keep only the background/scatter/legend objects
        while len(ax.patches) > len(words) // len(color_map) and frame < total_frames - 1:
            ax.patches[0].remove()

        return [scat] + texts

    logger.info("Assembling and rendering animation frames...")
    ani = animation.FuncAnimation(
        fig, update, frames=total_frames, init_func=init, blit=False, interval=50
    )

    # 4. Save output
    assets_dir = (
        "/mnt/c/Users/rogerio.silva/projetos/production-ai-systems/docs/assets/a_llm_basics"
    )
    os.makedirs(assets_dir, exist_ok=True)
    gif_path = os.path.join(assets_dir, "embedding_manifold.gif")

    logger.info("Saving animated GIF file via Pillow writer (this may take a few seconds)...")
    ani.save(gif_path, writer="pillow", fps=20)
    plt.close()

    logger.info(f"Animated manifold visualization saved successfully to: {gif_path}")


if __name__ == "__main__":
    generate_animation()
