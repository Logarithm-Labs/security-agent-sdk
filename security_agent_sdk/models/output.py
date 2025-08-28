from typing import Dict, Optional

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class VulnerabilityCount(BaseModel):
    model_config = ConfigDict(extra="forbid")
    high: int = 0
    medium: int = 0
    low: int = 0
    informational: int = 0
    optimization: int = 0


class AuditSummary(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auditedFiles: int = Field(..., ge=0, alias="auditedFiles")
    auditedContracts: int = Field(..., ge=0, alias="auditedContracts")
    vulnerabilityCount: VulnerabilityCount = Field(alias="vulnerabilityCount")
    totalLines: int = Field(..., ge=0, alias="totalLines")
    securityScore: float = Field(..., ge=0.0, le=100.0, description="0-100", alias="securityScore")


