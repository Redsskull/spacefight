import sys
import os


def test_paths():
    """Debug test to print path information"""
    print("\nPython executable:", sys.executable)
    print("\nsys.path:", sys.path)
    print("\nCWD:", os.getcwd())
