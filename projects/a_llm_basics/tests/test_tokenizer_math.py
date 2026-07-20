from unittest.mock import MagicMock

from projects.a_llm_basics.src.lab_01_tokenization.tokenizer_math import (
    BaseTokenizer,
    HuggingFaceTokenizer,
    TiktokenTokenizer,
    TokenizationAnalyzer,
)


class DummyTokenizer(BaseTokenizer):
    """A dummy implementation of BaseTokenizer for testing base class features."""

    @property
    def name(self) -> str:
        return "dummy"

    def encode(self, text: str) -> list[int]:
        # Return length of characters as simple mock encoding token IDs
        return [ord(char) for char in text]

    def decode(self, ids: list[int]) -> str:
        return "".join(chr(i) for i in ids)


def test_base_tokenizer_compression_ratio():
    tokenizer = DummyTokenizer()
    text = "Hello!"  # 6 bytes in UTF-8
    # encode returns 6 integers (one for each character)
    # Ratio = 6 bytes / 6 tokens = 1.0
    assert tokenizer.calculate_compression_ratio(text) == 1.0

    # Empty text case
    assert tokenizer.calculate_compression_ratio("") == 0.0


def test_tiktoken_tokenizer_lifecycle():
    # Test loading a valid standard encoding
    tokenizer = TiktokenTokenizer("cl100k_base")
    assert tokenizer.name == "cl100k_base"

    text = "AI is eating the world"
    tokens = tokenizer.encode(text)
    assert isinstance(tokens, list)
    assert len(tokens) > 0
    assert all(isinstance(t, int) for t in tokens)

    decoded = tokenizer.decode(tokens)
    assert decoded == text


def test_tiktoken_tokenizer_fallback():
    # Test loading an invalid encoding name to trigger fallback
    tokenizer = TiktokenTokenizer("invalid_encoding_name_xyz")
    # Should fall back to cl100k_base
    assert tokenizer._encoder.name == "cl100k_base"


def test_huggingface_tokenizer_mock():
    # Mock AutoTokenizer.from_pretrained to avoid network dependency in tests
    mock_hf_tokenizer = MagicMock()
    mock_hf_tokenizer.encode.return_value = [101, 2054, 2003, 102]
    mock_hf_tokenizer.decode.return_value = "hello world"

    # We patch or inject a mock tokenizer into HuggingFaceTokenizer for testing
    tokenizer = HuggingFaceTokenizer.__new__(HuggingFaceTokenizer)
    tokenizer._name = "mock-hf"
    tokenizer._tokenizer = mock_hf_tokenizer

    assert tokenizer.name == "mock-hf"
    assert tokenizer.encode("hello world") == [101, 2054, 2003, 102]
    assert tokenizer.decode([101, 2054, 2003, 102]) == "hello world"
    mock_hf_tokenizer.encode.assert_called_once_with("hello world", add_special_tokens=False)
    mock_hf_tokenizer.decode.assert_called_once_with(
        [101, 2054, 2003, 102], clean_up_tokenization_spaces=False
    )


def test_tokenization_analyzer():
    tk1 = DummyTokenizer()
    analyzer = TokenizationAnalyzer([tk1])

    corpus = {
        "english": "Hello world",
        "empty": "",
    }

    analysis = analyzer.analyze_corpus(corpus)

    assert "english" in analysis
    assert "empty" in analysis
    assert "dummy" in analysis["english"]

    metrics = analysis["english"]["dummy"]
    assert metrics["token_count"] == len("Hello world")
    assert metrics["bytes"] == len("Hello world".encode("utf-8"))
    assert metrics["compression_ratio"] == 1.0
