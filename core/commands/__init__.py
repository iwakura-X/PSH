import os
import importlib
from pathlib import Path
import sys

def load_commands():
    """Динамически загружает команды из папки commands"""
    commands = {}
    commands_dir = Path(__file__).parent
    
    # Добавляем директорию core в PYTHONPATH
    core_dir = commands_dir.parent
    if str(core_dir) not in sys.path:
        sys.path.insert(0, str(core_dir))
    
    for file in commands_dir.glob("*.py"):
        if file.name.startswith("_") or file.name == "__init__.py":
            continue
        
        module_name = f"core.commands.{file.stem}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "command"):
                commands[file.stem] = module.command
        except Exception as e:
            print(f"⚠️ Failed to load command {file.stem}: {str(e)}")
            continue
            
    return commands
load_commands()