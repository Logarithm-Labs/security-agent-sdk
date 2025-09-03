from pydantic import BaseModel, ConfigDict, Field


class VulnerabilityCount(BaseModel):
    model_config = ConfigDict(extra="forbid")
    high: int = 0
    medium: int = 0
    low: int = 0
    informational: int = 0
    optimization: int = 0


class AuditResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    audited_files: int = Field(..., ge=0)
    audited_contracts: int = Field(..., ge=0)
    vulnerability_count: VulnerabilityCount = Field()
    total_lines: int = Field(..., ge=0)
    security_score: float = Field(..., ge=0.0, le=100.0, description="0-100")
