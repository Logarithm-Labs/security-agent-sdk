from security_agent_sdk.models.request import AuditRequest
from security_agent_sdk.validation import schema_path, validate_input_data


def test_audit_request_model():
    data = {
        "vault": {
            "address": "0x1234567890123456789012345678901234567890",
            "chain": "ethereum",
        },
        "contracts": [
            {
                "address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "chain": "ethereum",
            }
        ],
        "github_repo_url": "https://github.com/org/repo",
    }
    obj = AuditRequest(**data)
    assert obj.vault.address == "0x1234567890123456789012345678901234567890"
    assert obj.vault.chain == "ethereum"
    assert obj.contracts[0].address == "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
    assert obj.contracts[0].chain == "ethereum"


def test_audit_request_schema_validation():
    data = {
        "vault": {
            "address": "0x1234567890123456789012345678901234567890",
            "chain": "ethereum",
        },
        "contracts": [
            {
                "address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "chain": "ethereum",
            }
        ],
        "github_repo_url": "https://github.com/org/repo",
    }
    validate_input_data(data, schema_path("AuditRequest.json"))
