import sys
from typing import Literal

import numpy as np
from loguru import logger
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

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


class DimensionalityReducer:
    """A helper class to wrap PCA and t-SNE operations for embedding space visualization.

    Demonstrates how high-dimensional vectors (Manifold Hypothesis) can be projected into
    interpretable 2D/3D spaces.
    """

    def __init__(
        self,
        method: Literal["pca", "tsne"] = "pca",
        n_components: int = 2,
        random_state: int = 42,
        **kwargs,
    ) -> None:
        """Initializes the DimensionalityReducer.

        Args:
            method: The reduction algorithm to use ('pca' or 'tsne').
            n_components: Target dimensions (usually 2 for plotting).
            random_state: Random seed for reproducibility of t-SNE initialization.
            **kwargs: Additional parameters forwarded to the scikit-learn models.
        """
        self.method = method.lower()
        self.n_components = n_components
        self.random_state = random_state
        self.extra_params = kwargs

        if self.method == "pca":
            self._model = PCA(
                n_components=self.n_components, random_state=self.random_state, **self.extra_params
            )
        elif self.method == "tsne":
            # t-SNE perplexity must be less than the number of samples, handled during reduction.
            self._model = TSNE(
                n_components=self.n_components,
                random_state=self.random_state,
                init="random",  # Explicitly set to avoid deprecation warnings
                **self.extra_params,
            )
        else:
            raise ValueError(f"Unknown reduction method: '{self.method}'. Use 'pca' or 'tsne'.")

        logger.info(
            f"Initialized DimensionalityReducer with method='{self.method}', "
            f"target_dim={self.n_components}."
        )

    def fit_transform(self, embeddings: np.ndarray) -> np.ndarray:
        """Fits the reducer model and projects the embeddings to the target dimension.

        Args:
            embeddings: A 2D numpy array of shape (n_samples, n_features).

        Returns:
            A 2D numpy array of shape (n_samples, n_components).
        """
        n_samples, n_features = embeddings.shape

        if n_samples < self.n_components:
            raise ValueError(
                f"Number of samples ({n_samples}) must be greater than or equal to "
                f"target components ({self.n_components}) to perform reduction."
            )

        # Dynamic adjustment of perplexity for t-SNE to avoid crashes on small datasets
        if self.method == "tsne":
            # Perplexity must be less than n_samples. Typically perplexity = min(30, n_samples - 1)
            default_perplexity = self.extra_params.get("perplexity", 30.0)
            if default_perplexity >= n_samples:
                adjusted_perplexity = float(max(1, n_samples - 1))
                logger.warning(
                    f"t-SNE perplexity ({default_perplexity}) is >= "
                    f"samples ({n_samples}). Adjusting to {adjusted_perplexity}."
                )
                # Re-initialize model with adjusted perplexity
                self._model = TSNE(
                    n_components=self.n_components,
                    random_state=self.random_state,
                    perplexity=adjusted_perplexity,
                    init="random",
                )

        reduced_vectors = self._model.fit_transform(embeddings)
        logger.info(
            f"Successfully projected embeddings from shape {embeddings.shape} "
            f"to {reduced_vectors.shape} using {self.method.upper()}."
        )
        return reduced_vectors
