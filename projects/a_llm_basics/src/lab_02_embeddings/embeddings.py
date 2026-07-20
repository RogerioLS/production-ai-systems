import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import numpy as np
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer

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


class BaseEmbedder(ABC):
    """Abstract base class representing an embedding model to adhere to the OCP principle."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Returns the dimensionality of the generated embedding vectors."""
        pass

    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray:
        """Generates a dense embedding vector for a single text input.

        Args:
            text: The input string to embed.

        Returns:
            A NumPy 1D array of floats representing the embedding.
        """
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generates dense embedding vectors for a batch of text inputs.

        Args:
            texts: A list of input strings to embed.

        Returns:
            A NumPy 2D array of shape (len(texts), dimension) representing the embeddings.
        """
        pass


class WordCategoryEmbedder(BaseEmbedder):
    """A synthetic, deterministic embedder that generates cluster-based high-dimensional embeddings.

    This embedder is designed to demonstrate the Manifold Hypothesis and Embedding Geometry
    without requiring external model downloads (like PyTorch or TensorFlow) or API calls.
    It maps words in predefined categories to clusters in a latent space, adding minor
    Gaussian noise to simulate realistic word embeddings.
    """

    def __init__(self, dimension: int = 100, noise_std: float = 0.05, seed: int = 42) -> None:
        """Initializes the WordCategoryEmbedder with a specific dimensionality and noise level.

        Args:
            dimension: The size of the embedding vectors (must be >= 8).
            noise_std: Standard deviation of the Gaussian noise added to simulate variance.
            seed: Random seed for deterministic replication of vectors.
        """
        if dimension < 8:
            raise ValueError("Embedding dimension must be at least 8 to prevent overlap.")

        self._dimension = dimension
        self.noise_std = noise_std
        self.seed = seed

        # Define categories and semantic words
        self.categories = {
            "food": ["apple", "banana", "orange", "grape", "tomato", "pizza", "sushi", "bread"],
            "tech": [
                "python",
                "java",
                "computer",
                "software",
                "database",
                "ai",
                "hardware",
                "internet",
            ],
            "sports": [
                "football",
                "soccer",
                "tennis",
                "basketball",
                "athlete",
                "stadium",
                "referee",
                "run",
            ],
            "animals": ["lion", "tiger", "elephant", "giraffe", "monkey", "dog", "cat", "panda"],
        }

        # Initialize RNG and generate cluster centers
        rng = np.random.default_rng(self.seed)
        self.category_centers: Dict[str, np.ndarray] = {}

        # Place category centers on orthogonal axes to maximize initial separability
        category_keys = list(self.categories.keys())
        for idx, cat in enumerate(category_keys):
            center = np.zeros(self._dimension)
            # Assign specific orthogonal dimensions to represent core category dimensions
            center[idx * 2 : (idx + 1) * 2] = 1.0
            # Add a small amount of random distribution across other dimensions
            center += rng.normal(0, 0.1, size=self._dimension)
            # L2 Normalize the center vector
            self.category_centers[cat] = center / np.linalg.norm(center)

        logger.info(
            f"Initialized WordCategoryEmbedder (dimension={self._dimension}, "
            f"noise_std={self.noise_std}) with {len(category_keys)} semantic categories."
        )

    @property
    def dimension(self) -> int:
        return self._dimension

    def _get_word_category(self, word: str) -> Optional[str]:
        """Finds the category of a word, or returns None if out-of-vocabulary."""
        word_clean = word.strip().lower()
        for cat, words in self.categories.items():
            if word_clean in words:
                return cat
        return None

    def embed_text(self, text: str) -> np.ndarray:
        """Generates a dense embedding for a word by retrieving its category
        center and adding noise.

        For Out-Of-Vocabulary (OOV) words, a default randomized vector is generated
        deterministically based on the word's hash.

        Args:
            text: The word or phrase to embed.

        Returns:
            A 1D NumPy array representing the embedding vector.
        """
        category = self._get_word_category(text)
        rng_seed = hash(text) & 0xFFFFFFFF  # Ensure deterministic mapping per word
        rng = np.random.default_rng(rng_seed)

        if category is not None:
            # Word belongs to a known category
            center = self.category_centers[category]
            # Add small semantic offset based on word itself to give each word uniqueness
            offset = rng.normal(0, self.noise_std, size=self._dimension)
            vector = center + offset
        else:
            # OOV: generate a completely random unit vector
            logger.debug(f"OOV word '{text}' embedded as random vector.")
            vector = rng.normal(0, 1.0, size=self._dimension)

        # L2 Normalize to lie on the unit hypersphere (typical for modern embeddings)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        else:
            vector = np.zeros(self._dimension)

        return vector

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generates dense embedding vectors for a batch of texts.

        Args:
            texts: A list of input strings.

        Returns:
            A NumPy 2D array of shape (len(texts), dimension).
        """
        embeddings = [self.embed_text(t) for t in texts]
        return np.vstack(embeddings)


class TFIDFEmbedder(BaseEmbedder):
    """An embedder that uses TF-IDF vectors from scikit-learn.

    While not semantic in the modern neural sense, TF-IDF represents document geometry
    determined by vocabulary distributions.
    """

    def __init__(self) -> None:
        """Initializes the TF-IDF Vectorizer."""
        self._vectorizer = TfidfVectorizer()
        self._fitted = False
        self._dimension = 0

    @property
    def dimension(self) -> int:
        if not self._fitted:
            raise ValueError("TF-IDF Vectorizer is not fitted yet. Call fit or embed_batch first.")
        return self._dimension

    def fit(self, texts: List[str]) -> None:
        """Fits the TF-IDF vocabulary on a reference corpus.

        Args:
            texts: Corpus of reference documents.
        """
        self._vectorizer.fit(texts)
        self._fitted = True
        self._dimension = len(self._vectorizer.get_feature_names_out())
        logger.info(f"Fitted TFIDFEmbedder. Latent vocabulary size: {self._dimension}")

    def embed_text(self, text: str) -> np.ndarray:
        """Embeds a single string. Note: Vectorizer must be fitted first.

        Args:
            text: The text to encode.

        Returns:
            A 1D numpy array representing the TF-IDF vector.
        """
        if not self._fitted:
            # Fit on single text as fallback, though suboptimal
            self.fit([text])

        vector = self._vectorizer.transform([text]).toarray()[0]
        # Normalize to ensure L2 norm of 1
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embeds a list of strings, fitting the vocabulary if it hasn't been fitted.

        Args:
            texts: The list of texts to embed.

        Returns:
            A 2D numpy array of shape (len(texts), vocab_size).
        """
        if not self._fitted:
            self.fit(texts)

        vectors = self._vectorizer.transform(texts).toarray()
        # Row-wise L2 normalization
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0] = 1.0
        return vectors / norms
