"""Unit tests for the Memento and Caretaker classes."""
import pandas as pd
from app.history import HistoryManager
from app.calculator_memento import Caretaker, Memento

def test_memento():
    """Test that the memento correctly stores state."""
    df = pd.DataFrame({'A': [1]})
    memento = Memento(df)
    assert memento.get_state().equals(df)

def test_caretaker_undo_redo():
    """Test the full undo and redo functionality of the Caretaker."""
    manager = HistoryManager('dummy.csv')
    caretaker = Caretaker(manager)

    # State 1
    caretaker.backup() # Backup initial empty state
    manager.add_record('add', (1, 1), 2)
    
    # State 2
    caretaker.backup() # Backup state with one record
    manager.add_record('add', (2, 2), 4)

    # Current state has 2 records
    assert len(manager.get_history()) == 2
    
    # Undo to State 2
    caretaker.undo()
    assert len(manager.get_history()) == 1
    assert manager.get_history().iloc[0]['Result'] == 2

    # Undo to State 1
    caretaker.undo()
    assert manager.get_history().empty

    # Redo to State 2
    caretaker.redo()
    assert len(manager.get_history()) == 1
    
    # Redo to current state
    caretaker.redo()
    assert len(manager.get_history()) == 2

def test_undo_redo_empty_stack(capsys):
    """Test that undo/redo commands print messages when stacks are empty."""
    manager = HistoryManager('dummy.csv')
    caretaker = Caretaker(manager)
    
    caretaker.undo()
    captured = capsys.readouterr()
    assert "Nothing to undo." in captured.out
    
    caretaker.redo()
    captured = capsys.readouterr()
    assert "Nothing to redo." in captured.out