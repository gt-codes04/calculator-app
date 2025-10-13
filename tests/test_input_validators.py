"""Unit tests for the input_validators module."""
import pytest
from app.input_validators import validate_input

@pytest.mark.parametrize("user_input, expected_command, expected_args", [
    ("add 5 3", "add", ["5", "3"]),
    ("history", "history", []),
    ("  exit  ", "exit", []),
])
def test_validate_input_valid(user_input, expected_command, expected_args):
    """Test valid user inputs."""
    command, args = validate_input(user_input)
    assert command == expected_command
    assert args == expected_args

def test_validate_input_empty():
    """Test that empty input raises a ValueError."""
    with pytest.raises(ValueError, match="Input cannot be empty."):
        validate_input("")