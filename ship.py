from math import floor
import random
import time
from termcolor import cprint
from util import clearc, fprint
from events import events_list_1


class Ship:
    def __init__(self, name) -> None:
        self.name = name
        self.health = 100
        self.shield = 75
        self.food = 200
        self.max_shield = 75
        self.energy = 50
        self.max_health = 100
        self.max_energy = 50
        self.damage = 10
        self.distance = 0
        self.distance_required = 500
        self.credits = 10
        self.cycle = 0
        self.energybefore = 50
        self.foodbefore = 200
        self.distancebefore = 0

    def is_alive(self):
        return self.energy > 0 and self.food > 0 and self.health > 0
    
    def print_stats(self):
        cprint("(Press enter to proceed)\n", "grey")
        cprint("="*45, "grey")
        header = f"Cycle {self.cycle}"
        cprint(f"{header:^45s}", "grey")
        cprint("="*45, "grey")
        cprint(f"STATISTICS: {self.name.upper()}", "light_yellow")
        cprint(f" DISTANCE {f'{self.distance} / {self.distance_required}':>10s}    CYCLE {f'{self.cycle}':>10s}", "light_magenta")
        cprint(f"   HEALTH {f'{self.health} / {self.max_health}':>10s}   SHIELD {f'{self.shield} / {self.max_shield}':>10s}", "light_red")
        cprint(f"   ENERGY {f'{self.energy} / {self.max_energy}':>10s}     FOOD {f'{self.food}':>10s}", "light_cyan")
        cprint(f"   DAMAGE {f'{self.damage}':>10s}  CREDITS {f'[c] {self.credits}':>10s}", "light_green")
        cprint("="*45)
        input()

    def calc_resources(self):
        travel_dist = random.randint(6, 20)
        energy_used =  floor(travel_dist * 0.5)
        food_consumed = floor(travel_dist * 0.8)
        self.distance += travel_dist
        self.food -= food_consumed
        self.energy -= energy_used
        return {
            "travel_dist": travel_dist + (self.distance - self.distancebefore),
            "food_consumed": food_consumed + (self.energybefore - self.energy),
            "energy_used": energy_used + (self.foodbefore - self.food),
        }
    
    def random_event(self):
        clearc()
        self.energybefore = self.energy
        self.foodbefore = self.food
        self.distancebefore = self.distance
        random.choice(events_list_1)(self)