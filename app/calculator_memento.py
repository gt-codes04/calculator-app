"""Module for the Memento Pattern to enable undo/redo functionality."""
import pandas as pd

class Memento:
    """Stores the state of the HistoryManager's DataFrame."""
    def __init__(self, state: pd.DataFrame):
        self._state = state

    def get_state(self) -> pd.DataFrame:
        """Returns the stored state."""
        return self._state

class Caretaker:
    """Manages the undo and redo stacks of mementos."""
    def __init__(self, originator):
        self._originator = originator
        self._undo_stack: list[Memento] = []
        self._redo_stack: list[Memento] = []

    def backup(self):
        """Saves the current state of the originator for a future undo."""
        self._undo_stack.append(self._originator.save_to_memento())
        self._redo_stack.clear()

    def undo(self):
        """Restores the originator to its previous state."""
        if not self._undo_stack:
            print("Nothing to undo.")
            return
        
        # Move the current state to the redo stack before restoring
        self._redo_stack.append(self._originator.save_to_memento())
        
        # Restore the previous state from the undo stack
        memento = self._undo_stack.pop()
        self._originator.restore_from_memento(memento)
        print("Undo successful.")

    def redo(self):
        """Restores the originator to a previously undone state."""
        if not self._redo_stack:
            print("Nothing to redo.")
            return

        # Move the restored state back to the undo stack
        self._undo_stack.append(self._originator.save_to_memento())

        # Restore the state from the redo stack
        memento = self._redo_stack.pop()
        self._originator.restore_from_memento(memento)
        print("Redo successful.")