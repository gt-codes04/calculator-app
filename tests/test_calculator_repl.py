"""Unit tests for the CalculatorREPL class."""
from unittest.mock import patch, MagicMock
import pytest
from app.calculator_repl import CalculatorREPL

@pytest.fixture
def repl():
    """Fixture to create a CalculatorREPL instance for testing."""
    return CalculatorREPL()

@pytest.mark.parametrize("command", ["exit", "quit"])
def test_exit_command(repl, command):
    """Test that 'exit' and 'quit' commands stop the REPL."""
    with patch('builtins.input', side_effect=[command]):
        with patch.object(repl, '_exit', return_value=False) as mock_exit:
            repl.run()
            mock_exit.assert_called_once()

def test_help_command(repl, capsys):
    """Test the 'help' command."""
    repl._help()
    captured = capsys.readouterr()
    assert "Available Commands" in captured.out

def test_history_command_empty(repl, capsys):
    """Test the 'history' command when history is empty."""
    repl._history()
    captured = capsys.readouterr()
    assert "History is empty." in captured.out

def test_history_command_with_data(repl, capsys):
    """Test the 'history' command with data."""
    repl.history_manager.add_record('add', (1,1), 2)
    repl._history()
    captured = capsys.readouterr()
    assert "Calculation History" in captured.out
    assert "add" in captured.out

def test_clear_history_command(repl, capsys):
    """Test the 'clear' command."""
    repl.history_manager.add_record('add', (1,1), 2)
    assert not repl.history_manager.get_history().empty
    repl._clear_history()
    assert repl.history_manager.get_history().empty
    captured = capsys.readouterr()
    assert "History cleared." in captured.out

def test_save_and_load_commands(repl, capsys):
    """Test the 'save' and 'load' commands."""
    repl._save_history()
    captured = capsys.readouterr()
    assert "History saved to" in captured.out

    repl._load_history()
    captured = capsys.readouterr()
    assert "History loaded from" in captured.out

def test_undo_redo_commands(repl):
    """Test the 'undo' and 'redo' commands by patching the Caretaker."""
    with patch.object(repl.caretaker, 'undo') as mock_undo:
        repl._undo()
        mock_undo.assert_called_once()
    
    with patch.object(repl.caretaker, 'redo') as mock_redo:
        repl._redo()
        mock_redo.assert_called_once()

def test_perform_calculation(repl, capsys):
    """Test a valid calculation."""
    repl._perform_calculation('5', ['+', '3'])
    captured = capsys.readouterr()
    assert "Result: 8" in captured.out
    assert len(repl.history_manager.get_history()) == 1

def test_perform_calculation_invalid_format(repl):
    """Test calculation with invalid format."""
    with pytest.raises(ValueError, match="Invalid calculation format."):
        repl._perform_calculation('5', ['+'])

def test_run_loop_handles_errors(repl, capsys):
    """Test that the main run loop handles errors gracefully."""
    with patch('builtins.input', side_effect=['5 / 0', 'exit']):
        repl.run()
        captured = capsys.readouterr()
        assert "Error: Cannot divide by zero." in captured.out

def test_run_loop_unexpected_error(repl, capsys):
    """Test that the run loop handles unexpected errors."""
    with patch('app.input_validators.validate_input', side_effect=Exception("Unexpected")):
        with patch('builtins.input', side_effect=['some input', 'exit']):
            repl.run()
            captured = capsys.readouterr()
            assert "An unexpected error occurred: Unexpected" in captured.out