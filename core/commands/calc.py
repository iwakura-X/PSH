import operator
from colorama import Fore, Style

def command(args=None, context=None):
    """Калькулятор с безопасным eval и поддержкой основных операций
    
    Использование:
        calc <выражение>  - вычислить математическое выражение
        calc               - интерактивный режим
    """
    if not args:  # Интерактивный режим
        print(f"{Fore.YELLOW}Interactive calclator(exit for exit){Style.RESET_ALL}")
        while True:
            try:
                expr = input(f"{Fore.CYAN}calc>{Style.RESET_ALL} ").strip()
                if expr.lower() == 'exit':
                    break
                if expr:
                    _safe_eval(expr)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break
        return

    # Режим однострочного вычисления
    _safe_eval(' '.join(args))

def _safe_eval(expr: str):
    """Безопасное вычисление математических выражений"""
    try:
        # Разрешенные операторы и функции
        SAFE_OPS = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod,
            '//': operator.floordiv,
        }

        # Парсим выражение
        tokens = []
        current_token = ''
        for char in expr.replace(' ', ''):
            if char in SAFE_OPS:
                if current_token:
                    tokens.append(float(current_token))
                    current_token = ''
                tokens.append(char)
            else:
                current_token += char
        if current_token:
            tokens.append(float(current_token))

        # Вычисляем
        result = tokens[0]
        for i in range(1, len(tokens), 2):
            op = tokens[i]
            num = tokens[i+1]
            result = SAFE_OPS[op](result, num)

        print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}E: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Operations: + - * / ** % //{Style.RESET_ALL}")