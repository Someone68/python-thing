from math import floor
import random
import time
from termcolor import cprint
from util import clearc, fprint, hide_cursor, show_cursor
from events import select, Program, events_list_1, events_list_2, boss_1, bosslevel
from util import bar, bar2
import psutil
import os


def log_memory_usage():
    process = psutil.Process(os.getpid())
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")


def exm():
    print("test pased")


class Ship:
    def __init__(self, name) -> None:
        self.name = name
        self.health = 100
        self.shield = 75
        self.food = 200
        self.max_shield = 75
        self.energy = 75
        self.max_health = 100
        self.max_energy = 75
        self.damage = 1
        self.distance = 0
        self.distance_required = 500
        self.credits = 10
        self.cycle = 0
        self.energybefore = 50
        self.foodbefore = 200
        self.distancebefore = 0
        self.lastevent = None
        self.programs = []
        self.distance_multiplier = 1

    def is_alive(self):
        return self.energy > 0 and self.food > 0 and self.health > 0

    def print_stats(self):
        self.damage = round(self.damage, 2)
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        cprint("(Press enter to proceed)\n", "light_grey")
        cprint("=" * 45, "grey")
        header = f"Cycle {self.cycle}"
        cprint(f"{header:^45s}", "light_yellow")
        cprint("=" * 45, "light_grey")
        if self.energy < 15:
            cprint("  WARNING: ENERGY CRITICALLY LOW  ", "black", "on_light_red")
        elif self.energy < 25:
            cprint("  WARNING: ENERGY LOW  ", "light_yellow")
        if self.shield < 1:
            cprint("  WARNING: SHIELD IS DOWN  ", "black", "on_light_yellow")
        if self.health < 25:
            cprint("  WARNING: HEALTH CRITICALLY LOW  ", "black", "on_light_red")
        elif self.health < 50:
            cprint("  WARNING: HEALTH LOW  ", "light_yellow")

        cprint(f" STATISTICS: {self.name.upper()}", "light_yellow")
        cprint(
            f"     DISTANCE {f'{self.distance} / {self.distance_required}':>10s}    CYCLE {f'{self.cycle}':>10s}",
            "light_magenta",
        )
        cprint(
            f"       HEALTH {f'{self.health} / {self.max_health}':>10s}   SHIELD {f'{self.shield} / {self.max_shield}':>10s}",
            "light_red",
        )
        cprint(
            f"       ENERGY {f'{self.energy} / {self.max_energy}':>10s}     FOOD {f'{self.food}':>10s}",
            "light_cyan",
        )
        cprint(
            f" DAMAGE MULTP {f'{round(self.damage * 100)}%':>10s}  CREDITS {f'[c] {self.credits}':>10s}",
            "light_green",
        )
        cprint("=" * 45)
        #
        # log_memory_usage()
        hide_cursor()
        thing = input()
        if thing == "devtools":
            while True:
                cprint("[devtools] select:", "light_yellow")
                choice = select(
                    ["change stats", "run event", "show memory usage", "cancel"]
                )
                if choice == "change stats":
                    cprint("choose a stat to change:", "light_magenta")
                    change = select(list(vars(self).keys()))
                    value = input("value: ")
                    if type(getattr(self, change)) is int:
                        setattr(self, change, int(value))
                    elif type(getattr(self, change)) is float:
                        setattr(self, change, float(value))
                    elif type(getattr(self, change)) is list:
                        setattr(self, change, list(value))
                    elif type(getattr(self, change)) is dict:
                        setattr(self, change, dict(value))
                    else:
                        setattr(self, change, value)
                    cprint("success. enter to continue")
                    input()
                elif choice == "run event":
                    cprint("choose an event to run:")
                    events_list = events_list_1 + events_list_2
                    run = select(list(map(lambda x: x.__name__, events_list)))
                    function_names = {
                        func.__name__: idx for idx, func in enumerate(events_list)
                    }
                    to_run = events_list[function_names[run]]
                    clearc()
                    events_list[events_list.index(to_run)](self)
                elif choice == "show memory usage":
                    log_memory_usage()
                    input("enter to continue . . . ")
                else:
                    break
        show_cursor()

    def take_damage(self, damage, cancel_shield=False):
        if self.shield < 1 or cancel_shield:
            self.health -= damage
        elif damage > self.shield:
            self.shield = 0
            self.health += self.shield - damage
        else:
            self.shield -= damage

    def heal(self, heal):
        if self.health + heal > self.max_health:
            self.health = self.max_health
        else:
            self.health += heal

    def calc_resources(self):
        travel_dist = round(random.randint(9, 27) * self.distance_multiplier)
        energy_used = floor(travel_dist * 0.5)
        food_consumed = floor(travel_dist * 0.8)
        self.distance += travel_dist
        self.food -= food_consumed
        self.energy -= energy_used
        return {
            "travel_dist": travel_dist,
            "food_consumed": food_consumed,
            "energy_used": energy_used,
        }

    def calcfight(self):  # dont look at the variable names
        undertale_thingamajiggy = bar()
        unformulaed_thing = abs(abs(11 - undertale_thingamajiggy) - 11)
        return round(unformulaed_thing * 2.5 * self.damage)

    def calcshoot(self):  # dont look at the variable names
        undertale_thingamajiggy = bar2()
        undertale_thingamajiggy2 = bar2()
        undertale_thingamajiggy3 = bar2()
        unformulaed_thing = (
            abs(abs(11 - undertale_thingamajiggy) - 11)
            + abs(abs(11 - undertale_thingamajiggy2) - 11)
            + abs(abs(11 - undertale_thingamajiggy3) - 11)
        )
        return round(unformulaed_thing * 1.3)

    def random_event(self):
        clearc()
        self.energybefore = self.energy
        self.foodbefore = self.food
        self.distancebefore = self.distance
        if self.distance > 120 and bosslevel < 1:
            boss_1(self)
            return
        if self.energy < 15:
            fprint(
                "The ship's energy is critically low. Do you want to re-reoute to a fuel station, losing distance?",
                color="light_red",
                select=True,
            )
            choice = select(["RE-ROUTE", "DO NOT"])
            if choice == "RE-ROUTE":
                distance_lost = random.randint(10, 30)
                fprint(
                    f"You decided to re-route to a fuel station, losing {distance_lost} distance."
                )
                self.distance -= distance_lost
                self.lastevent = 0
                events_list_1[0](self)
                return
            else:
                fprint("You decided to keep going...")

        event_chosen = random.choice(events_list_1 if bosslevel == 0 else events_list_2)
        while event_chosen == self.lastevent:
            event_chosen = random.choice(
                events_list_1 if bosslevel == 0 else events_list_2
            )
        self.lastevent = events_list_1.index(event_chosen)
        event_chosen(self)
