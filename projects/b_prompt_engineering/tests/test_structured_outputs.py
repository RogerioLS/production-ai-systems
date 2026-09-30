"""Comprehensive unit test suite for LAB-06 Structured Outputs, Resilient Parsers & Self-Healing."""

import json
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from projects.b_prompt_engineering.src.lab_06_structured_outputs import (
    ContractObligation,
    ContractParty,
    CurrencyCode,
    ExtractionStrategy,
    FinancialContract,
    PartyType,
    RobustJSONParser,
    SchemaPromptBuilder,
    SelfHealingExhaustedError,
    StrategyBenchmark,
    StructuredOutputError,
    StructuredOutputExtractor,
    SyntaxParseError,
    XMLTagParser,
)


class TestSchemas:
    """Tests for Pydantic v2 domain schemas and custom validators."""

    def test_contract_party_valid(self) -> None:
        party = ContractParty(
            name="Alpha Corp Inc",
            tax_id="  12.345.678/0001-90  ",
            role="Supplier",
            party_type=PartyType.CORPORATION,
        )
        assert party.name == "Alpha Corp Inc"
        assert party.tax_id == "12.345.678/0001-90"  # Whitespace sanitized
        assert party.party_type == PartyType.CORPORATION

    def test_contract_party_empty_tax_id_fails(self) -> None:
        with pytest.raises(ValidationError):
            ContractParty(name="Test", tax_id="   ", role="Client")

    def test_contract_obligation_valid(self) -> None:
        obl = ContractObligation(
            description="Deliver phase 1 backend API",
            due_date="2026-12-31",
            penalty_rate_pct=2.5,
        )
        assert obl.penalty_rate_pct == 2.5

    def test_contract_obligation_invalid_penalty_fails(self) -> None:
        with pytest.raises(ValidationError):
            ContractObligation(
                description="Deliver product",
                penalty_rate_pct=-1.0,
            )
        with pytest.raises(ValidationError):
            ContractObligation(
                description="Deliver product",
                penalty_rate_pct=105.0,
            )

    def test_financial_contract_valid(self) -> None:
        contract = FinancialContract(
            contract_id="CNT-2026-999",
            title="Cloud Infrastructure Provisioning",
            parties=[
                ContractParty(
                    name="Global Cloud Ltd",
                    tax_id="US-998877",
                    role="Provider",
                ),
                ContractParty(
                    name="Enterprise Bank",
                    tax_id="BR-112233",
                    role="Client",
                ),
            ],
            total_value=500000.0,
            currency=CurrencyCode.USD,
            effective_date="2026-01-01",
            expiration_date="2027-01-01",
            obligations=[
                ContractObligation(description="99.99% SLA Uptime Guarantee", penalty_rate_pct=5.0)
            ],
        )
        assert contract.contract_id == "CNT-2026-999"
        assert contract.total_value == 500000.0
        assert len(contract.parties) == 2

    def test_financial_contract_invalid_value_fails(self) -> None:
        with pytest.raises(ValidationError):
            FinancialContract(
                contract_id="CNT-01",
                title="Test",
                parties=[ContractParty(name="Valid Name", tax_id="TAX-001", role="Role")],
                total_value=-100.0,
                effective_date="2026-01-01",
            )

    def test_financial_contract_invalid_date_format_fails(self) -> None:
        with pytest.raises(ValidationError):
            FinancialContract(
                contract_id="CNT-01",
                title="Test",
                parties=[ContractParty(name="Valid Name", tax_id="TAX-001", role="Role")],
                total_value=100.0,
                effective_date="01/01/2026",  # Not ISO YYYY-MM-DD
            )

    def test_financial_contract_chronology_violation_fails(self) -> None:
        with pytest.raises(ValidationError):
            FinancialContract(
                contract_id="CNT-01",
                title="Test",
                parties=[ContractParty(name="Valid Name", tax_id="TAX-001", role="Role")],
                total_value=100.0,
                effective_date="2026-10-01",
                expiration_date="2026-01-01",  # Before effective date!
            )


class TestParsers:
    """Tests for RobustJSONParser and XMLTagParser."""

    def test_strip_markdown_fences(self) -> None:
        fenced_json = '```json\n{"key": "value"}\n```'
        fenced_plain = '```\n{"key": "value"}\n```'
        raw_plain = '{"key": "value"}'

        assert RobustJSONParser.strip_markdown_fences(fenced_json) == '{"key": "value"}'
        assert RobustJSONParser.strip_markdown_fences(fenced_plain) == '{"key": "value"}'
        assert RobustJSONParser.strip_markdown_fences(raw_plain) == '{"key": "value"}'

    def test_fix_trailing_commas(self) -> None:
        bad_json = '{"a": 1, "b": [2, 3,], "c": {"d": 4,},}'
        fixed = RobustJSONParser.fix_trailing_commas(bad_json)
        assert json.loads(fixed) == {"a": 1, "b": [2, 3], "c": {"d": 4}}

    def test_extract_balanced_json(self) -> None:
        conversational = (
            "Here is the result you requested:\n\n"
            '{"name": "test", "items": [1, 2, 3]}\n\n'
            "Let me know if you need anything else!"
        )
        extracted = RobustJSONParser.extract_balanced_json(conversational)
        assert extracted == '{"name": "test", "items": [1, 2, 3]}'

    def test_robust_json_parser_success(self) -> None:
        messy_output = (
            "Sure! Here is the JSON:\n"
            "```json\n"
            "{\n"
            '  "title": "MSA",\n'
            '  "value": 1500.50,\n'
            '  "items": ["a", "b",],\n'
            "}\n"
            "```"
        )
        parsed = RobustJSONParser.parse(messy_output)
        assert parsed["title"] == "MSA"
        assert parsed["value"] == 1500.50
        assert parsed["items"] == ["a", "b"]

    def test_robust_json_parser_unfixable_raises(self) -> None:
        with pytest.raises(SyntaxParseError):
            RobustJSONParser.parse("This is complete nonsense without any brackets.")

    def test_xml_tag_parser_success(self) -> None:
        xml_text = (
            "<financialcontract>\n"
            "  <contract_id>CNT-123</contract_id>\n"
            "  <title>Service Agreement</title>\n"
            "  <total_value>7500.0</total_value>\n"
            "  <currency>USD</currency>\n"
            "  <effective_date>2026-05-01</effective_date>\n"
            "  <parties>\n"
            "    <item>\n"
            "      <name>Alpha Corp</name>\n"
            "      <tax_id>TAX-001</tax_id>\n"
            "      <role>Client</role>\n"
            "      <party_type>corporation</party_type>\n"
            "    </item>\n"
            "  </parties>\n"
            "</financialcontract>"
        )
        parsed = XMLTagParser.parse(xml_text, root_tag="financialcontract")
        assert parsed["contract_id"] == "CNT-123"
        assert parsed["total_value"] == 7500.0
        assert parsed["parties"][0]["name"] == "Alpha Corp"

    def test_xml_tag_parser_invalid_raises(self) -> None:
        with pytest.raises(SyntaxParseError):
            XMLTagParser.parse("<unclosed>Broken XML")


class TestPromptBuilders:
    """Tests for SchemaPromptBuilder."""

    def test_build_system_prompts(self) -> None:
        builder = SchemaPromptBuilder()
        json_prompt = builder.build_system_prompt(
            FinancialContract, ExtractionStrategy.JSON_SCHEMA_STRICT
        )
        xml_prompt = builder.build_system_prompt(FinancialContract, ExtractionStrategy.XML_TAGS)
        raw_prompt = builder.build_system_prompt(FinancialContract, ExtractionStrategy.RAW_JSON)

        assert "TARGET JSON SCHEMA" in json_prompt
        assert "<financialcontract>" in xml_prompt
        assert "RAW_JSON" not in raw_prompt
        assert "contract_id" in raw_prompt

    def test_build_repair_messages(self) -> None:
        builder = SchemaPromptBuilder()
        msgs = builder.build_repair_messages(
            original_prompt="Extract contract",
            failed_raw_output="{'invalid': true}",
            error_details="Field required: contract_id",
            attempt=1,
            model_cls=FinancialContract,
        )
        assert len(msgs) == 2
        assert msgs[0]["role"] == "system"
        assert "ATTEMPT #1 FAILED OUTPUT" in msgs[1]["content"]
        assert "Field required: contract_id" in msgs[1]["content"]


class TestStructuredOutputExtractor:
    """Tests for the StructuredOutputExtractor engine and Self-Healing reflection loops."""

    def test_extractor_missing_callable_raises(self) -> None:
        extractor = StructuredOutputExtractor(target_model=FinancialContract)
        with pytest.raises(StructuredOutputError):
            extractor.extract("some document")

    def test_extractor_single_attempt_success(self) -> None:
        valid_payload = {
            "contract_id": "CNT-001",
            "title": "Software SLA",
            "parties": [{"name": "Tech Corp", "tax_id": "TAX-12345", "role": "Vendor"}],
            "total_value": 12000.0,
            "currency": "USD",
            "effective_date": "2026-01-01",
        }

        mock_llm = MagicMock(return_value=json.dumps(valid_payload))
        extractor = StructuredOutputExtractor(
            target_model=FinancialContract,
            llm_callable=mock_llm,
        )

        result = extractor.extract("Contract document text")
        assert result.is_success is True
        assert result.attempts == 1
        assert result.data is not None
        assert result.data.contract_id == "CNT-001"
        assert len(result.validation_errors) == 0

    def test_extractor_self_healing_recovery(self) -> None:
        # Attempt 1: missing required field 'contract_id' and trailing comma
        bad_payload = (
            "```json\n"
            "{\n"
            '  "title": "Software SLA",\n'
            '  "parties": [{"name": "Tech Corp", "tax_id": "TAX-12345", "role": "Vendor"}],\n'
            '  "total_value": 12000.0,\n'
            '  "currency": "USD",\n'
            '  "effective_date": "2026-01-01",\n'
            "}\n"
            "```"
        )
        # Attempt 2 (Repaired via reflection): includes 'contract_id'
        repaired_payload = {
            "contract_id": "CNT-RECOVERED",
            "title": "Software SLA",
            "parties": [{"name": "Tech Corp", "tax_id": "TAX-12345", "role": "Vendor"}],
            "total_value": 12000.0,
            "currency": "USD",
            "effective_date": "2026-01-01",
        }

        mock_llm = MagicMock(side_effect=[bad_payload, json.dumps(repaired_payload)])
        extractor = StructuredOutputExtractor(
            target_model=FinancialContract,
            max_retries=3,
            llm_callable=mock_llm,
        )

        result = extractor.extract("Contract document text")
        assert result.is_success is True
        assert result.attempts == 2
        assert result.data is not None
        assert result.data.contract_id == "CNT-RECOVERED"
        assert len(result.validation_errors) == 1
        assert "contract_id" in result.validation_errors[0]

    def test_extractor_exhausted_retries_returns_failure(self) -> None:
        mock_llm = MagicMock(return_value="completely invalid json")
        extractor = StructuredOutputExtractor(
            target_model=FinancialContract,
            max_retries=2,
            llm_callable=mock_llm,
        )

        result = extractor.extract("Contract text")
        assert result.is_success is False
        assert result.attempts == 2
        assert result.data is None
        assert len(result.validation_errors) == 2

    def test_extractor_exhausted_retries_raises_when_requested(self) -> None:
        mock_llm = MagicMock(return_value="completely invalid json")
        extractor = StructuredOutputExtractor(
            target_model=FinancialContract,
            max_retries=2,
            llm_callable=mock_llm,
        )

        with pytest.raises(SelfHealingExhaustedError):
            extractor.extract("Contract text", raise_on_failure=True)

    def test_extractor_xml_strategy_success(self) -> None:
        xml_response = (
            "<financialcontract>\n"
            "  <contract_id>CNT-XML-01</contract_id>\n"
            "  <title>Hardware Supply</title>\n"
            "  <total_value>99000.0</total_value>\n"
            "  <currency>USD</currency>\n"
            "  <effective_date>2026-02-01</effective_date>\n"
            "  <parties>\n"
            "    <item>\n"
            "      <name>Dell Corp</name>\n"
            "      <tax_id>TAX-DELL</tax_id>\n"
            "      <role>Supplier</role>\n"
            "    </item>\n"
            "  </parties>\n"
            "</financialcontract>"
        )
        mock_llm = MagicMock(return_value=xml_response)
        extractor = StructuredOutputExtractor(
            target_model=FinancialContract,
            strategy=ExtractionStrategy.XML_TAGS,
            llm_callable=mock_llm,
        )

        result = extractor.extract("Contract text")
        assert result.is_success is True
        assert result.data is not None
        assert result.data.contract_id == "CNT-XML-01"

    def test_extractor_with_instructor_mock(self) -> None:
        mock_client = MagicMock()
        expected_contract = FinancialContract(
            contract_id="CNT-INST-01",
            title="Licensing",
            parties=[ContractParty(name="Client Corp", tax_id="TAX-001", role="Client")],
            total_value=5000.0,
            currency=CurrencyCode.USD,
            effective_date="2026-03-01",
        )
        mock_client.chat.completions.create.return_value = expected_contract

        extractor = StructuredOutputExtractor(target_model=FinancialContract)
        result = extractor.extract_with_instructor(
            client=mock_client,
            text="Extract license contract",
        )
        assert result.is_success is True
        assert result.data == expected_contract
        assert result.strategy == ExtractionStrategy.INSTRUCTOR


class TestBenchmarking:
    """Tests for StrategyBenchmark evaluation and reporting."""

    def test_benchmark_evaluation_and_table(self) -> None:
        benchmark = StrategyBenchmark(target_model=FinancialContract)

        valid_payload = json.dumps(
            {
                "contract_id": "CNT-BENCH",
                "title": "Benchmarking Contract",
                "parties": [
                    {
                        "name": "Benchmark Party",
                        "tax_id": "TAX-12345",
                        "role": "Client",
                    }
                ],
                "total_value": 1000.0,
                "currency": "USD",
                "effective_date": "2026-01-01",
            }
        )

        def mock_factory(test_case: str):
            if "fail" in test_case:
                return lambda msgs: "broken"
            return lambda msgs: valid_payload

        report = benchmark.evaluate_strategy(
            strategy=ExtractionStrategy.JSON_SCHEMA_STRICT,
            test_cases=["good document", "fail document"],
            llm_callable_factory=mock_factory,
            max_retries=2,
        )

        assert report.total_runs == 2
        assert report.successful_runs == 1
        assert report.success_rate_pct == 50.0
        assert report.syntax_errors > 0

        markdown = StrategyBenchmark.generate_markdown_table([report])
        assert "| **json_schema_strict** |" in markdown
        assert "50.0%" in markdown
