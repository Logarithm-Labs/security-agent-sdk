from security_agent_sdk.models.response import AuditResponse
from security_agent_sdk.validation import schema_path, validate_output_data


def test_audit_response_model():
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
        "extra_info": {"analyzed_at": "2024-01-01T00:00:00Z"},
    }
    obj = AuditResponse(**data)
    assert obj.audited_files == 13
    assert obj.vulnerability_count.low == 14
    assert obj.extra_info["analyzed_at"] == "2024-01-01T00:00:00Z"


def test_audit_response_schema_validation():
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
    validate_output_data(data, schema_path("AuditResponse.json"))
