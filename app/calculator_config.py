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
    def get_history_filepath() -> str:
        """
        Retrieves the history file path from environment variables.
        Defaults to 'calculation_history.csv' if not set.
        """
        filepath = os.getenv('HISTORY_FILEPATH')
        if not filepath:
            print("Warning: HISTORY_FILEPATH not set. Using default 'calculation_history.csv'.")
            return 'calculation_history.csv'
        return filepath