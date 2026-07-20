import sys
from typing import List, Tuple

import numpy as np
from loguru import logger

from projects.a_llm_basics.src.lab_02_embeddings.embeddings import BaseEmbedder

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


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """Computes the cosine similarity between two 1D vectors.

    Mathematical formula:
    cos(theta) = (u . v) / (||u||_2 * ||v||_2)

    A value of 1.0 means identical direction, 0.0 means orthogonal, and -1.0 means opposite.

    Args:
        u: First 1D NumPy array.
        v: Second 1D NumPy array.

    Returns:
        The similarity value as a float in [-1.0, 1.0].
        Returns 0.0 if either vector has a magnitude of 0.
    """
    if u.ndim != 1 or v.ndim != 1:
        raise ValueError("Inputs to cosine_similarity must be 1D vectors.")

    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)

    if norm_u == 0.0 or norm_v == 0.0:
        logger.warning("Zero-vector detected in cosine similarity computation. Returning 0.0.")
        return 0.0

    dot_product = np.dot(u, v)
    similarity = float(dot_product / (norm_u * norm_v))

    # Guard against float precision issues pushing value outside [-1, 1]
    return max(-1.0, min(1.0, similarity))


def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    """Computes the pairwise cosine similarity matrix for a set of vectors.

    Args:
        vectors: A 2D NumPy array of shape (n_samples, n_features).

    Returns:
        A 2D symmetric NumPy array of shape (n_samples, n_samples) where
        entry (i, j) is the cosine similarity between vector i and vector j.
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    # Avoid division by zero
    norms[norms == 0.0] = 1.0
    normalized_vectors = vectors / norms
    return np.dot(normalized_vectors, normalized_vectors.T)


class SemanticSearchEngine:
    """A semantic search engine using vectors and Cosine Similarity to find documents.

    Adheres to dependency inversion by requiring a BaseEmbedder abstraction.
    """

    def __init__(self, embedder: BaseEmbedder) -> None:
        """Initializes the search engine.

        Args:
            embedder: A concrete implementation of BaseEmbedder.
        """
        self.embedder = embedder
        self.documents: List[str] = []
        self.doc_embeddings: np.ndarray = np.empty((0, embedder.dimension))
        logger.info(
            f"Initialized SemanticSearchEngine with embedder dimension: {embedder.dimension}"
        )

    def add_documents(self, documents: List[str]) -> None:
        """Embeds and indexes documents for search.

        Args:
            documents: List of text strings to index.
        """
        if not documents:
            return

        new_embeddings = self.embedder.embed_batch(documents)
        self.documents.extend(documents)

        if self.doc_embeddings.size == 0:
            self.doc_embeddings = new_embeddings
        else:
            self.doc_embeddings = np.vstack([self.doc_embeddings, new_embeddings])

        logger.info(
            f"Indexed {len(documents)} new documents. Total corpus size: {len(self.documents)}"
        )

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Searches the indexed corpus using the query string.

        Computes cosine similarity between the query vector and all document vectors,
        sorting descending.

        Args:
            query: The search query string.
            top_k: The number of top results to return.

        Returns:
            A list of tuples (document_text, similarity_score) sorted descending by similarity.
        """
        if not self.documents:
            logger.warning("Search query executed on an empty index.")
            return []

        query_vector = self.embedder.embed_text(query)

        # Compute cosine similarity for all indexed documents
        # Since self.doc_embeddings are L2 normalized and query_vector is L2 normalized,
        # we can compute this using a single matrix-vector dot product.
        norms = np.linalg.norm(self.doc_embeddings, axis=1)
        query_norm = np.linalg.norm(query_vector)

        if query_norm == 0.0:
            logger.warning("Query vector has zero magnitude.")
            return [(doc, 0.0) for doc in self.documents[:top_k]]

        # Fallback to standard math in case indexing norms are non-unit
        scores = np.dot(self.doc_embeddings, query_vector) / (norms * query_norm + 1e-15)

        # Retrieve top k indexes
        top_k = min(top_k, len(self.documents))
        # argpartition is O(n), then sort the slice O(k log k)
        partition_indices = np.argpartition(scores, -top_k)[-top_k:]
        sorted_partition_indices = partition_indices[np.argsort(-scores[partition_indices])]

        results = [(self.documents[idx], float(scores[idx])) for idx in sorted_partition_indices]
        logger.info(
            f"Completed semantic search for query '{query}'. Returned {len(results)} results."
        )
        return results
