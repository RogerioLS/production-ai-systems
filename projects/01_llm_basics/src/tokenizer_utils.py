import tiktoken
from transformers import AutoTokenizer


def count_tokens_openai(text: str, model: str = "gpt-4o") -> int:
    """Counts tokens using tiktoken for OpenAI models."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def count_tokens_anthropic(text: str) -> int:
    """Estimates tokens for Claude (using HuggingFace tokenizer as proxy)."""
    # Note: Anthropic uses a slightly different BPE, but this is a common proxy for estimation
    tokenizer = AutoTokenizer.from_pretrained("claude-tokenizer-proxy")  # Placeholder
    return len(tokenizer.encode(text))


if __name__ == "__main__":
    sample_text = "IA para produção exige robustez e pipelines claros."
    print(f"Text: {sample_text}")
    print(f"OpenAI (gpt-4o) tokens: {count_tokens_openai(sample_text)}")
