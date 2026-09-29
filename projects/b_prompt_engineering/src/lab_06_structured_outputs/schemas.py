"""Pydantic v2 schemas, domain models, and data types for structured output extraction."""

from datetime import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PartyType(str, Enum):
    """Categorization of contract counterparties."""

    INDIVIDUAL = "individual"
    CORPORATION = "corporation"
    GOVERNMENT = "government"


class CurrencyCode(str, Enum):
    """Standard ISO currency codes supported."""

    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class ExtractionStrategy(str, Enum):
    """Strategies for requesting and enforcing structured outputs from LLMs."""

    RAW_JSON = "raw_json"
    XML_TAGS = "xml_tags"
    JSON_SCHEMA_STRICT = "json_schema_strict"
    INSTRUCTOR = "instructor"


class ContractParty(BaseModel):
    """Represents a legal or natural entity in a commercial agreement."""

    model_config = ConfigDict(strict=False, extra="forbid")

    name: str = Field(..., min_length=2, description="Full legal name of the entity")
    tax_id: str = Field(
        ...,
        min_length=5,
        description="Official tax identifier (e.g., CNPJ, CPF, EIN, VAT)",
    )
    role: str = Field(
        ...,
        description="Role in contract (e.g., Contractor, Client, Guarantor, Lender)",
    )
    party_type: PartyType = Field(
        default=PartyType.CORPORATION,
        description="Classification of counterparty entity",
    )

    @field_validator("tax_id")
    @classmethod
    def sanitize_tax_id(cls, v: str) -> str:
        """Sanitizes tax ID by stripping leading/trailing whitespace."""
        clean = v.strip()
        if not clean:
            raise ValueError("Tax ID cannot be empty or whitespace.")
        return clean


class ContractObligation(BaseModel):
    """Specific commercial deliverable or milestone obligation."""

    model_config = ConfigDict(strict=False, extra="forbid")

    description: str = Field(..., min_length=5, description="Description of the obligation")
    due_date: Optional[str] = Field(
        default=None,
        description="Due date in YYYY-MM-DD ISO format if specified",
    )
    penalty_rate_pct: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Contractual penalty percentage for non-compliance (0.0 to 100.0)",
    )


class FinancialContract(BaseModel):
    """Enterprise financial contract schema with strict validations."""

    model_config = ConfigDict(strict=False, extra="forbid")

    contract_id: str = Field(..., min_length=3, description="Unique contract identifier")
    title: str = Field(..., min_length=3, description="Descriptive contract title")
    parties: List[ContractParty] = Field(
        ...,
        min_length=1,
        description="List of all participating legal parties",
    )
    total_value: float = Field(..., gt=0.0, description="Total contract monetary valuation")
    currency: CurrencyCode = Field(
        default=CurrencyCode.USD,
        description="ISO currency code",
    )
    effective_date: str = Field(
        ...,
        description="Initial active date in YYYY-MM-DD ISO format",
    )
    expiration_date: Optional[str] = Field(
        default=None,
        description="Contract termination date in YYYY-MM-DD ISO format",
    )
    obligations: List[ContractObligation] = Field(
        default_factory=list,
        description="Operational milestones and duties",
    )

    @field_validator("effective_date", "expiration_date")
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validates that dates follow the ISO YYYY-MM-DD format."""
        if v is None:
            return None
        try:
            datetime.strptime(v.strip(), "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(f"Date '{v}' must match ISO format YYYY-MM-DD.") from exc
        return v.strip()

    @model_validator(mode="after")
    def validate_date_chronology(self) -> "FinancialContract":
        """Ensures expiration date is not chronologically earlier than effective date."""
        if self.expiration_date and self.effective_date:
            eff = datetime.strptime(self.effective_date, "%Y-%m-%d")
            exp = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            if exp < eff:
                raise ValueError(
                    f"Expiration date ({self.expiration_date}) cannot be earlier "
                    f"than effective date ({self.effective_date})."
                )
        return self


T = TypeVar("T", bound=BaseModel)


class ExtractionAttempt(BaseModel):
    """Audit log entry for an extraction iteration."""

    attempt_number: int
    raw_output: str
    error: Optional[str] = None
    was_successful: bool = False


class ExtractionResult(BaseModel, Generic[T]):
    """Standardized response container for structured data extraction."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: Optional[T] = None
    strategy: ExtractionStrategy
    attempts: int = 1
    is_success: bool = False
    raw_outputs: List[str] = Field(default_factory=list)
    validation_errors: List[str] = Field(default_factory=list)
    execution_time_seconds: float = 0.0


class BenchmarkReport(BaseModel):
    """Empirical benchmark summary across extraction runs."""

    strategy: ExtractionStrategy
    total_runs: int
    successful_runs: int
    success_rate_pct: float
    avg_attempts: float
    avg_latency_seconds: float
    syntax_errors: int
    schema_errors: int
