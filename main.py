import time
import random
from termcolor import colored, cprint
from util import tprint, tinput, fprint, finput, clearc
from ship import Ship




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
        if(random.randint(1,5) > 1 or ship.energy < 20):
            ship.random_event()
        fprint(f":: In this cycle:", "light_blue", False, True)
        tprint(f":: - {consumed['energy_used']} energy consumed.", pause=False, color="light_blue")
        tprint(f":: - {consumed['food_consumed']} food eaten.", pause=False, color="light_blue")
        tprint(f":: - Traveled {consumed['travel_dist']}ly.", pause=True, color="light_blue")
    if(ship.is_alive()):
        clearc()
        cprint("""==================
 Mission Complete
==================""", "light_green")
        input()
        fprint("You successfully arrived at the Stellaris Rift. Ty for playing bye")
    else:
        clearc()
        cprint("""===========
 GAME OVER
===========""", "light_red")
        input()
        fprint("nice try")
main()