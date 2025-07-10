import curses
import os
from pathlib import Path
from typing import List, Dict, Optional

class Notepad:
    def __init__(self, stdscr, context: dict):
        self.stdscr = stdscr
        self.buffer: List[str] = [""]
        self.cursor_y = 0
        self.cursor_x = 0
        self.filename: Optional[str] = None
        self.context = context
        self.setup_curses()
        self.setup_hotkeys()
        
        if context.get('file_to_open'):
            self.load_file(context['file_to_open'])

    def setup_curses(self):
        """Инициализация curses"""
        self.stdscr.keypad(True)
        curses.curs_set(1)
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def setup_hotkeys(self):
        """Настройка горячих клавиш"""
        self.hotkeys = {
            curses.KEY_F1: self.show_help,
            curses.KEY_F2: self.save_file,
            curses.KEY_F3: self.open_file_dialog,
            curses.KEY_F10: self.exit_notepad,
            curses.KEY_DC: self.delete_line,
        }

    def show_help(self):
        """Показывает справку по горячим клавишам"""
        help_text = [
            "Горячие клавиши:",
            "F1        - Эта справка",
            "F2        - Сохранить файл",
            "F3        - Открыть файл",
            "F10       - Выход",
            "Del       - Удалить строку",
            "Стрелки   - Навигация",
            "Tab       - Отступ",
            "",
            "Нажмите любую клавишу чтобы продолжить..."
        ]
        
        max_y, max_x = self.stdscr.getmaxyx()
        help_window = curses.newwin(min(12, max_y-2), min(50, max_x-4), 1, 1)
        help_window.border()
        
        for i, line in enumerate(help_text):
            self.safe_addstr(help_window, i+1, 2, line[:min(46, max_x-6)])
        
        help_window.refresh()
        help_window.getch()

    def delete_line(self):
        """Удаляет текущую строку"""
        if len(self.buffer) > 1:
            del self.buffer[self.cursor_y]
            self.cursor_y = min(self.cursor_y, len(self.buffer)-1)
            self.cursor_x = min(self.cursor_x, len(self.buffer[self.cursor_y]))
        else:
            self.buffer = [""]
            self.cursor_x = 0
            self.cursor_y = 0

    def exit_notepad(self):
        """Выход из блокнота"""
        raise KeyboardInterrupt

    def safe_addstr(self, win, y: int, x: int, text: str, attr=curses.A_NORMAL):
        """Безопасный вывод текста в окно"""
        try:
            max_y, max_x = win.getmaxyx()
            if 0 <= y < max_y and 0 <= x < max_x:
                text = text[:max_x - x - 1]
                win.addstr(y, x, text, attr)
                return True
        except:
            pass
        return False

    def handle_input(self, key: int):
        """Обработка ввода пользователя"""
        # Обработка горячих клавиш
        if key in self.hotkeys:
            self.hotkeys[key]()
            return

        # Навигация стрелками
        if key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
            self.cursor_x = min(self.cursor_x, len(self.buffer[self.cursor_y]))
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(len(self.buffer) - 1, self.cursor_y + 1)
            self.cursor_x = min(self.cursor_x, len(self.buffer[self.cursor_y]))
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(len(self.buffer[self.cursor_y]), self.cursor_x + 1)
        
        # Обработка Tab
        elif key == ord('\t'):
            self.insert_text('    ')
        
        # Enter
        elif key in (curses.KEY_ENTER, 10, 13):
            self.insert_newline()
        
        # Backspace
        elif key == curses.KEY_BACKSPACE:
            self.handle_backspace()
        
        # Печатные символы
        elif 32 <= key <= 126:
            self.insert_text(chr(key))

    def insert_text(self, text: str):
        """Вставка текста в текущую позицию"""
        line = self.buffer[self.cursor_y]
        self.buffer[self.cursor_y] = line[:self.cursor_x] + text + line[self.cursor_x:]
        self.cursor_x += len(text)

    def insert_newline(self):
        """Вставка новой строки"""
        current_line = self.buffer[self.cursor_y]
        new_line = current_line[self.cursor_x:]
        self.buffer[self.cursor_y] = current_line[:self.cursor_x]
        self.buffer.insert(self.cursor_y + 1, new_line)
        self.cursor_y += 1
        self.cursor_x = 0

    def handle_backspace(self):
        """Обработка backspace"""
        if self.cursor_x > 0:
            line = self.buffer[self.cursor_y]
            self.buffer[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_x = len(self.buffer[self.cursor_y - 1])
            self.buffer[self.cursor_y - 1] += self.buffer[self.cursor_y]
            del self.buffer[self.cursor_y]
            self.cursor_y -= 1

    def load_file(self, filepath: str):
        """Загрузка файла"""
        try:
            if not os.path.exists(filepath):
                self.show_message(f"Файл не найден: {filepath}", curses.color_pair(2))
                return False
                
            with open(filepath, 'r', encoding='utf-8') as f:
                self.buffer = [line.rstrip('\n') for line in f.readlines()] or [""]
            
            self.filename = filepath
            self.cursor_y = 0
            self.cursor_x = 0
            self.show_message(f"Загружен: {filepath}")
            return True
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}", curses.color_pair(2))
            return False

    def save_file(self):
        """Сохранение файла"""
        try:
            suggested_name = self.filename or "newfile.txt"
            filepath = self.get_input(f"Сохранить как ({suggested_name}): ") or suggested_name
            
            if not filepath:
                return False
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.buffer))
            
            self.filename = filepath
            self.show_message(f"Сохранено: {filepath}")
            return True
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}", curses.color_pair(2))
            return False

    def open_file_dialog(self):
        """Диалог открытия файла"""
        filepath = self.get_input("Открыть файл: ")
        if filepath:
            self.load_file(filepath)

    def show_message(self, message: str, attr=curses.A_NORMAL):
        """Показать сообщение"""
        max_y, max_x = self.stdscr.getmaxyx()
        self.safe_addstr(self.stdscr, max_y-1, 0, " " * (max_x-1))
        self.safe_addstr(self.stdscr, max_y-1, 0, message[:max_x-2], attr)
        self.stdscr.refresh()

    def get_input(self, prompt: str) -> Optional[str]:
        """Получить ввод от пользователя"""
        curses.echo()
        self.show_message(prompt)
        input_str = self.stdscr.getstr().decode('utf-8')
        curses.noecho()
        return input_str if input_str.strip() else None

    def draw_interface(self):
        """Отрисовка интерфейса"""
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        
        # Отрисовка текста
        for i in range(min(len(self.buffer), max_y-1)):
            self.safe_addstr(self.stdscr, i, 0, self.buffer[i][:max_x-1])
        
        # Статус-бар
        status = f" Строка {self.cursor_y+1}/{len(self.buffer)} Поз {self.cursor_x} "
        if self.filename:
            status += f"| {os.path.basename(self.filename)}"
        self.safe_addstr(self.stdscr, max_y-1, 0, status.ljust(max_x-1), curses.color_pair(1))
        
        # Позиционирование курсора
        try:
            self.stdscr.move(
                min(self.cursor_y, max_y-2),
                min(self.cursor_x, len(self.buffer[self.cursor_y]))
            )
        except curses.error:
            self.stdscr.move(0, 0)
        
        self.stdscr.refresh()

    def run(self):
        """Главный цикл"""
        while True:
            self.draw_interface()
            try:
                key = self.stdscr.getch()
                self.handle_input(key)
            except KeyboardInterrupt:
                break

def curses_wrapper(stdscr, context: dict):
    Notepad(stdscr, context).run()

def command(args=None, context=None):
    """Точка входа для модульной системы"""
    try:
        import curses
        context = context or {}
        if args:
            context['file_to_open'] = args[0]
        curses.wrapper(lambda stdscr: curses_wrapper(stdscr, context))
    except Exception as e:
        print(f"Ошибка блокнота: {str(e)}")
    """Точка входа для модульной системы"""
    try:
        import curses
        context = context or {}
        if args:
            context['file_to_open'] = args[0]
        curses.wrapper(lambda stdscr: curses_wrapper(stdscr, context))
    except Exception as e:
        print(f"Ошибка блокнота: {str(e)}")