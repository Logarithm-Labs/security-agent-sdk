# Security Agent SDK

Python SDK that defines data models and JSON Schemas for interoperability between a crypto agent and auditor agents.

## Installation

```bash
pip install security_agent_sdk
```

or with Poetry:

```bash
poetry add security_agent_sdk
```

## Quick start

```python
from security_agent_sdk.models.input import RequirementScheme
from security_agent_sdk.models.output import AuditSummary
from security_agent_sdk.validation import validate_input_data, validate_output_data, schema_path

# Validate input data (JSON object)
validate_input_data(data, schema_path("input/v1/RequirementScheme.json"))
req = RequirementScheme(**data)

# Validate output data
validate_output_data(result, schema_path("output/v1/AuditResult.json"))
summary = AuditSummary(**result)
```

## License

MIT
