import time
import random

try:
    from termcolor import colored, cprint
except ImportError:
    print(
        "\x1b[38;5;9mPlease install the required libraries. Read README.md to figure out how.\x1b[0m"
    )
    quit()
from events import select
from util import hide_cursor, show_cursor, tprint, tinput, fprint, finput, clearc
from ship import Ship
import datetime
import sys
import os


def main():
    global ship, dev_mode
    clearc()
    cprint("(Press enter to skip/proceed)", "light_grey")
    fprint(
        "Welcome Captain. We are ready to depart and head to the Stellaris Rift.",
        "light_magenta",
        False,
    )

    # log_memory_usage()
    # input()
    name = finput("Before departure, name the ship", "light_green", False)
    ship = Ship(name)

    if name.lower() == "hello world":
        dev_mode = True
    # log_memory_usage()
    # input()
    fprint("Excellent, let's begin.")

    while ship.distance < ship.distance_required and ship.is_alive():
        clearc()
        ship.cycle += 1
        consumed = ship.calc_resources()
        ship.print_stats()
        if (
            random.randint(1, 5) > 1
            or ship.energy < 20
            or (ship.distance > 120 and ship.bosslevel == 1)
            or (ship.distance > 300 and ship.bosslevel == 2)
        ):
            ship.random_event()
        fprint(f":: In this cycle:", "light_blue", False, True)
        tprint(
            f":: - {consumed['energy_used']} energy consumed.",
            pause=False,
            color="light_blue",
        )
        tprint(
            f":: - {consumed['food_consumed']} food eaten.",
            pause=False,
            color="light_blue",
        )
        tprint(
            f":: - Traveled {consumed['travel_dist']}ly.",
            pause=True,
            color="light_blue",
        )
    if ship.is_alive() and ship.bosslevel == 3:
        clearc()
        cprint(
            """==================
 Mission Complete
==================""",
            "light_green",
        )
        fprint(
            "You successfully arrived at the Stellaris Rift. Ty for playing bye",
            clear=False,
            select=True,
        )
    else:
        clearc()
        cprint(
            """===========
 GAME OVER
===========""",
            "light_red",
        )
        fprint(
            f"You{' ran out of energy' if ship.energy < 1 else (' ran out of food' if ship.food < 1 else ('r ship ran out of health' if ship.health < 1 else 'error'))}.",
            clear=False,
            color="red",
            select=True,
        )


def menu():
    clearc()

    cprint("=" * 25)
    cprint(f"{'The Stellaris Rift':^25}", "blue")
    cprint("=" * 25)
    print()
    print(colored(f" Select an option", "yellow"))
    choice = select(["PLAY", "CREDITS", "QUIT"])

    clearc()
    if choice == "PLAY":
        load()
    elif choice == "CREDITS":
        credits()
    else:
        clearc()
        quit()


def credits():
    clearc()
    cprint(" " * 25)
    cprint(f"{'The Stellaris Rift':^25}", "blue")
    cprint(" " * 25)
    cprint(f"{'Programming':^25}", "green")
    cprint(f"{'FelixM':^25}")
    cprint(f"{'Stack Overflow':^25}")
    cprint("")
    cprint(f"{'Idea/Inspiration':^25}", "green")
    cprint(f"{'HACKINGTONS':^25}")
    cprint(f"{'ChatGPT':^25}")
    cprint("")
    cprint(f"{'Programming Help':^25}", "green")
    cprint(f"{'Obscure Python Libraries':^25}")
    cprint(f"{'ChatGPT':^25}")
    cprint("")
    cprint(f"{'Press enter to exit':^25}")
    hide_cursor()
    input()
    show_cursor()
    menu()


def load():
    hide_cursor()
    animation = [
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]",
    ]

    for i in range(len(animation)):
        time.sleep(random.uniform(0.06, 0.3))

        sys.stdout.write(
            "\rLoading... \x1b[38;5;218m" + animation[i % len(animation)] + "\x1b[0m"
        )
        sys.stdout.flush()

    print("\n")

    time.sleep(1)
    show_cursor()
    main()


menu()
