import time
import random
from termcolor import colored, cprint
from util import hide_cursor, show_cursor, tprint, tinput, fprint, finput, clearc
from ship import Ship
import datetime
import sys
import psutil
import os


def test():
    clearc()
    cprint("Testing your terminal's speed...", "light_magenta")
    time.sleep(1)
    words = "testing..."
    start = datetime.datetime.now()
    stop = start + datetime.timedelta(0, 1.7)
    failed = False
    for char in words:
        if datetime.datetime.now() > stop:
            fprint("Speed test FAILED", "red")
            failed = True
            choice = input(
                "Terminal is not fast enough for this game! Do you want to [c]ontinue (not recommended for the best experience) or [e]xit?"
            ).lower()
            if choice == "c" or choice == "continue":
                fprint("Continuing...", select=True)
            else:
                cprint(
                    "Good choice, try freeing up your memory, your terminal is slow."
                )
                quit()
            break
        colored_char = char
        sys.stdout.write(colored_char)
        sleep_time = 0.15

        sys.stdout.flush()
        time.sleep(sleep_time)
    if not failed:
        fprint("Speed test passed!")


# set to true
should_check_speed = False

if should_check_speed:
    test()


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
        if random.randint(1, 5) > 1 or ship.energy < 20:
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
    if ship.is_alive():
        clearc()
        cprint(
            """==================
 Mission Complete
==================""",
            "light_green",
        )
        input()
        fprint("You successfully arrived at the Stellaris Rift. Ty for playing bye")
    else:
        clearc()
        cprint(
            """===========
 GAME OVER
===========""",
            "light_red",
        )
        input()
        fprint("nice try")


clearc()


cprint("=" * 25)
cprint(f"{'The Stellaris Rift':^25}", "blue")
cprint("=" * 25)
print()
print(colored(f"{'Press enter to begin':^25}", "yellow"))
hide_cursor()
input("")

clearc()

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
