# tests/test_operations.py
"""Unit tests for the operations module."""
import pytest
from app.operations import OperationFactory, Root
from app.exceptions import InvalidOperationError

def test_operation_factory():
    """Test the OperationFactory for creating correct operation objects."""
    assert isinstance(OperationFactory.create_operation('+'), object)
    assert isinstance(OperationFactory.create_operation('subtract'), object)
    assert isinstance(OperationFactory.create_operation('^'), object)

def test_operation_factory_invalid():
    """Test that OperationFactory raises an error for unknown operations."""
    with pytest.raises(InvalidOperationError, match="Unknown operation: bogus"):
        OperationFactory.create_operation('bogus')

@pytest.mark.parametrize("op_symbol, a, b, expected", [
    ('add', 5, 3, 8),
    ('+', 5, 3, 8),
    ('subtract', 10, 4, 6),
    ('-', 10, 4, 6),
    ('multiply', 5, 5, 25),
    ('*', 5, 5, 25),
    ('divide', 10, 2, 5),
    ('/', 10, 2, 5),
    ('power', 2, 3, 8),
    ('^', 2, 3, 8),
])
def test_two_operand_operations(op_symbol, a, b, expected):
    """Test standard two-operand operations."""
    operation = OperationFactory.create_operation(op_symbol)
    assert operation.execute(a, b) == expected

def test_division_by_zero():
    """Test that division by zero raises a ZeroDivisionError."""
    div_op = OperationFactory.create_operation('divide')
    with pytest.raises(ZeroDivisionError):
        div_op.execute(10, 0)

@pytest.mark.parametrize("op_symbol, args, expected", [
    ('root', [16], 4),
    ('sqrt', [16], 4),
    ('root', [27, 3], 3),
])
def test_root_operation(op_symbol, args, expected):
    """Test the root operation with one or two operands."""
    operation = OperationFactory.create_operation(op_symbol)
    assert operation.execute(*args) == expected

def test_root_negative_input():
    """Test root operation with invalid negative inputs."""
    root_op = Root()
    with pytest.raises(ValueError, match="Cannot calculate the square root of a negative number."):
        root_op.execute(-4)
    with pytest.raises(ValueError, match="Cannot calculate an even root of a negative number."):
        root_op.execute(-8, 2)

@pytest.mark.parametrize("op_symbol, args", [
    ('add', [1]),
    ('subtract', [1, 2, 3]),
    ('multiply', []),
    ('divide', [5]),
    ('power', [2]),
    ('root', []),
])
def test_invalid_operand_count(op_symbol, args):
    """Test that operations raise errors with incorrect number of operands."""
    operation = OperationFactory.create_operation(op_symbol)
    with pytest.raises(ValueError):
        operation.execute(*args)

# --- New Tests for Midterm ---

@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 1),
    (10, 2, 0),
])
def test_modulus_operation(a, b, expected):
    operation = OperationFactory.create_operation('modulus')
    assert operation.execute(a, b) == expected

def test_modulus_by_zero():
    operation = OperationFactory.create_operation('modulus')
    with pytest.raises(ZeroDivisionError):
        operation.execute(10, 0)

@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 3),
    (7, 2, 3),
])
def test_integer_division_operation(a, b, expected):
    operation = OperationFactory.create_operation('int_divide')
    assert operation.execute(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (50, 100, 50.0),
    (20, 80, 25.0),
])
def test_percentage_operation(a, b, expected):
    operation = OperationFactory.create_operation('percent')
    assert operation.execute(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 15, 5),
    (15, 10, 5),
    (-10, 5, 15),
])
def test_abs_diff_operation(a, b, expected):
    operation = OperationFactory.create_operation('abs_diff')
    assert operation.execute(a, b) == expected