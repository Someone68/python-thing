from math import floor
import random
import time
from termcolor import cprint
from util import clearc, fprint
from events import select, Program, events_list_1
from util import bar

def exm():
    print("test pased")

example = Program("test", exm, 1)
example2 = Program("test2", exm, 0)


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
        self.programs = [example, example2]

    def is_alive(self):
        return self.energy > 0 and self.food > 0 and self.health > 0
    
    def print_stats(self):
        self.damage = round(self.damage, 2)
        if(self.energy > self.max_energy):
            self.energy = self.max_energy
        cprint("(Press enter to proceed)\n", "light_grey")
        cprint("="*45, "grey")
        header = f"Cycle {self.cycle}"
        cprint(f"{header:^45s}", "light_magenta")
        cprint("="*45, "light_grey")
        if(self.energy < 15):
            cprint("  WARNING: ENERGY CRITICALLY LOW  ", "black", "on_light_red")
        elif(self.energy < 25):
            cprint("  WARNING: ENERGY LOW  ", "light_yellow")
        if(self.shield < 1):
            cprint("  WARNING: SHIELD IS DOWN  ", "black", "on_light_yellow")
        if(self.health < 25):
            cprint("  WARNING: HEALTH CRITICALLY LOW  ", "black", "on_light_red")
        elif(self.health < 50):
            cprint("  WARNING: HEALTH LOW  ", "light_yellow")
        
        cprint(f" STATISTICS: {self.name.upper()}", "light_yellow")
        cprint(f"     DISTANCE {f'{self.distance} / {self.distance_required}':>10s}    CYCLE {f'{self.cycle}':>10s}", "light_magenta")
        cprint(f"       HEALTH {f'{self.health} / {self.max_health}':>10s}   SHIELD {f'{self.shield} / {self.max_shield}':>10s}", "light_red")
        cprint(f"       ENERGY {f'{self.energy} / {self.max_energy}':>10s}     FOOD {f'{self.food}':>10s}", "light_cyan")
        cprint(f" DAMAGE MULTP {f'{self.damage}':>10s}  CREDITS {f'[c] {self.credits}':>10s}", "light_green")
        cprint("="*45)
        input()

    def take_damage(self, damage, cancel_shield=False):
        if(self.shield < 1 or cancel_shield):
            self.health -= damage
        elif(damage > self.shield):
            self.shield = 0
            self.health += self.shield - damage
        else:
            self.shield -= damage

    def calc_resources(self):
        travel_dist = random.randint(6, 20)
        energy_used =  floor(travel_dist * 0.5)
        food_consumed = floor(travel_dist * 0.8)
        self.distance += travel_dist
        self.food -= food_consumed
        self.energy -= energy_used
        return {
            "travel_dist": travel_dist,
            "food_consumed": food_consumed,
            "energy_used": energy_used,
        }
    
    def calcfight(self): # dont look at the variable names
        undertale_thingamajiggy = bar()
        unformulaed_thing = abs(abs(11 - undertale_thingamajiggy) - 11)
        return round(unformulaed_thing * 2.5 * self.damage)
    
    def random_event(self):
        clearc()
        self.energybefore = self.energy
        self.foodbefore = self.food
        self.distancebefore = self.distance
        if(self.energy < 15):
            fprint("The ship's energy is critically low. Do you want to re-reoute to a fuel station, losing distance?", color="light_red", select=True)
            choice = select(["RE-ROUTE", "DO NOT"])
            if(choice == "RE-ROUTE"):
                distance_lost = random.randint(10, 30)
                fprint(f"You decided to re-route to a fuel station, losing {distance_lost} distance.")
                self.distance -= distance_lost
                self.lastevent = 0
                events_list_1[0](self)
                return
            else:
                fprint("You decided to keep going...")
        
        event_chosen = random.choice(events_list_1)
        while event_chosen == self.lastevent:
            event_chosen = random.choice(events_list_1)
        self.lastevent = events_list_1.index(event_chosen)
        event_chosen(self)

