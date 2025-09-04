from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class VulnerabilityCount(BaseModel):
    """Vulnerability count model for security agent vault report."""

    high: int = 0
    medium: int = 0
    low: int = 0
    informational: int = 0
    optimization: int = 0


class AuditResponse(BaseModel):
    """Audit report model for security agent vault report."""

    audited_files: int = Field(..., ge=0)
    audited_contracts: int = Field(..., ge=0)
    vulnerability_count: VulnerabilityCount = Field()
    total_lines: int = Field(..., ge=0)
    security_score: float = Field(..., ge=0.0, le=100.0, description="0-100")
    extra_info: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional information about the vault"
    )
