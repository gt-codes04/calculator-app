# tests/test_calculator_config.py
"""Unit tests for the Config class."""
import os
from unittest.mock import patch
from app.calculator_config import Config

def test_load_config():
    """Test that load_config runs without errors."""
    Config.load_config()
    assert True # Simple check that it runs

@patch.dict(os.environ, {'CALCULATOR_LOG_DIR': 'custom_logs'})
def test_get_log_dir_set():
    assert Config.get_log_dir() == 'custom_logs'

@patch.dict(os.environ, {}, clear=True)
def test_get_log_dir_default():
    assert Config.get_log_dir() == 'logs'

@patch.dict(os.environ, {'CALCULATOR_HISTORY_DIR': 'custom_history'})
def test_get_history_dir_set():
    assert Config.get_history_dir() == 'custom_history'

@patch.dict(os.environ, {}, clear=True)
def test_get_history_dir_default():
    assert Config.get_history_dir() == 'history'

@patch.dict(os.environ, {'CALCULATOR_MAX_HISTORY_SIZE': '50'})
def test_get_max_history_size_set():
    assert Config.get_max_history_size() == 50

@patch.dict(os.environ, {}, clear=True)
def test_get_max_history_size_default():
    assert Config.get_max_history_size() == 100

@patch.dict(os.environ, {'CALCULATOR_PRECISION': '2'})
def test_get_precision_set():
    assert Config.get_precision() == 2

@patch.dict(os.environ, {'CALCULATOR_MAX_INPUT_VALUE': '5000'})
def test_get_max_input_value_set():
    assert Config.get_max_input_value() == 5000

@patch.dict(os.environ, {'CALCULATOR_DEFAULT_ENCODING': 'latin-1'})
def test_get_default_encoding_set():
    assert Config.get_default_encoding() == 'latin-1'