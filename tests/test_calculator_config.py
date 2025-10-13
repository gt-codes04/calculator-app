"""Unit tests for the Config class."""
import os
from unittest.mock import patch
from app.calculator_config import Config

def test_get_history_filepath_from_env():
    """Test retrieving the filepath when the environment variable is set."""
    test_path = "test_path.csv"
    with patch.dict(os.environ, {'HISTORY_FILEPATH': test_path}):
        assert Config.get_history_filepath() == test_path

def test_get_history_filepath_default(capsys):
    """Test that a default filepath is returned when the env var is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert Config.get_history_filepath() == 'calculation_history.csv'
        captured = capsys.readouterr()
        assert "Warning: HISTORY_FILEPATH not set." in captured.out