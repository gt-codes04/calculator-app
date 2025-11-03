# app/observers.py
from abc import ABC, abstractmethod
import logging
# We need to import HistoryManager from app.history
from app.history import HistoryManager 

class Subject(ABC):
    """The Subject interface."""
    @abstractmethod
    def attach(self, observer):
        pass # pragma: no cover

    @abstractmethod
    def detach(self, observer):
        pass # pragma: no cover

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass # pragma: no cover

class Observer(ABC):
    """The Observer interface."""
    @abstractmethod
    def update(self, subject, *args, **kwargs):
        pass # pragma: no cover

# --- Concrete Observers ---

class LoggingObserver(Observer):
    """Logs calculations."""
    def update(self, subject, *args, **kwargs):
        operation = kwargs.get('operation')
        operands = kwargs.get('operands')
        result = kwargs.get('result')
        if operation:
            logging.info(f"Calculation: {operation} with {operands}. Result: {result}")

class AutoSaveObserver(Observer):
    """Saves history after each calculation."""
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager

    def update(self, subject, *args, **kwargs):
        # Only save if a calculation was performed
        if kwargs.get('operation'):
            self.history_manager.save()
            logging.info("History auto-saved.")