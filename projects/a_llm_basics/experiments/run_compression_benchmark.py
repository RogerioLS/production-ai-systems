import os
from typing import Dict

from projects.a_llm_basics.src.lab_01_tokenization.tokenizer_math import (
    HuggingFaceTokenizer,
    TiktokenTokenizer,
    TokenizationAnalyzer,
)


def run_benchmark():
    # Define corpus representing various production domains
    corpus: Dict[str, str] = {
        "Plain English": (
            "In mathematical logic and computer science, a type system is a "
            "logical system comprising a set of rules that assigns a "
            "property called a type to every term."
        ),
        "Portuguese (PT-BR)": (
            "No desenvolvimento de sistemas de inteligência artificial "
            "aplicados ao mercado financeiro, a precisão da tokenização "
            "impacta diretamente os custos operacionais e a latência "
            "de inferência."
        ),
        "Structured JSON": (
            '{"transaction_id": "tx_982341", "amount": 15400.50, '
            '"currency": "BRL", "status": "approved", '
            '"timestamp": "2026-06-25T19:00:00Z", "metadata": '
            '{"origin": "api-gateway", "retry_count": 0}}'
        ),
        "Numeric / Tabular": (
            "10,234.50 | 89,120.00 | -15.4% | " "1.00234 | 0.000034 | 42 | 999.999"
        ),
        "Emojis / Special Chars": ("🚀🔥📈💡🤖 💻💎💼 | 🛑⚠️⚠️ | ⚡🔗🌐 | 📈💰💹"),
    }

    # Initialize tokenizers (mix of BPE and WordPiece)
    tokenizers = [
        TiktokenTokenizer("o200k_base"),  # GPT-4o Tokenizer (BPE)
        TiktokenTokenizer("cl100k_base"),  # GPT-4 Tokenizer (BPE)
        HuggingFaceTokenizer("gpt2"),  # GPT-2 Tokenizer (BPE - baseline)
        HuggingFaceTokenizer("bert-base-uncased"),  # BERT Tokenizer (WordPiece)
    ]

    analyzer = TokenizationAnalyzer(tokenizers)
    results = analyzer.analyze_corpus(corpus)

    # Generate Markdown Table Report
    report = []
    report.append("# 📊 Tokenization Compression Benchmark Report")
    report.append(
        "\nThis report benchmarks BPE vs WordPiece tokenization "
        "efficiency across different domains."
    )
    report.append("\n## Compression Ratio (Bytes / Token)")
    report.append(
        "> Higher is better. A higher ratio means more text bytes compressed into fewer tokens."
    )
    report.append(
        "\n| Category | GPT-4o (o200k_base) | GPT-4 (cl100k_base) | "
        "GPT-2 (gpt2) | BERT (bert-uncased) |"
    )
    report.append("| --- | --- | --- | --- | --- |")

    for category, tokenizer_results in results.items():
        o200k_ratio = tokenizer_results.get("o200k_base", {}).get("compression_ratio", 0.0)
        cl100k_ratio = tokenizer_results.get("cl100k_base", {}).get("compression_ratio", 0.0)
        gpt2_ratio = tokenizer_results.get("gpt2", {}).get("compression_ratio", 0.0)
        bert_ratio = tokenizer_results.get("bert-base-uncased", {}).get("compression_ratio", 0.0)

        report.append(
            f"| **{category}** | {o200k_ratio:.3f} B/T | "
            f"{cl100k_ratio:.3f} B/T | {gpt2_ratio:.3f} B/T | "
            f"{bert_ratio:.3f} B/T |"
        )

    # Token Count Comparison Table
    report.append("\n## Token Count Comparison")
    report.append(
        "\n| Category | UTF-8 Bytes | GPT-4o (o200k_base) | "
        "GPT-4 (cl100k_base) | GPT-2 (gpt2) | BERT (bert-uncased) |"
    )
    report.append("| --- | --- | --- | --- | --- | --- |")

    for category, tokenizer_results in results.items():
        raw_bytes = next(iter(tokenizer_results.values()))["bytes"]
        o200k_tokens = tokenizer_results.get("o200k_base", {}).get("token_count", 0)
        cl100k_tokens = tokenizer_results.get("cl100k_base", {}).get("token_count", 0)
        gpt2_tokens = tokenizer_results.get("gpt2", {}).get("token_count", 0)
        bert_tokens = tokenizer_results.get("bert-base-uncased", {}).get("token_count", 0)

        report.append(
            f"| **{category}** | {raw_bytes} B | "
            f"{o200k_tokens} t | {cl100k_tokens} t | "
            f"{gpt2_tokens} t | {bert_tokens} t |"
        )

    report_content = "\n".join(report)
    print(report_content)

    # Save to a notes file
    output_path = os.path.join(os.path.dirname(__file__), "../README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\nReport saved successfully to {output_path}")


if __name__ == "__main__":
    run_benchmark()
