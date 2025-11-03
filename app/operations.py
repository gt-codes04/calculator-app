# app/operations.py
"""Module defining arithmetic operations using the Strategy and Factory patterns."""
from abc import ABC, abstractmethod
import math
from app.exceptions import InvalidOperationError

class Operation(ABC):
    """Abstract base class for all operations (Strategy interface)."""
    @abstractmethod
    def execute(self, *args):
        """Execute the operation with given arguments."""
        pass # pragma: no cover

# --- Existing Operations (Standardized) ---

class Addition(Operation):
    """Adds two numbers."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Addition requires two operands.")
        return args[0] + args[1]

class Subtraction(Operation):
    """Subtracts the second number from the first."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Subtraction requires two operands.")
        return args[0] - args[1]

class Multiplication(Operation):
    """Multiplies two numbers."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Multiplication requires two operands.")
        return args[0] * args[1]

class Division(Operation):
    """Divides the first number by the second."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Division requires two operands.")
        if args[1] == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return args[0] / args[1]

class Power(Operation):
    """Raises the first number to the power of the second."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Power requires two operands.")
        return math.pow(args[0], args[1])

class Root(Operation):
    """Calculates the nth root of a number. Defaults to square root."""
    def execute(self, *args):
        if len(args) == 1:
            if args[0] < 0:
                raise ValueError("Cannot calculate the square root of a negative number.")
            return math.sqrt(args[0])
        if len(args) == 2:
            if args[0] < 0 and args[1] % 2 == 0:
                raise ValueError("Cannot calculate an even root of a negative number.")
            return args[0] ** (1 / args[1])
        raise ValueError("Root requires one or two operands.")

# --- New Midterm Operations ---

class Modulus(Operation):
    """Calculates the remainder of a division."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Modulus requires two operands.")
        if args[1] == 0:
            raise ZeroDivisionError("Cannot perform modulus by zero.")
        return args[0] % args[1]

class IntegerDivision(Operation):
    """Performs division that results in an integer quotient."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Integer Division requires two operands.")
        if args[1] == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return args[0] // args[1]

class Percentage(Operation):
    """Calculates the percentage of one number with respect to another."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Percentage requires two operands.")
        if args[1] == 0:
            raise ZeroDivisionError("Cannot calculate percentage with zero as the denominator.")
        return (args[0] / args[1]) * 100

class AbsoluteDifference(Operation):
    """Calculates the absolute difference between two numbers."""
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Absolute Difference requires two operands.")
        return abs(args[0] - args[1])

# --- Factory ---

class OperationFactory:
    """Factory to create operation objects."""
    @staticmethod
    def create_operation(op_name: str) -> Operation:
        """Creates and returns the appropriate operation object."""
        operations = {
            "add": Addition,
            "subtract": Subtraction,
            "multiply": Multiplication,
            "divide": Division,
            "power": Power,
            "root": Root,
            "modulus": Modulus,           # <-- NEW
            "int_divide": IntegerDivision,  # <-- NEW
            "percent": Percentage,        # <-- NEW
            "abs_diff": AbsoluteDifference  # <-- NEW
        }
        # A mapping for common symbols to command names
        symbol_map = {
            '+': 'add',
            '-': 'subtract',
            '*': 'multiply',
            '/': 'divide',
            '^': 'power',
            '**': 'power',
            'sqrt': 'root',
            '%': 'modulus',             # <-- NEW
            '//': 'int_divide',         # <-- NEW
            'perc': 'percent',          # <-- NEW
            'abs': 'abs_diff'           # <-- NEW
        }

        # Normalize input to lowercase command name
        command = symbol_map.get(op_name.lower(), op_name.lower())

        operation_class = operations.get(command)
        if not operation_class:
            raise InvalidOperationError(f"Unknown operation: {op_name}")
        return operation_class()