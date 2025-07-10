import os
import hashlib
from pathlib import Path
from getpass import getpass
import sys
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Определяем абсолютный путь к файлу пользователей
def get_users_db_path():
    """Возвращает абсолютный путь к файлу users.txt"""
    # Вариант 1: Рядом с auth.py
    db_path = Path(__file__).parent.parent / 'data' / 'users.txt'
    
    # Вариант 2: В корне проекта (раскомментировать если нужно)
    # db_path = Path(__file__).parent.parent / 'data' / 'users.txt'
    
    db_path.parent.mkdir(exist_ok=True, parents=True)
    return db_path.absolute()

USERS_FILE = get_users_db_path()

def init_auth_system():
    clear()
    """Инициализирует систему аутентификации"""
    try:
        USERS_FILE.parent.mkdir(exist_ok=True, parents=True)
        if not USERS_FILE.exists():
            USERS_FILE.touch(mode=0o600)
            clear()
            print(f"✅ Created new user DB at {USERS_FILE}")
        else:
            clear()
            print(f"ℹ️ Using existing user DB at {USERS_FILE}")
    except Exception as e:
        clear()
        print(f"🚨 Fatal auth error: {str(e)}")
        sys.exit(1)

def hash_password(password: str) -> str:
    """Хеширует пароль с использованием SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(login: str) -> bool:
    """Проверяет существование пользователя"""
    with open(USERS_FILE, 'r') as f:
        for line in f:
            if line.split(':')[0] == login:
                return True
    return False

def register_user(login: str, password: str) -> bool:
    """Регистрирует нового пользователя"""
    if user_exists(login):
        return False
    
    with open(USERS_FILE, 'a') as f:
        f.write(f"{login}:{hash_password(password)}\n")
    return True

def verify_user(login: str, password: str) -> bool:
    """Проверяет логин и пароль"""
    with open(USERS_FILE, 'r') as f:
        for line in f:
            stored_login, stored_hash = line.strip().split(':')
            if stored_login == login and stored_hash == hash_password(password):
                return True
    return False

def login_loop() -> str:
    """Основной цикл аутентификации"""
    init_auth_system()
    
    while True:
        clear()
        print('+===============+')
        print("|PSH Auth System|")
        print("|-1. Login      |")
        print("|-2. Register   |")
        print("|-3. Exit       |")
        print('+===============+')
        
        choice = input("> ").strip()
        
        if choice == '1':  # Логин
            clear()
            login = input("Login: ").strip()
            password = getpass("Password: ").strip()
            
            if verify_user(login, password):
                clear()
                print(f"\nWelcome, {login}!")
                return login
            clear()
            print("\nInvalid login or password!")
            time.sleep(0.5)
            
        elif choice == '2':  # Регистрация
            clear()
            login = input("New login: ").strip()
            if not login:
                print("Login cannot be empty!")
                continue
                
            password = getpass("New password: ").strip()
            password_confirm = getpass("Confirm password: ").strip()
            
            if password != password_confirm:
                print("Passwords don't match!")
                time.sleep(0.5)
                clear()
                continue
                
            if register_user(login, password):
                clear()
                print("Registration was successful! Please login.")
                time.sleep(1)
            else:
                print("User already exists!")
                time.sleep(0.8)
                clear()
                
        elif choice == '3':  # Выход
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice!")
            time.sleep(1)
            clear()