# app/calculation.py
from app.operations import OperationFactory

class Calculator:
    @staticmethod
    def calculate(a, b, op_char):
        """Static method to perform calculation."""
        operation = OperationFactory.create_operation(op_char)
        return operation.execute(a, b)