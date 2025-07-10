from core.commands import load_commands
from colorama import Fore, Back, Style
import os
import platform
from datetime import datetime
from utils.auth import login_loop
import time

current_user = login_loop()
hostname = platform.node()

def linux_prompt(username):
    # Получаем системную информацию
    hostname = platform.node()
    current_time = datetime.now().strftime('%H:%M:%S')
    current_dir = os.getcwd()
    dir_name = os.path.basename(current_dir)
    
    # Формируем цветное приглашение
    prompt = (
        f"{Fore.GREEN}{username}{Style.RESET_ALL}"  # Зеленый username
        f"{Fore.WHITE}@{Style.RESET_ALL}"          # Белый @
        f"{Fore.BLUE}{hostname}{Style.RESET_ALL}"  # Синий hostname
        f"{Fore.WHITE}:{Style.RESET_ALL}"         # Белый :
        f"{Fore.YELLOW}~{dir_name}{Style.RESET_ALL}" # Желтый каталог
        f"{Fore.WHITE} [{current_time}]{Style.RESET_ALL}\n"  # Время
        f"{Fore.RED}➜{Style.RESET_ALL} "          # Красная стрелка
    )
    return prompt

def main():
    commands = load_commands()
    print(f"Загружено команд: {len(commands)}")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        try:
            user_input = input(linux_prompt(current_user)).strip().split()
            if not user_input:
                continue
                
            cmd = user_input[0]
            args = user_input[1:] if len(user_input) > 1 else None

            if cmd in commands:
                try:
                    commands[cmd](args)
                except Exception as e:
                    print(f"Ошибка выполнения: {str(e)}")
            elif cmd == "exit":
                break
            else:
                print("Неизвестная команда. Введите 'help' для списка команд.")
        except KeyboardInterrupt:
            print(" Use 'exit' to logout")
if __name__ == "__main__":
    main()
