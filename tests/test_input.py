from security_agent_sdk.models.input import RequirementScheme, Vault, Contract
from security_agent_sdk.validation import validate_input_data, schema_path


def test_requirement_scheme_model():
    data = {
        "vault": {"vault_address": "0xabc", "chain": 1},
        "contracts": [{"address": "0xdef", "chain": 1}],
        "github_repo_url": "https://github.com/org/repo",
    }
    obj = RequirementScheme(**data)
    assert obj.vault.vault_address == "0xabc"
    assert obj.contracts[0].address == "0xdef"


def test_requirement_scheme_schema_validation():
    data = {
        "vault": {"vault_address": "0xabc", "chain": 1},
        "contracts": [{"address": "0xdef", "chain": 1}],
        "github_repo_url": "https://github.com/org/repo",
    }
    validate_input_data(data, schema_path("input/v1/RequirementScheme.json"))


