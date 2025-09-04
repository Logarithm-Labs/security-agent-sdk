class InvalidInputDataError(Exception):
    """
    Error raised when input payload fails JSON Schema validation.

    This exception indicates that the provided input data does not conform to
    the expected JSON Schema used for validation.
    """


class InvalidOutputDataError(Exception):
    """
    Error raised when output payload fails JSON Schema validation.

    This exception indicates that the produced output data does not conform to
    the expected JSON Schema used for validation.
    """
