"""Module for validating user input."""
from typing import List, Tuple

def validate_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Validates and parses the user's command-line input.
    
    Returns:
        A tuple containing the command and a list of arguments.
    Raises:
        ValueError: If the input is empty or invalid.
    """
    if not user_input:
        raise ValueError("Input cannot be empty.")
        
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    
    return command, args