import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import tiktoken
from loguru import logger
from transformers import AutoTokenizer

# Configure loguru logger to stderr
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


class BaseTokenizer(ABC):
    """Abstract base class representing a tokenizer wrapper to ensure SOLID principles."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the identifier name of the tokenizer."""
        pass

    @abstractmethod
    def encode(self, text: str) -> List[int]:
        """Encodes a string of text into a list of token IDs."""
        pass

    @abstractmethod
    def decode(self, ids: List[int]) -> str:
        """Decodes a list of token IDs back into a string of text."""
        pass

    def calculate_compression_ratio(self, text: str) -> float:
        """Calculates the compression efficiency of the tokenizer.

        Formula: bytes / tokens.
        A higher ratio represents a more efficient compression (fewer tokens per byte).

        Args:
            text: The raw input string.

        Returns:
            The compression ratio as a float. Returns 0.0 if text is empty or tokens equal 0.
        """
        if not text:
            return 0.0

        byte_length = len(text.encode("utf-8"))
        tokens = self.encode(text)
        token_count = len(tokens)

        if token_count == 0:
            return 0.0

        ratio = byte_length / token_count
        logger.debug(
            f"[{self.name}] Bytes: {byte_length}, Tokens: {token_count}, Ratio: {ratio:.4f}"
        )
        return ratio


class TiktokenTokenizer(BaseTokenizer):
    """Wrapper for OpenAI's tiktoken library."""

    def __init__(self, model_or_encoding: str) -> None:
        """Initializes the tiktoken tokenizer.

        Args:
            model_or_encoding: Encoding name (e.g. 'cl100k_base') or model name (e.g. 'gpt-4o').
        """
        self._name = model_or_encoding
        try:
            # Check if it's an encoding name
            self._encoder = tiktoken.get_encoding(model_or_encoding)
        except ValueError:
            # Fall back to checking if it's a model name
            try:
                self._encoder = tiktoken.encoding_for_model(model_or_encoding)
            except KeyError:
                logger.warning(
                    f"Model/encoding '{model_or_encoding}' not found. "
                    "Falling back to cl100k_base."
                )
                self._encoder = tiktoken.get_encoding("cl100k_base")

        logger.info(
            f"Loaded TiktokenTokenizer for '{self._name}' using encoding '{self._encoder.name}'."
        )

    @property
    def name(self) -> str:
        return self._name

    def encode(self, text: str) -> List[int]:
        return self._encoder.encode(text)

    def decode(self, ids: List[int]) -> str:
        return self._encoder.decode(ids)


class HuggingFaceTokenizer(BaseTokenizer):
    """Wrapper for Hugging Face Tokenizers library."""

    def __init__(self, pretrained_model_name: str) -> None:
        """Initializes the Hugging Face tokenizer.

        Args:
            pretrained_model_name: Hugging Face model identifier
                (e.g. 'bert-base-uncased' or 'gpt2').
        """
        self._name = pretrained_model_name
        logger.info(f"Loading HuggingFaceTokenizer for '{self._name}'...")
        # Use local_files_only or try loading, with fallback
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
        except Exception as e:
            logger.error(f"Failed to load tokenizer '{pretrained_model_name}': {e}")
            raise e
        logger.info(f"Successfully loaded HuggingFaceTokenizer '{self._name}'.")

    @property
    def name(self) -> str:
        return self._name

    def encode(self, text: str) -> List[int]:
        # return_tensors is omitted to return raw python ints list
        return self._tokenizer.encode(text, add_special_tokens=False)

    def decode(self, ids: List[int]) -> str:
        return self._tokenizer.decode(ids, clean_up_tokenization_spaces=False)


class TokenizationAnalyzer:
    """Class to perform benchmarks and compression analysis across multiple tokenizers."""

    def __init__(self, tokenizers: List[BaseTokenizer]) -> None:
        self.tokenizers = tokenizers

    def analyze_text(self, text: str) -> Dict[str, Dict[str, Any]]:
        """Analyzes a single text string across all registered tokenizers.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary containing metrics (tokens, bytes, ratio) for each tokenizer.
        """
        byte_length = len(text.encode("utf-8"))
        char_length = len(text)
        results: Dict[str, Dict[str, Any]] = {}

        for tokenizer in self.tokenizers:
            try:
                tokens = tokenizer.encode(text)
                ratio = tokenizer.calculate_compression_ratio(text)
                results[tokenizer.name] = {
                    "token_count": len(tokens),
                    "bytes": byte_length,
                    "chars": char_length,
                    "compression_ratio": ratio,
                    "bytes_per_token": 1.0 / ratio if ratio > 0 else 0.0,
                }
            except Exception as e:
                logger.error(f"Error analyzing text with tokenizer '{tokenizer.name}': {e}")

        return results

    def analyze_corpus(self, corpus: Dict[str, str]) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Analyzes multiple texts representing different domains.

        Args:
            corpus: A dictionary mapping domain/category names to text content.

        Returns:
            Nested dictionary of analysis results: {domain: {tokenizer_name: metrics}}
        """
        analysis: Dict[str, Dict[str, Dict[str, Any]]] = {}
        for category, text in corpus.items():
            logger.info(f"Analyzing category '{category}'...")
            analysis[category] = self.analyze_text(text)
        return analysis
