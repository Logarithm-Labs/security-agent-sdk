import json
from pathlib import Path
from typing import Any, Dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pydantic import field_validator
from yield_analysis_sdk.validators import normalize_address

from .exceptions import InvalidInputDataError, InvalidOutputDataError


class AddressValidatorMixin:
    """Mixin class that provides address validation functionality."""

    @field_validator("address", mode="before")
    @classmethod
    def validate_address(cls, v) -> str:
        """Validate address format and normalize it."""
        if isinstance(v, str):
            return normalize_address(v)
        elif v is None:
            raise InvalidInputDataError("Address cannot be None")
        else:
            return str(v)


def schema_path(relative: str) -> str:
    """
    Return absolute path to schema within the tests directory.

    Args:
        relative: Path inside the tests/schemas directory, e.g. "RequirementScheme.json".

    Returns:
        Absolute filesystem path to the requested schema file.
    """
    base = Path(__file__).resolve().parent.parent / "tests" / "schemas"
    return str(base.joinpath(relative))


def validate_input_data(data: Dict[str, Any], schema_file_path: str) -> None:
    """
    Validate input data against the provided JSON Schema.

    Args:
        data: Input payload to be validated.
        schema_file_path: Absolute path to JSON Schema file for input validation.

    Raises:
        FileNotFoundError: If the schema file cannot be found.
        InvalidInputDataError: If the input data does not conform to the schema.
        Exception: For any other unexpected validation errors.
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
    """
    Validate output data against the provided JSON Schema.

    Args:
        data: Output payload produced by the agent.
        schema_file_path: Absolute path to JSON Schema file for output validation.

    Raises:
        FileNotFoundError: If the schema file cannot be found.
        InvalidOutputDataError: If the output data does not conform to the schema.
        Exception: For any other unexpected validation errors.
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
