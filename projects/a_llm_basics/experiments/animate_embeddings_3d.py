import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from loguru import logger

from projects.a_llm_basics.src.embeddings import WordCategoryEmbedder
from projects.a_llm_basics.src.reducer import DimensionalityReducer

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


def generate_3d_rotation() -> None:
    """Generates an animated GIF of a 3D PCA embedding space rotating 360 degrees."""
    logger.info("Initializing 3D PCA space rotation animation generation...")

    # 1. Generate Embeddings
    embedder = WordCategoryEmbedder(dimension=100, noise_std=0.06, seed=42)
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

    embeddings = embedder.embed_batch(words)

    # 2. Project to 3D via PCA
    pca_reducer = DimensionalityReducer(method="pca", n_components=3)
    coords_3d = pca_reducer.fit_transform(embeddings)

    # Setup figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    fig.patch.set_facecolor("#ffffff")
    ax = fig.add_subplot(projection="3d")
    ax.set_facecolor("#fcfcfc")

    # Set initial plotting limits
    margin = 0.2
    ax.set_xlim(coords_3d[:, 0].min() - margin, coords_3d[:, 0].max() + margin)
    ax.set_ylim(coords_3d[:, 1].min() - margin, coords_3d[:, 1].max() + margin)
    ax.set_zlim(coords_3d[:, 2].min() - margin, coords_3d[:, 2].max() + margin)

    # Styling axes
    ax.set_xlabel("Principal Component 1", fontsize=10, labelpad=10)
    ax.set_ylabel("Principal Component 2", fontsize=10, labelpad=10)
    ax.set_zlabel("Principal Component 3", fontsize=10, labelpad=10)
    ax.grid(True, linestyle="--", alpha=0.3)

    # Legend proxy handles
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

    # Draw initial scatter points in 3D
    scatter = ax.scatter(
        coords_3d[:, 0],
        coords_3d[:, 1],
        coords_3d[:, 2],
        c=colors,
        edgecolors="k",
        s=120,
        alpha=0.85,
        depthshade=True,
    )

    # Add text labels in 3D
    text_objects = []
    for idx, word in enumerate(words):
        txt = ax.text(
            coords_3d[idx, 0],
            coords_3d[idx, 1],
            coords_3d[idx, 2],
            word,
            fontsize=8,
            fontweight="semibold",
            ha="center",
            va="bottom",
        )
        text_objects.append(txt)

    total_frames = 120

    def init():
        ax.view_init(elev=20, azim=0)
        return [scatter] + text_objects

    def update(frame):
        # Rotate azimuth angle 360 degrees over total frames
        angle = (frame / total_frames) * 360.0
        ax.view_init(elev=20, azim=angle)

        ax.set_title(
            f"3D PCA Manifold Rotation (Angle: {int(angle)}°)",
            fontsize=14,
            fontweight="bold",
            pad=10,
        )
        return [scatter] + text_objects

    logger.info("Assembling 3D rotation frames...")
    ani = animation.FuncAnimation(
        fig, update, frames=total_frames, init_func=init, blit=False, interval=40
    )

    # Save output
    assets_dir = (
        "/mnt/c/Users/rogerio.silva/projetos/production-ai-systems/docs/assets/a_llm_basics"
    )
    os.makedirs(assets_dir, exist_ok=True)
    gif_path = os.path.join(assets_dir, "embedding_rotation_3d.gif")

    logger.info("Saving 3D rotation animated GIF file via Pillow (this may take a few seconds)...")
    ani.save(gif_path, writer="pillow", fps=25)
    plt.close()

    logger.info(f"3D Manifold Rotation animation saved successfully to: {gif_path}")


if __name__ == "__main__":
    generate_3d_rotation()
