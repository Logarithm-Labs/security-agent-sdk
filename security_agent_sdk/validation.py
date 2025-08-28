import json
from importlib.resources import files
from pathlib import Path
from typing import Any, Dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .exceptions import InvalidInputDataError, InvalidOutputDataError


def schema_path(relative: str) -> str:
    """Return absolute path to schema within the package.

    relative: path inside the schemas directory, e.g. "input/v1/RequirementScheme.json".
    """
    base = files("security_agent_sdk").joinpath("schemas")
    return str(base.joinpath(relative))


def validate_input_data(data: Dict[str, Any], schema_file_path: str) -> None:
    """Validate input data against the provided JSON Schema.

    Raises InvalidInputDataError on mismatch.
    """
    try:
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
        validate(instance=data, schema=schema)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Schema file not found: {schema_file_path}") from e
    except ValidationError as e:
        raise InvalidInputDataError(f"Invalid input data: {e.message}") from e
    except Exception as e:
        raise Exception(f"Unexpected error during input validation: {e}") from e


def validate_output_data(data: Dict[str, Any], schema_file_path: str) -> None:
    """Validate output data against the provided JSON Schema.

    Raises InvalidOutputDataError on mismatch.
    """
    try:
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
        validate(instance=data, schema=schema)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Schema file not found: {schema_file_path}") from e
    except ValidationError as e:
        raise InvalidOutputDataError(f"Invalid output data: {e.message}") from e
    except Exception as e:
        raise Exception(f"Unexpected error during output validation: {e}") from e


