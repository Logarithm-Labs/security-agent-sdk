from security_agent_sdk.models.input import RequirementScheme
from security_agent_sdk.validation import schema_path, validate_input_data


def test_requirement_scheme_model():
    data = {
        "contracts": [{"address": "0xdef", "chain_id": 1}],
        "github_repo_url": "https://github.com/org/repo",
    }
    obj = RequirementScheme(**data)
    assert obj.contracts[0].address == "0xdef"
    assert obj.contracts[0].chain_id == 1


def test_requirement_scheme_schema_validation():
    data = {
        "contracts": [{"address": "0xdef", "chain_id": 1}],
        "github_repo_url": "https://github.com/org/repo",
    }
    validate_input_data(data, schema_path("RequirementScheme.json"))
