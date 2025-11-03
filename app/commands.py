# app/commands.py
COMMANDS = {}

def register_command(name, description):
    """Decorator to register a command for the REPL."""
    def decorator(func):
        # Store the function and its description
        COMMANDS[name] = {'function': func, 'description': description}
        # Return the original function
        return func
    return decorator