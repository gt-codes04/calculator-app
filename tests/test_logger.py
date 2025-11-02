# tests/test_logger.py
import logging
import os
from app.logger import setup_logger
from app.calculator_config import Config
from unittest.mock import patch

@patch('os.makedirs')
@patch('logging.FileHandler')
def test_setup_logger(mock_file_handler, mock_makedirs):
    """Test that the logger setup runs."""
    # Ensure the logger is clear of handlers before test
    logging.getLogger().handlers.clear()

    setup_logger()

    # Check that it tried to create a FileHandler
    log_dir = Config.get_log_dir()
    log_file_path = os.path.join(log_dir, 'calculator.log')
    mock_file_handler.assert_called_with(log_file_path)

    # Check that it logs the config message
    assert logging.getLogger().level == logging.INFO

    # Clear handlers again after test
    logging.getLogger().handlers.clear()