import time
import random
from termcolor import colored, cprint
from util import tprint, tinput, fprint, finput, clearc
from simple_term_menu import TerminalMenu

def select(options):
    terminal_menu = TerminalMenu(options, menu_highlight_style=("underline",))
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]

def shipwreck(ship):
    if(ship.cycle == 1):
        cprint("(use arrow keys to select and enter to proceed)", "grey")
    fprint("You noticed a destroyed shipwreck. It may have some useful resources. What do you do?", "light_magenta", True, True)
    choice = select(["EXPLORE", "LEAVE IT"])
    if(choice == "EXPLORE"):
        energyused = random.randint(3,6)
        if(random.randint(0, 1) == 1):
            fprint(f"You didn't find anything. Used {energyused} energy.", "light_red")
        else:
            creditsearned = random.randint(12,23)
            foodearned = random.randint(20,45)
            fprint(f"You found {creditsearned} credits and {foodearned} food. Used {energyused} energy.")
            ship.food += foodearned
            ship.credits += creditsearned
        ship.energy -= energyused
    else:
        fprint("You decided to save energy and pass by the shipwreck")

def fuel(ship):
    if(ship.cycle == 1):
        cprint("(use arrow keys to select and enter to proceed)", "grey")
    fprint("You arrived at a fuel station, which can refill your energy. Do you want to refill, using 25 food?", "light_yellow", True, True)
    choice = select(["REFILL", "CONTINUE"])
    if(choice == "REFILL"):
        fprint("You decided to refuel. Keep pressing ENTER to refill energy!")
        start_time = time.time()
        end_time = start_time + 7
        press_count = 0

        while time.time() < end_time:
            clearc()
            input(colored(f"REFUELED: {press_count / 2} | PRESS ENTER TO REFUEL > ", "light_yellow"))
            press_count += 1

        ship.energy += int(round(press_count / 2))
        if(press_count > 0):
            fprint(f"Successfully refilled {press_count / 2} energy! Used 25 food.", "light_green")
        else:
            fprint(f"Unsuccessful! Keep pressing enter to refill. Used 25 food.", "light_red")
        ship.food -= 25
    else:
        fprint(f"You decided to save time and continue. You can always refuel later.", "light_yellow")
events_list_1 = [fuel, shipwreck]