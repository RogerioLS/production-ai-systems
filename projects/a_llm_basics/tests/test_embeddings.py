import numpy as np
import pytest

from projects.a_llm_basics.src.embeddings import TFIDFEmbedder, WordCategoryEmbedder
from projects.a_llm_basics.src.reducer import DimensionalityReducer
from projects.a_llm_basics.src.semantic_search import (
    SemanticSearchEngine,
    cosine_similarity,
    cosine_similarity_matrix,
)


def test_cosine_similarity_edge_cases():
    # Identical vectors
    u = np.array([1.0, 0.0, 0.0])
    v = np.array([1.0, 0.0, 0.0])
    assert pytest.approx(cosine_similarity(u, v)) == 1.0

    # Orthogonal vectors
    v2 = np.array([0.0, 1.0, 0.0])
    assert pytest.approx(cosine_similarity(u, v2)) == 0.0

    # Opposite vectors
    v3 = np.array([-1.0, 0.0, 0.0])
    assert pytest.approx(cosine_similarity(u, v3)) == -1.0

    # Zero vector handling
    zero_vec = np.zeros(3)
    assert cosine_similarity(u, zero_vec) == 0.0

    # Dimension mismatch check
    with pytest.raises(ValueError):
        cosine_similarity(np.array([1.0, 2.0]), np.array([1.0, 2.0, 3.0]))


def test_cosine_similarity_matrix():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]])
    matrix = cosine_similarity_matrix(vectors)
    assert matrix.shape == (3, 3)
    assert pytest.approx(matrix[0, 0]) == 1.0
    assert pytest.approx(matrix[0, 1]) == 0.0
    assert pytest.approx(matrix[0, 2]) == -1.0


def test_word_category_embedder():
    embedder = WordCategoryEmbedder(dimension=32)
    assert embedder.dimension == 32

    # Verify normalization (L2 norm should be 1.0)
    vec_apple = embedder.embed_text("apple")
    assert pytest.approx(np.linalg.norm(vec_apple)) == 1.0

    # In-Vocabulary vs OOV
    vec_oov = embedder.embed_text("out-of-vocabulary-word-here")
    assert pytest.approx(np.linalg.norm(vec_oov)) == 1.0

    # Verify category clustering behavior
    # "apple" and "banana" are both 'food'
    # "python" and "java" are both 'tech'
    sim_same = cosine_similarity(embedder.embed_text("apple"), embedder.embed_text("banana"))
    sim_diff = cosine_similarity(embedder.embed_text("apple"), embedder.embed_text("python"))

    # Word embeddings within the same category should be more similar than across categories
    assert sim_same > sim_diff

    # Test batch embedding
    batch = ["apple", "banana", "python"]
    vectors = embedder.embed_batch(batch)
    assert vectors.shape == (3, 32)


def test_tfidf_embedder():
    embedder = TFIDFEmbedder()

    corpus = [
        "the quick brown fox",
        "jumped over the lazy dog",
        "neural networks and artificial intelligence",
    ]

    embedder.fit(corpus)
    assert embedder.dimension > 0

    vec = embedder.embed_text("neural networks")
    assert vec.shape == (embedder.dimension,)
    assert pytest.approx(np.linalg.norm(vec)) == 1.0

    # Test batch embedding auto-fit
    embedder_lazy = TFIDFEmbedder()
    vectors = embedder_lazy.embed_batch(corpus)
    assert vectors.shape[0] == 3
    assert vectors.shape[1] > 0


def test_dimensionality_reducer():
    embedder = WordCategoryEmbedder(dimension=16)
    words = ["apple", "banana", "orange", "python", "java", "computer"]
    embeddings = embedder.embed_batch(words)

    # Test PCA
    reducer_pca = DimensionalityReducer(method="pca", n_components=2)
    reduced_pca = reducer_pca.fit_transform(embeddings)
    assert reduced_pca.shape == (6, 2)

    # Test t-SNE (perplexity adjustment should trigger)
    reducer_tsne = DimensionalityReducer(method="tsne", n_components=2, perplexity=10)
    reduced_tsne = reducer_tsne.fit_transform(embeddings)
    assert reduced_tsne.shape == (6, 2)


def test_semantic_search_engine():
    embedder = WordCategoryEmbedder(dimension=16)
    engine = SemanticSearchEngine(embedder=embedder)

    corpus = ["apple", "python", "soccer"]
    engine.add_documents(corpus)

    # Search for something related to food
    results_food = engine.search("banana", top_k=2)
    assert len(results_food) == 2
    # Top result should be "apple" as it shares 'food' category in WordCategoryEmbedder
    assert results_food[0][0] == "apple"
    assert results_food[0][1] > results_food[1][1]

    # Search for something related to programming
    results_tech = engine.search("java", top_k=1)
    assert results_tech[0][0] == "python"
