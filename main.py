import time
import random
from termcolor import colored, cprint
from util import tprint, tinput, fprint, finput, clearc
from simple_term_menu import TerminalMenu
from ship import Ship


def select(options):
    terminal_menu = TerminalMenu(options, menu_highlight_style=("underline",))
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]

def main():
    global ship
    clearc()
    cprint("(Press enter to skip/proceed)", "grey")
    fprint("Welcome Captain. We are ready to depart and head to the Stellaris Rift.", "light_magenta", False)
    ship = Ship(finput("Before departure, name the ship", "light_green", False))
    fprint("Excellent, let's begin.")

    while ship.distance < ship.distance_required and ship.is_alive():
        clearc()
        ship.cycle += 1
        consumed = ship.calc_resources()
        ship.print_stats()

        fprint(f":: In this cycle:\n:: - {consumed['energy_used']} energy consumed.\n:: - {consumed['food_consumed']} food eaten.\n:: - Traveled {consumed['travel_dist']}ly.", "light_blue", False)
main()