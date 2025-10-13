# app/operations.py
from abc import ABC, abstractmethod
import math

class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class Addition(Operation):
    def execute(self, a, b):
        return a + b

class Subtraction(Operation):
    def execute(self, a, b):
        return a - b

class Multiplication(Operation):
    def execute(self, a, b):
        return a * b

class Power(Operation):
    def execute(self, a, b):
        return a ** b

class Root(Operation):
    def execute(self, a, b=None):
        # If b is None, compute sqrt(a), else compute a ** (1/b)
        if b is None:
            return math.sqrt(a)
        return a ** (1 / b)

class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b
    # app/operations.py (continued)
class OperationFactory:
    @staticmethod
    def create_operation(op_char):
        operations = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division(),
            '^': Power(), # or '**'
            'sqrt': Root()
        }
        if op_char not in operations:
            raise ValueError(f"Unknown operation: {op_char}")
        return operations[op_char]