import os
from pathlib import Path

def command(args=None, context=None):
    """Очищает консоль в Windows/Linux/MacOS"""
    os.system('cls' if os.name == 'nt' else 'clear')