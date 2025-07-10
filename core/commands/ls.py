import os
from pathlib import Path
from colorama import Fore, Style

def command(args=None, context=None):
    """Выводит содержимое директории с цветовой подсветкой
    
    Использование:
        ls          - список файлов в текущей директории
        ls <path>   - список файлов по указанному пути
        ls -l       - подробный вывод
    """
    # Парсинг аргументов
    long_format = False
    target_dir = os.getcwd()

    if args:
        if '-l' in args:
            long_format = True
            args.remove('-l')
        if args:
            target_dir = args[0]

    try:
        path = Path(target_dir)
        if not path.exists():
            print(f"{Fore.RED}E: Directory is not existing{Style.RESET_ALL}")
            return

        items = sorted(os.listdir(path))
        if not items:
            print(f"{Fore.YELLOW}Directory is empty{Style.RESET_ALL}")
            return

        for item in items:
            item_path = path / item
            if item_path.is_dir():
                print(f"{Fore.BLUE}{item}/{Style.RESET_ALL}", end='')
            elif os.access(item_path, os.X_OK):
                print(f"{Fore.GREEN}{item}{Style.RESET_ALL}", end='')
            else:
                print(item, end='')

            if long_format:
                stat = item_path.stat()
                print(f"  {stat.st_size:8} bytes  {stat.st_mtime:.0f}", end='')
            print()

    except Exception as e:
        print(f"{Fore.RED}E: {str(e)}{Style.RESET_ALL}")