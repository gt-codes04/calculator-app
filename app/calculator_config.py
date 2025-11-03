# app/calculator_config.py
"""Module for managing application configuration from environment variables."""
import os
from dotenv import load_dotenv

class Config:
    """Loads and provides access to configuration settings."""

    @staticmethod
    def load_config():
        """Loads environment variables from a .env file."""
        load_dotenv()

    @staticmethod
    def get_log_dir() -> str:
        """Gets the log directory path from .env, with a default."""
        return os.getenv('CALCULATOR_LOG_DIR', 'logs')

    @staticmethod
    def get_history_dir() -> str:
        """Gets the history directory path from .env, with a default."""
        return os.getenv('CALCULATOR_HISTORY_DIR', 'history')

    @staticmethod
    def get_max_history_size() -> int:
        """Gets the max history size from .env, with a default."""
        return int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', 100))

    @staticmethod
    def get_precision() -> int:
        """Gets the calculation precision from .env, with a default."""
        return int(os.getenv('CALCULATOR_PRECISION', 4))

    @staticmethod
    def get_max_input_value() -> int:
        """Gets the max input value from .env, with a default."""
        return int(os.getenv('CALCULATOR_MAX_INPUT_VALUE', 1000000))

    @staticmethod
    def get_default_encoding() -> str:
        """Gets the default file encoding from .env, with a default."""
        return os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')