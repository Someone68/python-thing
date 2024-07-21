import time
import random
from termcolor import colored, cprint
import os
import sys
import select
import termios
import tty


def tprint(words, color, pause=True):
    skip_animation = False

    # Save the terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Set the terminal to raw mode
        tty.setcbreak(fd)

        for char in words:
            if sys.stdin in select.select([sys.stdin], [], [], 0.05)[0]:
                key = sys.stdin.read(1)
                if key == "\n":  # Check for Enter key
                    skip_animation = True
                    break
            colored_char = colored(char, color)
            sys.stdout.write(colored_char)

            # Check for punctuation and set sleep time accordingly
            if char == ",":
                sleep_time = 0.2
            elif char in ".!?":
                sleep_time = 0.7
            else:
                sleep_time = 0.01  # Adjusted to 0.05 to be noticeable

            sys.stdout.flush()
            time.sleep(sleep_time)

        if skip_animation:
            # Clear the current line
            sys.stdout.write("\r" + " " * len(words) + "\r")
            sys.stdout.flush()
            # Print the full text
            sys.stdout.write(colored(words, color))
            sys.stdout.flush()
    finally:
        # Restore the terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if pause:
        input()
    print()  # Move to the next line after printing


def tinput(words, color, pause=True):
    skip_animation = False

    # Save the terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Set the terminal to raw mode
        tty.setcbreak(fd)

        for char in words:
            if sys.stdin in select.select([sys.stdin], [], [], 0.05)[0]:
                key = sys.stdin.read(1)
                if key == "\n":  # Check for Enter key
                    skip_animation = True
                    break
            colored_char = colored(char, color)
            sys.stdout.write(colored_char)

            # Check for punctuation and set sleep time accordingly
            if char == ",":
                sleep_time = 0.2
            elif char in ".!?:":
                sleep_time = 0.37
            else:
                sleep_time = 0.005

            sys.stdout.flush()
            time.sleep(sleep_time)

        if skip_animation:
            # Clear the current line
            sys.stdout.write("\r" + " " * len(words) + "\r")
            sys.stdout.flush()
            # Print the full text
            sys.stdout.write(colored(words, color))
            sys.stdout.flush()
    finally:
        # Restore the terminal settings
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