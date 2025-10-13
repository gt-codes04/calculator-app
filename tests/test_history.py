"""Unit tests for the HistoryManager."""
import os
import pandas as pd
import pytest
from app.history import HistoryManager
from app.calculator_memento import Memento

@pytest.fixture
def history_manager(tmpdir):
    """Fixture to create a HistoryManager with a temporary file path."""
    filepath = tmpdir.join("test_history.csv")
    return HistoryManager(filepath=str(filepath))

def test_add_record(history_manager):
    """Test adding a single record to the history."""
    assert history_manager.get_history().empty
    history_manager.add_record('add', (5, 3), 8)
    df = history_manager.get_history()
    assert len(df) == 1
    assert df.iloc[0]['Operation'] == 'add'
    assert df.iloc[0]['Result'] == 8

def test_save_and_load(history_manager):
    """Test saving history to a file and loading it back."""
    history_manager.add_record('multiply', (4, 5), 20)
    history_manager.save()
    assert os.path.exists(history_manager.filepath)
    
    # Create a new manager to load from the same file
    new_manager = HistoryManager(filepath=history_manager.filepath)
    df = new_manager.get_history()
    assert len(df) == 1
    assert df.iloc[0]['Operation'] == 'multiply'

def test_clear(history_manager):
    """Test clearing the history."""
    history_manager.add_record('subtract', (10, 4), 6)
    assert not history_manager.get_history().empty
    history_manager.clear()
    assert history_manager.get_history().empty

def test_memento_save_restore(history_manager):
    """Test saving to and restoring from a memento."""
    history_manager.add_record('add', (1, 1), 2)
    memento = history_manager.save_to_memento()
    
    history_manager.add_record('add', (2, 2), 4)
    assert len(history_manager.get_history()) == 2
    
    history_manager.restore_from_memento(memento)
    assert len(history_manager.get_history()) == 1
    assert history_manager.get_history().iloc[0]['Result'] == 2

def test_load_nonexistent_file(tmpdir):
    """Test that loading a non-existent file creates an empty DataFrame."""
    filepath = tmpdir.join("nonexistent.csv")
    manager = HistoryManager(filepath=str(filepath))
    assert manager.get_history().empty
    assert list(manager.get_history().columns) == ['Operation', 'Operands', 'Result']