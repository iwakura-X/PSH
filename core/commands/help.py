import os
from pathlib import Path

def command(args=None, context=None):
    """Показывает список доступных команд и их описание
    
    Использование:
        help - показать все команды
        help <command> - показать справку по конкретной команде
    """
    help_text = """
+=== PSH Help ===+
| Base cmds:
| help    - showing this
| ls      - list of files in a dir
| cd      - change dir
| cls     - clear screen
| exit    - logout
|
| File ops:
| mkdir   - create dir
| rmdir   - delete dir
| aleph   - create or edit a file
| rm      - delete file
|
| System:
| sysinfo - system info
|
| Misc:
| ascii - showing ASCII logo
+=================+
"""
    print(help_text)