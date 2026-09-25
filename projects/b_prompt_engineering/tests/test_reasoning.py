"""Comprehensive test suite for LAB-05: Prompt Reasoning Patterns."""

import pytest

from projects.b_prompt_engineering.src.lab_05_reasoning.chain_of_thought import (
    ChainOfThoughtPromptEngine,
    SelfConsistencyEngine,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.exceptions import (
    ExemplarSelectionError,
    ReActExecutionError,
    SelfConsistencyError,
    TemplateError,
    ToolNotFoundError,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.few_shot import FewShotPromptEngine
from projects.b_prompt_engineering.src.lab_05_reasoning.react import ReActEngine
from projects.b_prompt_engineering.src.lab_05_reasoning.templates import (
    ChatPromptTemplate,
    PromptTemplate,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.types import (
    Exemplar,
    PromptRole,
)


class TestPromptTemplates:
    """Tests for single and multi-turn prompt templating systems."""

    def test_single_prompt_template_success(self) -> None:
        template = PromptTemplate(
            template="Analyze stock {ticker} for fiscal year {year}.",
            role=PromptRole.USER,
        )
        assert template.variables == {"ticker", "year"}
        formatted = template.format(ticker="AAPL", year="2025")
        assert formatted == "Analyze stock AAPL for fiscal year 2025."

        msg = template.format_message(ticker="AAPL", year="2025")
        assert msg.role == PromptRole.USER
        assert msg.content == "Analyze stock AAPL for fiscal year 2025."

    def test_empty_template_raises_error(self) -> None:
        with pytest.raises(TemplateError, match="cannot be empty"):
            PromptTemplate(template="   ")

    def test_missing_variables_raises_error(self) -> None:
        template = PromptTemplate("Hello {name}, your code is {code}.")
        with pytest.raises(TemplateError, match="Missing required template variables"):
            template.format(name="Alice")

    def test_chat_prompt_template_multi_turn(self) -> None:
        system = PromptTemplate(
            "You are an AI financial auditor for {firm}.", role=PromptRole.SYSTEM
        )
        user = PromptTemplate("Inspect balance sheet for {company}.", role=PromptRole.USER)

        chat_tmpl = ChatPromptTemplate(messages=[system, user])
        assert chat_tmpl.variables == {"firm", "company"}

        turns = chat_tmpl.format_messages(firm="Goldman", company="Petrobras")
        assert len(turns) == 2
        assert turns[0].role == PromptRole.SYSTEM
        assert turns[0].content == "You are an AI financial auditor for Goldman."
        assert turns[1].role == PromptRole.USER
        assert turns[1].content == "Inspect balance sheet for Petrobras."

        flat = chat_tmpl.to_single_prompt(firm="Goldman", company="Petrobras")
        assert "[SYSTEM]" in flat
        assert "[USER]" in flat


class TestFewShotPromptEngine:
    """Tests for in-context exemplar registration and dynamic assembly."""

    def test_zero_shot_fallback_when_empty_pool(self) -> None:
        engine = FewShotPromptEngine()
        prompt = engine.build_prompt("Translate 'apple' to Portuguese.")
        assert "Translate 'apple' to Portuguese." in prompt

    def test_few_shot_registration_and_k_limit(self) -> None:
        engine = FewShotPromptEngine()
        ex1 = Exemplar(input_text="2 + 2", output_text="4", reasoning="Addition of two twos")
        ex2 = Exemplar(
            input_text="3 * 3", output_text="9", reasoning="Multiplication of three by three"
        )
        ex3 = Exemplar(input_text="10 / 2", output_text="5", reasoning="Division of ten by two")

        engine.register_exemplars([ex1, ex2, ex3])
        prompt_k2 = engine.build_prompt("5 + 5", k=2)

        assert "Input: 2 + 2" in prompt_k2
        assert "Input: 3 * 3" in prompt_k2
        assert "Input: 10 / 2" not in prompt_k2
        assert "Input: 5 + 5" in prompt_k2

    def test_custom_dynamic_exemplar_selector(self) -> None:
        engine = FewShotPromptEngine()
        ex_math = Exemplar(input_text="calc: 4+4", output_text="8", metadata={"domain": "math"})
        ex_text = Exemplar(input_text="text: hello", output_text="olá", metadata={"domain": "text"})
        engine.register_exemplars([ex_math, ex_text])

        def domain_selector(query: str, pool: list[Exemplar], limit: int) -> list[Exemplar]:
            domain = "math" if "calc" in query else "text"
            return [ex for ex in pool if ex.metadata.get("domain") == domain][:limit]

        prompt = engine.build_prompt("calc: 10+10", selector=domain_selector)
        assert "calc: 4+4" in prompt
        assert "text: hello" not in prompt

    def test_empty_query_raises_error(self) -> None:
        engine = FewShotPromptEngine()
        with pytest.raises(ExemplarSelectionError, match="cannot be empty"):
            engine.build_prompt("   ")


class TestChainOfThoughtAndSelfConsistency:
    """Tests for CoT induction and Self-Consistency majority voting."""

    def test_zero_shot_cot_wrapper(self) -> None:
        q = "If John has 5 apples and eats 2, how many remain?"
        prompt = ChainOfThoughtPromptEngine.wrap_zero_shot_cot(q)
        assert "Let's think step by step:" in prompt
        assert q in prompt

    def test_extract_final_answer_from_cot(self) -> None:
        response = (
            "First, John starts with 5 apples.\n"
            "Then, he consumes 2 apples.\n"
            "5 minus 2 is 3.\n"
            "Therefore, the final answer is: 3"
        )
        ans = ChainOfThoughtPromptEngine.extract_final_answer(response)
        assert ans == "3"

    def test_self_consistency_unanimous_consensus(self) -> None:
        sc = SelfConsistencyEngine()
        candidates = ["42", "42", "42", "42"]
        res = sc.evaluate_consensus(candidates)
        assert res.winning_answer == "42"
        assert res.confidence_score == 1.0
        assert res.shannon_entropy == 0.0

    def test_self_consistency_majority_vote_with_dispersion(self) -> None:
        sc = SelfConsistencyEngine()
        candidates = ["10", "10", "10", "12", "15"]
        res = sc.evaluate_consensus(candidates)
        assert res.winning_answer == "10"
        assert res.confidence_score == 0.6
        assert res.vote_distribution == {"10": 3, "12": 1, "15": 1}
        assert res.shannon_entropy > 0.0

    def test_self_consistency_empty_candidates_error(self) -> None:
        sc = SelfConsistencyEngine()
        with pytest.raises(SelfConsistencyError, match="cannot be empty"):
            sc.evaluate_consensus([])

    def test_self_consistency_sample_and_vote(self) -> None:
        sc = SelfConsistencyEngine()

        def mock_llm(prompt: str) -> str:
            return "Thinking step-by-step...\nFinal Answer: 100"

        res = sc.sample_and_vote("What is 10 * 10?", sampler_fn=mock_llm, num_samples=3)
        assert res.winning_answer == "100"
        assert res.confidence_score == 1.0


class TestReActAutonomousEngine:
    """Tests for ReAct cognitive cycle (Thought -> Action -> Observation -> Final Answer)."""

    def test_register_and_execute_tool(self) -> None:
        engine = ReActEngine()

        def add(a: int, b: int) -> int:
            return a + b

        engine.register_tool(
            name="calculator",
            description="Adds two integers",
            handler=add,
        )

        res = engine.execute_tool("calculator", {"a": 10, "b": 25})
        assert res == "35"

    def test_execute_unknown_tool_raises_error(self) -> None:
        engine = ReActEngine()
        with pytest.raises(ToolNotFoundError, match="Tool 'crypto_swap' not found"):
            engine.execute_tool("crypto_swap", {})

    def test_react_autonomous_loop_success(self) -> None:
        engine = ReActEngine(max_iterations=5)

        # Mock database tool
        def get_company_revenue(ticker: str) -> str:
            database = {"VALE3": "$42 Billion USD", "PETR4": "$98 Billion USD"}
            return database.get(ticker.upper(), "Ticker not found.")

        engine.register_tool(
            name="lookup_revenue",
            description="Returns revenue for a stock ticker",
            handler=get_company_revenue,
        )

        # Mock simulated LLM that performs 1 tool call then gives final answer
        def mock_react_llm(trajectory: str) -> str:
            if "Observation: $98 Billion USD" in trajectory:
                return (
                    "Thought: I now have the revenue for PETR4.\n"
                    "Final Answer: The revenue of PETR4 is $98 Billion USD."
                )
            return (
                "Thought: I need to query the database for PETR4 revenue.\n"
                "Action: lookup_revenue\n"
                'Action Input: {"ticker": "PETR4"}\n'
            )

        result = engine.run(
            task="Find the annual revenue of PETR4.",
            llm_responder=mock_react_llm,
        )

        assert result.success is True
        assert "98 Billion USD" in result.final_answer
        assert len(result.steps) == 2
        assert result.steps[0].action_tool == "lookup_revenue"
        assert result.steps[0].observation == "$98 Billion USD"

    def test_react_max_iterations_exceeded(self) -> None:
        engine = ReActEngine(max_iterations=2)

        def mock_infinite_loop_llm(trajectory: str) -> str:
            return "Thought: Thinking constantly...\n" "Action: fake_tool\n" "Action Input: {}\n"

        engine.register_tool("fake_tool", "Does nothing", lambda: "ok")

        with pytest.raises(ReActExecutionError, match="exceeded maximum allowable iterations"):
            engine.run("Infinite loop task", mock_infinite_loop_llm)
