# app/calculator_repl.py

from app.calculation import Calculator
from app.history import HistoryManager

class CalculatorREPL:
    def __init__(self):
        self.history_manager = HistoryManager()
        self._running = True

    def run(self):
        print("Welcome to the Enhanced Calculator!")
        print("Type 'help' for commands. Enter 'exit' to quit.")
        while self._running:
            try:
                user_input = input(">>> ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    self._exit()
                    continue
                if user_input.lower() == 'help':
                    self._help()
                    continue
                if user_input.lower() == 'history':
                    self._history()
                    continue
                if user_input.lower() == 'clear':
                    self.history_manager.clear()
                    print("History cleared.")
                    continue

                parts = user_input.split()
                if len(parts) != 3:
                    print("Invalid input format. Please use: <num1> <operator> <num2>")
                    continue

                a, op, b = parts
                result = Calculator.calculate(float(a), float(b), op)
                self.history_manager.add_record(op, (a, b), result)
                print(f"Result: {result}")

            except ValueError as ve:
                print(f"Error: {ve}")
            except ZeroDivisionError as zde:
                print(f"Error: {zde}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def _exit(self):
        self._running = False

    def _help(self):
        print("""Available Commands:
  <num1> <operator> <num2> : Perform calculation
  history                  : Show calculation history
  clear                    : Clear calculation history
  help                     : Show this help message
  exit/quit                : Exit the calculator
""")

    def _history(self):
        if self.history_manager.history_df.empty:
            print("History is empty.")
        else:
            print("Calculation History:")
            print(self.history_manager.history_df)

if __name__ == "__main__":
    repl = CalculatorREPL()
    repl.run() # pragma: no cover