# 📊 Tokenization Compression Benchmark Report

This report benchmarks BPE vs WordPiece tokenization efficiency across different domains.

## Compression Ratio (Bytes / Token)
> Higher is better. A higher ratio means more text bytes compressed into fewer tokens.

| Category | GPT-4o (o200k_base) | GPT-4 (cl100k_base) | GPT-2 (gpt2) | BERT (bert-uncased) |
| --- | --- | --- | --- | --- |
| **Plain English** | 5.200 B/T | 5.200 B/T | 5.200 B/T | 5.200 B/T |
| **Portuguese (PT-BR)** | 5.848 B/T | 4.825 B/T | 3.063 B/T | 3.509 B/T |
| **Structured JSON** | 2.735 B/T | 2.735 B/T | 2.548 B/T | 2.114 B/T |
| **Numeric / Tabular** | 1.737 B/T | 1.737 B/T | 2.000 B/T | 1.886 B/T |
| **Emojis / Special Chars** | 2.077 B/T | 1.620 B/T | 1.446 B/T | 10.125 B/T |

## Token Count Comparison

| Category | UTF-8 Bytes | GPT-4o (o200k_base) | GPT-4 (cl100k_base) | GPT-2 (gpt2) | BERT (bert-uncased) |
| --- | --- | --- | --- | --- | --- |
| **Plain English** | 156 B | 30 t | 30 t | 30 t | 30 t |
| **Portuguese (PT-BR)** | 193 B | 33 t | 40 t | 63 t | 55 t |
| **Structured JSON** | 186 B | 68 t | 68 t | 73 t | 88 t |
| **Numeric / Tabular** | 66 B | 38 t | 38 t | 33 t | 35 t |
| **Emojis / Special Chars** | 81 B | 39 t | 50 t | 56 t | 8 t |
