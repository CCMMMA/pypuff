from __future__ import annotations


class PyPuffError(Exception):
    """Base exception for pypuff."""


class ConfigurationError(PyPuffError, ValueError):
    """Raised when a suite configuration is invalid."""


class DataFormatError(PyPuffError, ValueError):
    """Raised when an input data file cannot be parsed safely."""


class ParallelExecutionError(PyPuffError, RuntimeError):
    """Raised when requested parallel execution cannot be initialized."""
