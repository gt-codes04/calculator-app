# app/history.py

"""Module for managing calculation history with pandas."""
import os
import pandas as pd
from app.calculator_memento import Memento

class HistoryManager:
    """Manages the history of calculations (Originator for Memento Pattern)."""
    def __init__(self, filepath: str = 'calculation_history.csv'):
        self.filepath = filepath
        self.history_df = self._load_or_initialize()

    def _load_or_initialize(self) -> pd.DataFrame:
        """Loads history from CSV or creates a new DataFrame."""
        if os.path.exists(self.filepath):
            return pd.read_csv(self.filepath)
        return pd.DataFrame(columns=['Operation', 'Operands', 'Result'])

    def add_record(self, operation: str, operands: tuple, result: float):
        """Adds a new calculation record to the history."""
        new_record = pd.DataFrame([{
            'Operation': operation,
            'Operands': str(operands),
            'Result': result
        }])
        self.history_df = pd.concat([self.history_df, new_record], ignore_index=True)

    def save(self):
        """Saves the history DataFrame to a CSV file."""
        self.history_df.to_csv(self.filepath, index=False)

    def load(self):
        """Forces a reload of history from the file."""
        self.history_df = self._load_or_initialize()

    def clear(self):
        """Clears all records from the history DataFrame."""
        self.history_df = pd.DataFrame(columns=['Operation', 'Operands', 'Result'])

    def get_history(self) -> pd.DataFrame:
        """Returns the current history DataFrame."""
        return self.history_df

    # Memento Pattern Methods
    def save_to_memento(self) -> Memento:
        """Saves the current state to a Memento."""
        return Memento(self.history_df.copy(deep=True))

    def restore_from_memento(self, memento: Memento):
        """Restores the state from a Memento."""
        self.history_df = memento.get_state()