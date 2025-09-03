from security_agent_sdk.models.output import AuditResult
from security_agent_sdk.validation import schema_path, validate_output_data


def test_audit_result_model():
    data = {
        "audited_files": 13,
        "audited_contracts": 11,
        "vulnerability_count": {
            "high": 0,
            "medium": 1,
            "low": 14,
            "informational": 7,
            "optimization": 0,
        },
        "total_lines": 2527,
        "security_score": 98.5,
    }
    obj = AuditResult(**data)
    assert obj.audited_files == 13
    assert obj.vulnerability_count.low == 14


def test_audit_result_schema_validation():
    data = {
        "audited_files": 13,
        "audited_contracts": 11,
        "vulnerability_count": {
            "high": 0,
            "medium": 1,
            "low": 14,
            "informational": 7,
            "optimization": 0,
        },
        "total_lines": 2527,
        "security_score": 98.5,
    }
    validate_output_data(data, schema_path("AuditResult.json"))
