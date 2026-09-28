"""Chain-of-Thought (CoT) and Self-Consistency prompting engines."""

import math
from collections import Counter
from typing import Callable, List, Optional

from loguru import logger

from projects.b_prompt_engineering.src.lab_05_reasoning.exceptions import SelfConsistencyError
from projects.b_prompt_engineering.src.lab_05_reasoning.types import ConsensusResult


class ChainOfThoughtPromptEngine:
    """Standardizes zero-shot and few-shot Chain-of-Thought induction.

    Applies prompt steering to enforce step-by-step mathematical or logical
    deduction before committing to a final answer.
    """

    COT_TRIGGER: str = "Let's think step by step:"

    @classmethod
    def wrap_zero_shot_cot(cls, question: str, trigger: Optional[str] = None) -> str:
        """Wraps a query with zero-shot CoT induction phrase (Kojima et al., 2022)."""
        phrase = trigger or cls.COT_TRIGGER
        return f"Question: {question.strip()}\n\n{phrase}"

    @classmethod
    def extract_final_answer(cls, response_text: str, prefixes: Optional[List[str]] = None) -> str:
        """Heuristic parser to isolate the final answer line from verbose CoT reasoning."""
        default_prefixes = [
            "Therefore, the final answer is:",
            "The final answer is:",
            "Final Answer:",
            "Answer:",
            "Portanto, a resposta é:",
        ]
        target_prefixes = prefixes or default_prefixes

        lines = [line.strip() for line in response_text.strip().splitlines() if line.strip()]
        for line in reversed(lines):
            for prefix in target_prefixes:
                if prefix.lower() in line.lower():
                    idx = line.lower().find(prefix.lower())
                    ans = line[idx + len(prefix) :].strip().strip(".$*#")
                    if ans:
                        return ans

        # Fallback to the very last non-empty line
        return lines[-1] if lines else ""


class SelfConsistencyEngine:
    """Implements Self-Consistency (Wang et al., 2022) with Majority Voting and Shannon Entropy.

    Samples multiple independent reasoning paths from an LLM at non-zero temperature,
    extracts candidate answers, and selects the consensus answer via majority vote.
    """

    @staticmethod
    def compute_shannon_entropy(distribution: Counter) -> float:
        """Calculates information entropy H(X) = - sum(p * log2(p)).

        Higher entropy indicates higher uncertainty and disagreement across samples;
        zero entropy indicates unanimous agreement across all reasoning paths.
        """
        total = sum(distribution.values())
        if total == 0:
            return 0.0

        entropy = 0.0
        for count in distribution.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return float(round(entropy, 4))

    def evaluate_consensus(self, candidate_answers: List[str]) -> ConsensusResult:
        """Calculates majority vote, confidence, and entropy across candidate answers."""
        if not candidate_answers:
            raise SelfConsistencyError(
                "Candidate answers list cannot be empty for consensus evaluation."
            )

        # Normalize answers (lowercase and whitespace stripping)
        normalized = [ans.strip().lower() for ans in candidate_answers if ans.strip()]
        if not normalized:
            raise SelfConsistencyError("No non-empty answers found among candidates.")

        counts = Counter(normalized)
        most_common = counts.most_common(1)
        winner, win_count = most_common[0]

        total_samples = len(normalized)
        confidence = float(round(win_count / total_samples, 4))
        entropy = self.compute_shannon_entropy(counts)

        logger.info(
            f"Consensus evaluated: Winner='{winner}' (Confidence: {confidence * 100:.1f}%, "
            f"Samples: {total_samples}, Entropy: {entropy:.4f})"
        )

        return ConsensusResult(
            candidate_answers=candidate_answers,
            winning_answer=winner,
            confidence_score=confidence,
            vote_distribution=dict(counts),
            shannon_entropy=entropy,
        )

    def sample_and_vote(
        self,
        prompt: str,
        sampler_fn: Callable[[str], str],
        num_samples: int = 5,
        answer_extractor: Optional[Callable[[str], str]] = None,
    ) -> ConsensusResult:
        """Executes multiple stochastic inference calls and computes the consensus result."""
        if num_samples < 1:
            raise SelfConsistencyError("num_samples must be >= 1.")

        extractor = answer_extractor or ChainOfThoughtPromptEngine.extract_final_answer

        candidates: List[str] = []
        for _ in range(num_samples):
            raw_response = sampler_fn(prompt)
            extracted = extractor(raw_response)
            candidates.append(extracted)

        return self.evaluate_consensus(candidates)
