import os
from pathlib import Path
from colorama import Fore, Style

def command(args=None, context=None):
    """Смена текущей директории с проверкой пути
    
    Использование:
        cd <директория>  - перейти в указанную директорию
        cd ~             - перейти в домашнюю директорию
        cd ..            - перейти на уровень выше
    """
    if not args:
        print(f"{Fore.YELLOW}Usage: cd <directory>{Style.RESET_ALL}")
        return

    try:
        target_dir = args[0]
        
        # Специальные случаи
        if target_dir == "~":
            target_dir = str(Path.home())
        elif target_dir == "-":
            print(f"{Fore.RED}История директорий не реализована{Style.RESET_ALL}")
            return
        
        # Нормализация пути
        new_dir = str(Path(target_dir).expanduser().absolute())
        
        if not os.path.exists(new_dir):
            print(f"{Fore.RED}E: Directory is not existing{Style.RESET_ALL}")
            return
            
        os.chdir(new_dir)
        
        # Обновляем контекст, если он передан
        if context is not None:
            context['current_dir'] = os.getcwd()
        
    except Exception as e:
        print(f"{Fore.RED}E: {str(e)}{Style.RESET_ALL}")