# app/calculator_repl.py
"""Module for the Read-Eval-Print Loop (REPL) interface."""
import os
import logging
from app.calculation import Calculator
from app.history import HistoryManager
from app.calculator_memento import Caretaker
from app.calculator_config import Config
from app.input_validators import validate_input
from app.exceptions import InvalidOperationError
from app.logger import setup_logger
from app.observers import Subject, Observer, LoggingObserver, AutoSaveObserver
from app.commands import register_command, COMMANDS

class CalculatorREPL(Subject):
    """The main class for the calculator's REPL."""
    def __init__(self):
        self._observers = [] # For Observer Pattern
        Config.load_config()
        setup_logger() # Set up logging on start

        # --- Use new Config for directory-based history ---
        history_dir = Config.get_history_dir()
        if not os.path.exists(history_dir):
             os.makedirs(history_dir) # pragma: no cover
        history_filename = os.getenv('HISTORY_FILEPATH', 'calculation_history.csv')
        history_filepath = os.path.join(history_dir, history_filename)
        # --- End of new logic ---

        self.history_manager = HistoryManager(history_filepath)
        self.caretaker = Caretaker(self.history_manager) # For Memento Pattern
        # --- Attach Observers ---
        self.attach(LoggingObserver())
        self.attach(AutoSaveObserver(self.history_manager))

    # --- Subject Methods (Observer Pattern) ---
    def attach(self, observer: Observer):
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Detach an observer from the subject."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass # pragma: no cover

    def notify(self, *args, **kwargs):
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

    # --- Command Methods (Decorator Pattern) ---
    @register_command("quit", "Exits the application.")
    @register_command("exit", "Exits the application.")
    def _exit(self, *args):
        """Exits the application."""
        print("Exiting calculator. Goodbye!")
        return False  # Signal to stop the loop

    @register_command("help", "Displays this help message.")
    def _help(self, *args):
        """Displays help information dynamically."""
        print("\nAvailable Commands:")
        print("  <num1> <op> <num2> - Perform a calculation (e.g., 5 + 3).")
        print("  Operators: +, -, *, /, ^, sqrt, %, //, perc, abs")
        # Loop through the registered commands
        for name, info in sorted(COMMANDS.items()):
            print(f"  {name:<15} - {info['description']}")
        print()
        return True

    @register_command("history", "Show calculation history.")
    def _history(self, *args):
        """Displays the calculation history."""
        history_df = self.history_manager.get_history()
        if history_df.empty:
            print("History is empty.")
        else:
            print("\n--- Calculation History ---")
            print(history_df.to_string())
            print("---------------------------\n")
        return True

    @register_command("clear", "Clear calculation history.")
    def _clear_history(self, *args):
        """Clears the history."""
        self.caretaker.backup() # Save state before clearing for undo
        self.history_manager.clear()
        self.history_manager.save() # Manually save after clear
        print("History cleared.")
        return True

    @register_command("save", "Manually save history to CSV.")
    def _save_history(self, *args):
        """Manually saves the history."""
        self.history_manager.save()
        print(f"History saved to {self.history_manager.filepath}.")
        return True

    @register_command("load", "Manually load history from CSV.")
    def _load_history(self, *args):
        """Manually loads the history."""
        self.caretaker.backup() # Save state before loading for undo
        self.history_manager.load()
        print(f"History loaded from {self.history_manager.filepath}.")
        return True

    @register_command("undo", "Undo the last change to history.")
    def _undo(self, *args):
        """Undoes the last action."""
        self.caretaker.undo()
        return True

    @register_command("redo", "Redo the last undone change.")
    def _redo(self, *args):
        """Redoes the last undone action."""
        self.caretaker.redo()
        return True

    def _perform_calculation(self, command: str, args: list):
        """Handles the calculation logic."""
        try:
            # Standard two-operand calculation, e.g., 5 + 3
            if len(args) == 2:
                operands = [command, args[1]]
                op_name = args[0]
            # Single-operand calculation, e.g., sqrt 16
            elif len(args) == 1 and command in ['sqrt', 'root']:
                operands = args
                op_name = command
            else:
                raise ValueError("Invalid calculation format. Use <num1> <op> <num2> or sqrt <num>")

            self.caretaker.backup() # Save history state before calculation

            # Use the Calculator facade
            result = Calculator.calculate(operands, op_name)

            # Add to history
            self.history_manager.add_record(op_name, tuple(operands), result)

            # Notify observers (for logging and auto-save)
            self.notify(operation=op_name, operands=tuple(operands), result=result)

            print(f"Result: {result}")

        except (ValueError, ZeroDivisionError, InvalidOperationError, IndexError) as e:
            print(f"Error: {e}")
            logging.warning(f"Calculation error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logging.error(f"Unexpected error: {e}", exc_info=True)


    def run(self):
        """Starts the REPL loop."""
        print("Welcome to the Enhanced Calculator!")
        self._help()
        while True:
            try:
                user_input = input(">>> ").strip()
                if not user_input:
                    continue # pragma: no cover

                command, args = validate_input(user_input)

                if command in COMMANDS:
                    # Call command from the decorator registry
                    if not COMMANDS[command]['function'](self, *args):
                        break # Exit loop if command returns False
                else:
                    # If not a known command, assume it's a calculation
                    self._perform_calculation(command, args)

            except (ValueError, InvalidOperationError) as e:
                print(f"Input Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                logging.error(f"REPL loop error: {e}", exc_info=True)

if __name__ == "__main__": # pragma: no cover
    CalculatorREPL().run()