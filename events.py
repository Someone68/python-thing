import time
import random
from termcolor import colored, cprint
from util import tprint, tinput, fprint, finput, clearc, Enemy_Ship
import cutie
import re

def remove_ansi(text):
    ansi_escape = re.compile(r'''
        \x1B   # ESC
        (?:    # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |      # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)

def select(options, caption_indicies=None, cursor_index=0):
    if(caption_indicies):
      return options[cutie.select(
        options,
        deselected_prefix="  ",
        selected_prefix="\x1b[38;5;210m>\x1b[0m ",
        caption_indices=caption_indicies,
        selected_index=cursor_index)]
    else:
      return options[cutie.select(
        options,
        deselected_prefix="  ",
        selected_prefix="\x1b[38;5;210m>\x1b[0m ",
        selected_index=cursor_index)]

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
        fprint("You decided to save energy and pass by the shipwreck.")

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


def wormhole(ship):
    fprint("You found a wormhole. It might speed up the trip, or make it worse. What do you want to do?", select=True)
    choice = select(["ENTER", "MOVE AROUND"])
    if(choice == "ENTER"):
        distance = random.randint(-20, 20)
        energy = random.randint(5, 10)
        fprint("You went through the wormhole...", "light_yellow")
        fprint(f"And traveled {distance}ly. Used {energy} energy.")
        ship.distance += distance
        ship.energy -= energy
    else:
        energy = random.randint(3, 6)
        fprint(f"You avoided the wormhole, but used an extra {energy} energy.")
        ship.energy -= energy

def asteroid_field(ship):
    fprint("You are approaching an asteroid field, which can deal heavy damage to the ship. Do you want to avoid the asteroid field or proceed?", select=True)
    choice = select(["PROCEED", "AVOID"])
    if(choice == "PROCEED"):
        if(random.randint(1,3) == 1):
            fprint("You went through the asteroids like it was nothing! No shield or health damage taken.", "light_green")
        elif(random.randint(1,3) > 1):
            damage_taken = random.randint(10,30)
            fprint(f"You tanked some hits from the asteroids. Ship took {damage_taken} damage.", "light_yellow")
            ship.take_damage(damage_taken)
        else:
            damage_taken = random.randint(30,60)
            fprint(f"You took heavy damage from the asteroids. {damage_taken} damage taken.", "light_red")
            ship.take_damage(damage_taken)
    else:
        energy_use = random.randint(8,14)
        fprint(f"You avoided the asteroid field, but used {energy_use} energy.")


def food_station(ship):
    fprint("You arrived at a food station. You can buy food for credits or just continue.", color="light_yellow",select=True)
    choice = select(["BUY", "CONTINUE"])
    if(choice == "BUY"):
        food_costs = {
            "x10": 5,
            "x20": 10,
            "x60": 25,
            "x100": 40,
            "x200": 65
        }
        while True:
          clearc()
          buy = select([f"\x1b[38;5;228m[c] {ship.credits} | BUYING FOOD",
                      "\x1b[38;5;196mx10 FOOD  | [c] 5",
                      "\x1b[38;5;216mx20 FOOD  | [c] 10",
                      "\x1b[38;5;214mx60 FOOD  | [c] 25 BONUS -5",
                      "\x1b[38;5;226mx100 FOOD | [c] 40 BONUS -10",
                      "\x1b[38;5;154mx200 FOOD | [c] 65 BONUS -15",
                      "\x1b[38;5;189mEXIT\x1b[0m"], [0], 1)
          cost = food_costs[remove_ansi(buy).split(" ")[0]] if remove_ansi(buy) != "EXIT" else None
          if(remove_ansi(buy) == "EXIT"):
              fprint("Leaving...",clear=False)
              break
          if(ship.credits >= cost):
              ship.credits -= cost
              ship.food += int(remove_ansi(buy).split(" ")[0].replace("x", ""))
              fprint("Bought. Do you want to buy anything else or exit?", color="light_green", clear=False, select=True)
              if(select(["BUY", "EXIT"]) == "NO"):
                  break
          else:
              fprint("Not enough credits!", color="light_red", clear=False)

def fight_begin(ship, enemy):
    player_turn = True
    while ship.health > 0 and ship.energy > 0 and ship.food > 0 and enemy.health > 0:
      clearc()
      print("---")
      print(colored(f"SHIELD: {ship.shield} / {ship.max_shield}", "light_blue") + " | ", colored(f"ENEMY SHIELD: {enemy.shield} / {enemy.max_shield}", "light_green"))
      print(colored(f"HEALTH: {ship.health} / {ship.max_health}", "light_red") + " | ", colored(f"ENEMY HEALTH: {enemy.health} / {enemy.max_health}", "light_yellow"))
      if(player_turn):
        fprint("It's your turn.", "light_magenta", False, select=True)
        choice = select(["FIGHT", "PROGRAM", "FLEE"])
        if(choice == "FIGHT"):
            clearc()
            power = ship.calcfight()
            fprint(("PERFECT HIT!" if power == round(ship.damage * 2.5 * 11) else ("SOLID HIT!" if round(power >= ship.damage * 2.5 * 9) else "Regular Hit.")) + f" Dealt {power} damage to the enemy ship.")
            if(enemy.shield < 1):
                enemy.health -= power
            elif(power >= enemy.shield):
                fprint("ENEMY SHIELD IS DOWN!", clear=False, color="light_green")
                enemy.shield = 0
                enemy.health += enemy.shield - power
            else:
                enemy.shield -= power
        elif(choice == "PROGRAM"):
            if(len(ship.programs) > 0):
              fprint("Choose a program to run:")
              run = select(list(map(lambda x: colored(x.name, "light_magenta" if x.times_used <= x.uses else "dark_grey"), ship.programs)))
              print("wip")

        else:
            energy_use = random.randint(15,25)
            fprint(f"You fled from the battle, using {energy_use} energy.")
            ship.energy -= energy_use
            break
      else:
          damage_taken = enemy.damage * 2 + random.randint(-8,8)
          print()
          fprint("It's the enemy turn.", color="light_red", select=True, clear=False)
          print()
          fprint(f"The enemy hits you {damage_taken} damage.", clear=False, select=True if ship.shield < 1 else False)
          print()
          ship.take_damage(damage_taken)
          if(ship.shield < 1):
              fprint("CRITICAL: SHIELD IS DOWN!", clear=False, color="light_red")
      player_turn = not player_turn
    if(enemy.health < 1):
        food_gain = random.randint(60,140)
        energy_gain = random.randint(20,40)
        credits_gain = random.randint(60,120)
        fprint(f"Successfully defeated enemy ship! Took {food_gain} food, {energy_gain} fuel, and [c] {credits_gain}.", "light_green")
        ship.food += food_gain
        ship.energy += energy_gain
        ship.credits += credits_gain
        


def enemy_ship(ship):
    fprint("You encountered an enemy ship. Do you want to fight, or try avoiding it?", select=True)
    choice = select(["FIGHT", "AVOID"])
    if(choice == "FIGHT"):
        enemy = Enemy_Ship(random.randint(80,120),random.randint(20,40),random.randint(8,14))
        fprint("You decided to fight the enemy ship.")
        fight_begin(ship, enemy)
    else:
        damage_taken = random.randint(0,20)
        fprint(f"Your ship was hit {damage_taken} while avoiding the enemy ship.")
        ship.take_damage(damage_taken)
    
class Program:
    def __init__(self, name, code, uses) -> None:
        self.name = name
        self.code = code
        self.uses = uses
        self.times_used = 0
    
    def run(self, ship, enemy=None):
        if(self.times_used <= self.uses):
            return self.code(ship, enemy if enemy else None)
        else:
            return None
    
    def install(self, ship):
        if(self in ship.programs):
            return {"message": "ERROR: Already Installed"}
        else:
            ship.programs.append(self)
            time.sleep(random.uniform(1,3))
            return {"message": "SUCCESS"}
        





def repair_station(ship):
    fprint("You arrived at a repair station. You can choose to repair or upgrade your ship. (Shield fully restored.)")
    ship.shield = ship.max_shield
    shop = {
        "repair ship health (x40)": 25,
        "upgrade shield (+15)": 40,
        "upgrade damage multp (+10%)": 35
    }
    choice = select(["REPAIR SHIP HEALTH (x40) | [c] 25", "UPGRADE SHIELD (+15) | [c] 40", "UPGRADE DAMAGE MULTP (+10%) | [c] 35", "INSTALL PROGRAM", "EXIT"])

            


events_list_1 = [fuel, food_station, shipwreck, wormhole, asteroid_field, enemy_ship]