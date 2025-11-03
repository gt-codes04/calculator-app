# app/calculation.py
"""Module for the Calculator Facade."""
from decimal import Decimal
from typing import List
from app.operations import OperationFactory
from app.exceptions import InvalidOperationError # Make sure you have this import

class Calculator:
    """Provides a simplified interface to the calculation subsystem (Facade Pattern)."""
    @staticmethod
    def _convert_operands(operands: List[str]) -> List[Decimal]:
        """Converts a list of string operands to a list of Decimals."""
        # Use list comprehension for efficient conversion
        try:
            return [Decimal(op) for op in operands]
        except Exception:
            raise ValueError(f"Invalid number in operands: {operands}")

    @staticmethod
    def calculate(operands: List[str], operation_name: str) -> Decimal:
        """
        Performs a calculation.

        Args:
            operands (List[str]): A list of numbers as strings. (e.g., ['10', '5'])
            operation_name (str): The name or symbol of the operation. (e.g., 'add')

        Returns:
            Decimal: The result of the calculation.
        """
        # Use the factory to get the correct operation object
        operation = OperationFactory.create_operation(operation_name)
        
        # Convert string operands to Decimal
        decimal_operands = Calculator._convert_operands(operands)
        
        # Use the * (splat) operator to pass operands as individual arguments
        result = operation.execute(*decimal_operands)
        return Decimal(result)