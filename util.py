import time
import random
from termcolor import colored, cprint
import os
import sys
import select
import curses
from threading import Thread, Event

if sys.platform.startswith('win'):
    import msvcrt
else:
    import termios
    import tty


def input_thread(stop_event):
    """Thread to monitor user input."""
    if sys.platform.startswith('win'):
        while not stop_event.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8')
                if key in ["\r", "\n"]:
                    stop_event.set()
    else:
        while not stop_event.is_set():
            if select.select([sys.stdin], [], [], 0.05)[0]:
                key = sys.stdin.read(1)
                if key in ["\r", "\n"]:
                    stop_event.set()

def tprint(words, color, pause=True):
    stop_event = Event()
    thread = Thread(target=input_thread, args=(stop_event,))
    thread.start()

    platform = sys.platform
    raw_mode = False

    # Platform-specific setup
    if platform.startswith('win'):
        get_char = msvcrt.getch
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        raw_mode = True

        def get_char():
            return sys.stdin.read(1)

    try:
        if raw_mode:
            tty.setcbreak(fd)

        for i, char in enumerate(words):
            # Check for input every character to allow immediate response
            if stop_event.is_set():
                break

            colored_char = colored(char, color)
            sys.stdout.write(colored_char)

            # Adjust sleep time based on punctuation
            sleep_time = {
                ',': 0.36,
                '.': 0.47,
                '!': 0.47,
                '?': 0.47
            }.get(char, 0.03)

            sys.stdout.flush()
            if not stop_event.is_set():
                time.sleep(sleep_time)  # Sleep only if no input was detected

        if stop_event.is_set():
            # Clear and overwrite the line if animation is skipped
            sys.stdout.write("\r" + " " * len(words) + "\r")
            sys.stdout.flush()
            sys.stdout.write(colored(words, color))
            sys.stdout.flush()
    finally:
        if raw_mode:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if pause:
        input()
    print()  # Move to the next line after printing

def tinput(words, color, pause=True):
    stop_event = Event()
    thread = Thread(target=input_thread, args=(stop_event,))
    thread.start()

    platform = sys.platform
    raw_mode = False

    # Platform-specific setup
    if platform.startswith('win'):
        get_char = msvcrt.getch
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        raw_mode = True

        def get_char():
            return sys.stdin.read(1)

    try:
        if raw_mode:
            tty.setcbreak(fd)

        for i, char in enumerate(words):
            # Check for input every character to allow immediate response
            if stop_event.is_set():
                break

            colored_char = colored(char, color)
            sys.stdout.write(colored_char)

            # Adjust sleep time based on punctuation
            sleep_time = {
                ',': 0.36,
                '.': 0.47,
                '!': 0.47,
                '?': 0.47
            }.get(char, 0.03)

            sys.stdout.flush()
            if not stop_event.is_set():
                time.sleep(sleep_time)  # Sleep only if no input was detected

        if stop_event.is_set():
            # Clear and overwrite the line if animation is skipped
            sys.stdout.write("\r" + " " * len(words) + "\r")
            sys.stdout.flush()
            sys.stdout.write(colored(words, color))
            sys.stdout.flush()
    finally:
        if raw_mode:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if pause:
        return input(colored(" > ", color))
    print()  # Move to the next line after printing



def clearc():
    os.system("cls" if os.name == "nt" else "clear")


def fprint(text, color="light_magenta", clear=True, select=False):  # STANDS FOR FANCY PRINT
    if clear:
        clearc()
    print("---")
    tprint(text, color, not select)
    # print("")


def finput(text, color="light_green", clear=True, required=True):
    if clear:
        clearc()
    print("---")
    if not required:
        userinput = tinput(text, color)
    reset = False
    while True and required:
        if reset:
            userinput = input(colored(text + " > ", color))
        else:
            userinput = tinput(text, color)
        if not userinput.strip():
            reset = True
            sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()
        else:
            break
    print("")
    return userinput

try:
    from msvcrt import getwch as getch
except ImportError:
    def getch():
        """Stolen from http://code.activestate.com/recipes/134892/"""
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def input_():
    """Print and return input without echoing newline."""
    response = ""
    while True:
        c = getch()
        if c == "\b" and len(response) > 0:
            # Backspaces don't delete already printed text with getch()
            # "\b" is returned by getch() when Backspace key is pressed
            response = response[:-1]
            sys.stdout.write("\b \b")
        elif c not in ["\r", "\b"]:
            # Likewise "\r" is returned by the Enter key
            response += c
            sys.stdout.write(c)
        elif c == "\r":
            break
        sys.stdout.flush()
    return response

class Enemy_Ship:
    def __init__(self, max_health, max_shield, damage) -> None:
        self.max_health = max_health
        self.health = max_health
        self.max_shield = max_shield
        self.shield = max_shield
        self.damage = damage





def draw_bar(stdscr, cursor_pos, bar_width, bar_start_x):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    bar_y = h // 2

    # Draw the bar
    stdscr.addstr(bar_y+3, bar_start_x-1, '(press space when X reaches the center)', curses.color_pair(1))
    stdscr.addstr(bar_y+1, bar_start_x-1, '╚', curses.color_pair(1))
    stdscr.addstr(bar_y, bar_start_x-1, '║', curses.color_pair(1))
    stdscr.addstr(bar_y-1, bar_start_x-1, '╔', curses.color_pair(1))
    stdscr.addstr(bar_y+1, bar_start_x+bar_width, '╝', curses.color_pair(1))
    stdscr.addstr(bar_y, bar_start_x+bar_width, '║', curses.color_pair(1))
    stdscr.addstr(bar_y-1, bar_start_x+bar_width, '╗', curses.color_pair(1))

    for i in range(bar_width):
        if bar_start_x + i == w // 2 or bar_start_x + i == w // 2 - 1 or bar_start_x + i == w // 2 + 1:  # Center of the bar
            stdscr.addstr(bar_y+1, bar_start_x + i, '═', curses.color_pair(2))
            stdscr.addstr(bar_y, bar_start_x + i, '|', curses.color_pair(2))
            stdscr.addstr(bar_y-1, bar_start_x + i, '═', curses.color_pair(2))
        else:
            stdscr.addstr(bar_y+1, bar_start_x + i, '═', curses.color_pair(1))
            stdscr.addstr(bar_y, bar_start_x + i, '|', curses.color_pair(1))
            stdscr.addstr(bar_y-1, bar_start_x + i, '═', curses.color_pair(1))

    # Draw the cursor
    cursor_x = bar_start_x + cursor_pos
    stdscr.addstr(bar_y, cursor_x, '|', curses.color_pair(3))
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)  # Default background
    curses.init_pair(2, curses.COLOR_YELLOW, -1) 

    if curses.COLORS >= 256:
        # Define a gray background if the terminal supports 256 colors
        curses.init_color(8, 300, 300, 300)  # Define a gray color
        curses.init_pair(3, curses.COLOR_RED, 8)  # Red foreground, gray background
        
    else:
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Fallback to black background

    stdscr.nodelay(1)  # Make getch() non-blocking

    bar_width = 21
    cursor_speed = 0.035
    cursor_direction = 1  # 1 for right, -1 for left
    cursor_pos = 0

    h, w = stdscr.getmaxyx()
    bar_start_x = w // 2 - bar_width // 2
    
    draw_bar(stdscr, cursor_pos, bar_width, bar_start_x)

    time.sleep(0.7)
    while True:
        key = stdscr.getch()

        
        if key == ord(' '):  # Space bar pressed
            time.sleep(1)
            stdscr.refresh()
            stdscr.getch()
            return cursor_pos

        # Recalculate bar start position if window size changes
        new_h, new_w = stdscr.getmaxyx()
        if new_w != w:
            w = new_w
            bar_start_x = w // 2 - bar_width // 2

        draw_bar(stdscr, cursor_pos, bar_width, bar_start_x)
        cursor_pos += cursor_direction

        if cursor_pos >= bar_width or cursor_pos < 0:
            cursor_direction *= -1  # Change direction
            cursor_pos += cursor_direction

        time.sleep(cursor_speed)

def bar():
    return curses.wrapper(main)
