"""Tests for custom exceptions."""
import pytest
from app.exceptions import InsufficientOperandsError, InvalidOperationError

def test_custom_exceptions():
    """Test that custom exceptions can be raised and caught."""
    with pytest.raises(InsufficientOperandsError):
        raise InsufficientOperandsError("Not enough operands")
        
    with pytest.raises(InvalidOperationError):
        raise InvalidOperationError("Invalid operation")