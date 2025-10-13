"""Module for custom exceptions."""

class InsufficientOperandsError(Exception):
    """Custom exception for when an operation requires more operands."""
    pass

class InvalidOperationError(ValueError):
    """Custom exception for unknown or invalid operations."""
    pass