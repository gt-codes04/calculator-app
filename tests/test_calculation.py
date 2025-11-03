# tests/test_calculation.py
"""Unit tests for the Calculator facade."""
import pytest
from decimal import Decimal
from app.calculation import Calculator
from app.exceptions import InvalidOperationError # Make sure you have this import

@pytest.mark.parametrize("operands, op_name, expected_str", [
    (['10', '5'], 'add', '15'),
    (['10', '5'], 'subtract', '5'),
    (['10', '5'], 'multiply', '50'),
    (['10', '2'], 'divide', '5'),
    (['2', '3'], 'power', '8'),
    (['25'], 'sqrt', '5'),
    (['27', '3'], 'root', '3'),
    (['10', '3'], 'modulus', '1'),
    (['10', '3'], 'int_divide', '3'),
    (['50', '100'], 'percent', '50'),
    (['10', '15'], 'abs_diff', '5'),
])
def test_calculate_all_operations(operands, op_name, expected_str):
    """Test the main calculate method with all operations."""
    result = Calculator.calculate(operands, op_name)
    assert result == Decimal(expected_str)

def test_calculate_invalid_operation():
    """Test calculation with an invalid operation name."""
    with pytest.raises(InvalidOperationError, match="Unknown operation: foo"):
        Calculator.calculate(['10', '5'], 'foo')

def test_calculate_division_by_zero():
    """Test that calculate handles division by zero."""
    with pytest.raises(ZeroDivisionError):
        Calculator.calculate(['10', '0'], 'divide')

def test_calculate_invalid_number():
    """Test that calculate handles invalid number strings."""
    with pytest.raises(ValueError, match="Invalid number in operands"):
        Calculator.calculate(['10', 'five'], 'add')