import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pytest
from csvimport import parse_format, remove_duplicates

# Sample test for parse_format

def test_parse_format_comma():
    result = parse_format("A,B,C")
    assert result == ["A", "B", "C"]

def test_parse_format_yaml():
    result = parse_format("[A, B, C]")
    assert result == ["A", "B", "C"]

# Sample test for remove_duplicates

def test_remove_duplicates_basic():
    rows = [
        {"A": "1", "B": "x"},
        {"A": "2", "B": "y"},
        {"A": "1", "B": "x"},
    ]
    existing = [{"A": "1", "B": "x"}]
    key_columns = ["A", "B"]
    class DummyLogger:
        def debug(self, msg): pass
        def info(self, msg): pass
    deduped = remove_duplicates(rows, existing, key_columns, DummyLogger())
    assert deduped == [{"A": "2", "B": "y"}]
