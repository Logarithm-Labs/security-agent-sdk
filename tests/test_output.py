from security_agent_sdk.models.output import AuditSummary, VulnerabilityCount
from security_agent_sdk.validation import validate_output_data, schema_path


def test_audit_summary_model():
    data = {
        "auditedFiles": 13,
        "auditedContracts": 11,
        "vulnerabilityCount": {
            "high": 0,
            "medium": 1,
            "low": 14,
            "informational": 7,
            "optimization": 0,
        },
        "totalLines": 2527,
        "securityScore": 98.5,
    }
    obj = AuditSummary(**data)
    assert obj.auditedFiles == 13
    assert obj.vulnerabilityCount.low == 14


def test_audit_summary_schema_validation():
    data = {
        "auditedFiles": 13,
        "auditedContracts": 11,
        "vulnerabilityCount": {
            "high": 0,
            "medium": 1,
            "low": 14,
            "informational": 7,
            "optimization": 0,
        },
        "totalLines": 2527,
        "securityScore": 98.5,
    }
    validate_output_data(data, schema_path("output/v1/AuditResult.json"))


