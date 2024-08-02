import time
import random
from termcolor import colored, cprint
from util import (
    tprint,
    tinput,
    fprint,
    finput,
    clearc,
    Enemy_Ship,
    show_cursor,
    hide_cursor,
)
import cutie
import re


def remove_ansi(text):
    ansi_escape = re.compile(
        r"""
        \x1B   # ESC
        (?:    # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |      # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    """,
        re.VERBOSE,
    )
    return ansi_escape.sub("", text)


def select(options, caption_indicies=None, cursor_index=0):
    hide_cursor()
    try:
        if caption_indicies:
            return options[
                cutie.select(
                    options,
                    deselected_prefix="  ",
                    selected_prefix="\x1b[38;5;210m>\x1b[0m ",
                    caption_indices=caption_indicies,
                    selected_index=cursor_index,
                )
            ]
        else:
            return options[
                cutie.select(
                    options,
                    deselected_prefix="  ",
                    selected_prefix="\x1b[38;5;210m>\x1b[0m ",
                    selected_index=cursor_index,
                )
            ]
    finally:
        show_cursor()


def shipwreck(ship):
    if ship.cycle == 1:
        cprint("(use arrow keys to select and enter to proceed)", "grey")
    fprint(
        "You noticed a destroyed shipwreck. It may have some useful resources. What do you do?",
        "light_magenta",
        True,
        True,
    )
    choice = select(["EXPLORE", "LEAVE IT"])
    if choice == "EXPLORE":
        energyused = random.randint(3, 6)
        if random.randint(0, 1) == 1:
            fprint(f"You didn't find anything. Used {energyused} energy.", "light_red")
        else:
            creditsearned = random.randint(12, 23)
            foodearned = random.randint(20, 45)
            fprint(
                f"You found {creditsearned} credits and {foodearned} food. Used {energyused} energy."
            )
            ship.food += foodearned
            ship.credits += creditsearned
        ship.energy -= energyused
    else:
        fprint("You decided to save energy and pass by the shipwreck.")


def fuel(ship):
    if ship.cycle == 1:
        cprint("(use arrow keys to select and enter to proceed)", "grey")
    fprint(
        "You arrived at a fuel station, which can refill your energy. Do you want to refill, using 25 food?",
        "light_yellow",
        True,
        True,
    )
    choice = select(["REFILL", "CONTINUE"])
    if choice == "REFILL":
        fprint("You decided to refuel. Keep pressing ENTER to refill energy!")
        start_time = time.time()
        end_time = start_time + 7
        press_count = 0

        while time.time() < end_time:
            clearc()
            input(
                colored(
                    f"REFUELED: {press_count / 2} | PRESS ENTER TO REFUEL > ",
                    "light_yellow",
                )
            )
            press_count += 1

        ship.energy += int(round(press_count / 2))
        if press_count > 0:
            fprint(
                f"Successfully refilled {press_count / 2} energy! Used 25 food.",
                "light_green",
            )
        else:
            fprint(
                f"Unsuccessful! Press enter to refill. Used 25 food.",
                "light_red",
            )
        ship.food -= 25
    else:
        fprint(
            f"You decided to save time and continue. You can always refuel later.",
            "light_yellow",
        )


def wormhole(ship):
    fprint(
        "You found a wormhole. It might speed up the trip, or make it worse. What do you want to do?",
        select=True,
    )
    choice = select(["ENTER", "MOVE AROUND"])
    if choice == "ENTER":
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
    fprint(
        "You are approaching an asteroid field, which can deal heavy damage to the ship. Do you want to avoid the asteroid field or proceed?",
        select=True,
    )
    choice = select(["PROCEED", "AVOID"])
    if choice == "PROCEED":
        if random.randint(1, 3) == 1:
            fprint(
                "You went through the asteroids like it was nothing! No shield or health damage taken.",
                "light_green",
            )
        elif random.randint(1, 3) > 1:
            damage_taken = random.randint(10, 30)
            fprint(
                f"You tanked some hits from the asteroids. Ship took {damage_taken} damage.",
                "light_yellow",
            )
            ship.take_damage(damage_taken)
        else:
            damage_taken = random.randint(30, 60)
            fprint(
                f"You took heavy damage from the asteroids. {damage_taken} damage taken.",
                "light_red",
            )
            ship.take_damage(damage_taken)
    else:
        energy_use = random.randint(8, 14)
        fprint(f"You avoided the asteroid field, but used {energy_use} energy.")


def food_station(ship):
    fprint(
        "You arrived at a food station. You can buy food for credits or just continue.",
        color="light_yellow",
        select=True,
    )
    choice = select(["BUY", "CONTINUE"])
    if choice == "BUY":
        food_costs = {"x10": 5, "x20": 10, "x60": 25, "x100": 40, "x200": 65}
        while True:
            clearc()
            buy = select(
                [
                    f"\x1b[38;5;228m[c] {ship.credits} | BUYING FOOD",
                    "\x1b[38;5;196mx10 FOOD  | [c] 5",
                    "\x1b[38;5;216mx20 FOOD  | [c] 10",
                    "\x1b[38;5;214mx60 FOOD  | [c] 25 BONUS -5",
                    "\x1b[38;5;226mx100 FOOD | [c] 40 BONUS -10",
                    "\x1b[38;5;154mx200 FOOD | [c] 65 BONUS -15",
                    "\x1b[38;5;189mEXIT\x1b[0m",
                ],
                [0],
                1,
            )
            cost = (
                food_costs[remove_ansi(buy).split(" ")[0]]
                if remove_ansi(buy) != "EXIT"
                else None
            )
            if remove_ansi(buy) == "EXIT":
                fprint("Leaving...", clear=False)
                break
            if ship.credits >= cost:
                ship.credits -= cost
                ship.food += int(remove_ansi(buy).split(" ")[0].replace("x", ""))
                fprint(
                    "Bought. Do you want to buy anything else or exit?",
                    color="light_green",
                    clear=False,
                    select=True,
                )
                if select(["BUY", "EXIT"]) == "NO":
                    break
            else:
                fprint("Not enough credits!", color="light_red", clear=False)


def fight_begin(ship, enemy):
    player_turn = True
    while ship.health > 0 and ship.energy > 0 and ship.food > 0 and enemy.health > 0:
        clearc()
        print("---")
        print(
            colored(f"SHIELD: {ship.shield} / {ship.max_shield}", "light_blue") + " | ",
            colored(
                f"ENEMY SHIELD: {enemy.shield} / {enemy.max_shield}", "light_green"
            ),
        )
        print(
            colored(f"HEALTH: {ship.health} / {ship.max_health}", "light_red") + " | ",
            colored(
                f"ENEMY HEALTH: {enemy.health} / {enemy.max_health}", "light_yellow"
            ),
        )
        if player_turn:
            fprint("It's your turn.", "light_magenta", False, select=True)
            choice = select(["FIGHT", "PROGRAM", "FLEE"])
            if choice == "FIGHT":
                clearc()
                power = ship.calcfight()
                fprint(
                    (
                        "PERFECT HIT!"
                        if power == round(ship.damage * 2.5 * 11)
                        else (
                            "SOLID HIT!"
                            if round(power >= ship.damage * 2.5 * 9)
                            else "Regular Hit."
                        )
                    )
                    + f" Dealt {power} damage to the enemy ship."
                )
                enemy.take_damage(power)
                if enemy.shield < 1:
                    fprint("ENEMY SHIELD IS DOWN!", clear=False, color="light_green")
            elif choice == "PROGRAM":
                if len(ship.programs) > 0 and not all(
                    obj.times_used == obj.uses for obj in ship.programs
                ):
                    fprint("Choose a program to run:", select=True)
                    disabled = []
                    for i in ship.programs:
                        if i.times_used >= i.uses:
                            disabled.append(ship.programs.index(i))
                    user_select = select(
                        list(
                            map(
                                lambda x: colored(
                                    "["
                                    + str(
                                        find_item_by_name(x, ship.programs)[1].uses
                                        - find_item_by_name(x, ship.programs)[
                                            1
                                        ].times_used
                                    )
                                    + "] "
                                    + x,
                                    (
                                        "grey"
                                        if find_item_by_name(x, ship.programs)[
                                            1
                                        ].times_used
                                        >= find_item_by_name(x, ship.programs)[1].uses
                                        else "light_yellow"
                                    ),
                                ),
                                sorted(
                                    list(
                                        map(
                                            lambda x: x.name,
                                            ship.programs,
                                        )
                                    ),
                                    key=lambda name: next(
                                        (
                                            obj
                                            for obj in ship.programs
                                            if obj.name == name
                                        ),
                                        None,
                                    ).times_used,
                                ),
                            )
                        ),
                        disabled,
                    )

                    find_item_by_name(
                        remove_ansi(user_select).split("] ")[1], ship.programs
                    )[1].run(ship, enemy)
                elif len(ship.programs) < 1:
                    fprint("No programs installed!")
                else:
                    fprint("No programs are available.")

            else:
                energy_use = random.randint(15, 25)
                success = random.randint(1, 5)
                if success > 3:
                    fprint(f"You fled from the battle, using {energy_use} energy.")
                    ship.energy -= energy_use
                    break
                else:
                    fprint(f"Unsuccessful!")
        else:
            damage_taken = enemy.damage * 2 + random.randint(-8, 8)
            print()
            fprint("It's the enemy turn.", color="light_red", select=True, clear=False)
            print()
            fprint(
                f"The enemy hits you {damage_taken} damage.",
                clear=False,
                select=True if ship.shield < 1 else False,
            )
            print()
            ship.take_damage(damage_taken)
            if ship.shield < 1:
                fprint("CRITICAL: SHIELD IS DOWN!", clear=False, color="light_red")
        player_turn = not player_turn
    if enemy.health < 1:
        food_gain = random.randint(60, 140)
        energy_gain = random.randint(20, 40)
        credits_gain = random.randint(60, 120)
        fprint(
            f"Successfully defeated enemy ship! Took {food_gain} food, {energy_gain} fuel, and [c] {credits_gain}.",
            "light_green",
        )
        ship.food += food_gain
        ship.energy += energy_gain
        ship.credits += credits_gain
    for i in ship.programs:
        i.times_used = 0


def enemy_ship(ship):
    fprint(
        "You encountered an enemy ship. Do you want to fight, or try avoiding it?",
        select=True,
    )
    choice = select(["FIGHT", "AVOID"])
    if choice == "FIGHT":
        enemy = Enemy_Ship(
            random.randint(80, 120), random.randint(20, 40), random.randint(8, 14)
        )
        fprint("You decided to fight the enemy ship.")
        fight_begin(ship, enemy)
    else:
        damage_taken = random.randint(0, 20)
        fprint(f"Your ship was hit {damage_taken} while avoiding the enemy ship.")
        ship.take_damage(damage_taken)


class Program:
    def __init__(self, name, code, uses) -> None:
        self.name = name
        self.code = code
        self.uses = uses
        self.times_used = 0

    def run(self, ship, enemy=None):
        if self.times_used <= self.uses:
            self.times_used += 1
            return self.code(ship, enemy if enemy else None)
        else:
            return None

    def install(self, ship):
        if self in ship.programs:
            return {"message": "ERROR: already installed"}
        else:
            ship.programs.append(self)
            time.sleep(random.uniform(1, 3))
            return {"message": f"Successfully installed module {self.name}"}


def find_item_by_name(name, items):
    for index, item in enumerate(items):
        if item.name == name:
            return index, item
    return None, None


def repair_station(ship):
    fprint(
        "You arrived at a repair station. You can choose to repair or upgrade your ship. (Only one choice!) (Shield fully restored)",
        select=True,
    )
    ship.shield = ship.max_shield
    cprint(f"[c] {ship.credits}", "light_yellow")
    choices = [
        colored("REPAIR SHIP HEALTH (x40) | [c] 25", "light_red"),
        colored("UPGRADE SHIELD (+15) | [c] 40", "light_blue"),
        colored("UPGRADE DAMAGE MULTP (+10%) | [c] 35", "light_yellow"),
        colored("INSTALL PROGRAM", "light_green"),
        colored("EXIT"),
    ]
    choice = select(choices)

    if remove_ansi(choice) == "INSTALL PROGRAM":

        def program_laser(ship, enemy):
            fprint("Running Program: Laser", "yellow", True, False)
            damage_dealt = random.randint(60, 100)
            miss = random.randint(1, 2)
            if miss == 1:
                fprint("Missed!", "red")
            else:
                enemy.take_damage(damage_dealt)
                fprint(f"Hit enemy {damage_dealt}!")

        def program_missle(ship, enemy):
            fprint("Running Program: Missle", "yellow", True, False)
            damage_dealt = random.randint(35, 60)
            miss = random.randint(1, 4)
            if miss == 3:
                fprint("Missed!", "red")
            else:
                enemy.take_damage(damage_dealt)
                fprint(f"Hit enemy {damage_dealt}!")

        def program_self_heal(ship, enemy):
            fprint("Running Program: Self-Heal", "yellow", True, False)
            amount = ship.calcfight()
            ship.heal(amount)
            fprint(f"Successfully healed {amount} HP!", "light_green")

        programs = [
            Program("MISSLE", program_missle, 2),
            Program("LASER", program_laser, 1),
            Program("SELF-HEAL", program_self_heal, 5),
        ]

        fprint("Choose a program to install ([c] 40  each):", select=True)
        install = select(list(map(lambda x: x.name, programs)))
        if ship.credits >= 40:
            ship.credits -= 40
            cprint("Installing...", "light_blue")
            fprint(find_item_by_name(install, programs)[1].install(ship)["message"])
        else:
            fprint("Not enough money.", "red")
    elif remove_ansi(choice) == "REPAIR SHIP HEALTH (x40) | [c] 25":
        if ship.credits >= 25:
            ship.heal(40)
            ship.credits -= 25
            fprint("Repaired 40 health.")
        else:
            fprint("Not enough credits!")
    elif remove_ansi(choice) == "UPGRADE SHIELD (+15) | [c] 40":
        if ship.credits >= 25:
            ship.max_shield += 15
            ship.shield = ship.max_shield
            fprint("Upgraded shield (+15).")
        else:
            fprint("Not enough credits!")
    elif remove_ansi(choice) == "UPGRADE DAMAGE MULTP (+10%) | [c] 35":
        if ship.credits >= 25:
            ship.damage += 0.1
            fprint("Upgraded damage multiplier (+10%).")
        else:
            fprint("Not enough credits!")


class Boss:
    def __init__(self, name, health, defense, damage):
        self.name = name
        self.health = health
        self.defense = defense
        self.max_health = health
        self.max_defense = defense
        self.damage = damage
        self.cycle = 0

    def take_damage(self, power):
        if self.defense < 1:
            self.health -= power
        elif power >= self.defense:
            self.defense = 0
            self.health += self.defense - power
        else:
            self.defense -= power

    def heal(self, amount):
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount


def boss_1(ship):
    enemy = Boss("The Stellar Warden", 300, 170, 10)
    stamina = 100
    phase = 1
    health = 150
    max_health = health
    defending = False
    fprint(
        "You are approaching an abandoned space station. Do you want to explore it, or avoid it and take pictures for scientific purposes?",
        select=True,
    )
    not_really_a_choice = select(["EXPLORE", "AVOID"])
    if not_really_a_choice == "EXPLORE":
        fprint(
            "You slowly enter the abandoned space station, looking for any food or fuel left behind."
        )
        fprint(
            "When you find nothing, you turn around, dissapointed. It's just some space trash and debris."
        )
        fprint(
            "[!] Suddenly, a massive mechanical entity blocks the way. It looks like it's made of metallic alloy and it's absorbing the power of the space station."
        )
        fprint(
            "You turn and run, but to no avail. You pull out your emergency gun, slowing backing away."
        )
    else:
        fprint("You try to avoid the space station, taking pictures from afar.")
        fprint(
            "[!] Suddenly, your ship gets slowly dragged towards the station magentically."
        )
        fprint(
            "When your ship crashes into the space station, metallic alloy pulls the airlock open."
        )
        fprint(
            "A massive mechanical entity slowly approaches you. You pull out your emergency gun, slowing backing away."
        )

    player_turn = True
    while enemy.health > 0 and health > 0 and stamina > -6:
        if phase == 1 and enemy.defense < 50:
            fprint(
                f"Entering phase 2! {enemy.name}'s defense increases! {enemy.name}'s attack decreases!"
            )
            phase = 2
        elif phase == 2 and enemy.defense < 1 and enemy.health < 200:
            fprint(
                f"Entering phase 3! {enemy.name}'s defense and attack greatly increase!"
            )
            phase = 3
        clearc()
        cprint(
            "=" * 40,
            "light_blue" if phase == 1 else ("light_yellow" if phase == 2 else "red"),
        )
        print(
            colored(f"HEALTH: {health} / {max_health}", "light_red")
            + "\n"
            + colored(f"STAMINA: {stamina}", "light_blue")
            + "\n"
        )
        print(
            colored(
                f"ENEMY DEFENSE: {enemy.defense} / {enemy.max_defense}", "light_green"
            ),
        )
        print(
            colored(
                f"ENEMY HEALTH: {enemy.health} / {enemy.max_health}", "light_yellow"
            ),
        )
        if player_turn:
            fprint("It's your turn.", "light_magenta", False, select=True)
            choice = select(["FIGHT", "DEFEND", "STALL"])
            if choice == "FIGHT":
                stamina -= 5
                clearc()
                power = (
                    ship.calcshoot()
                    if phase == 1
                    else (
                        round(ship.calcshoot() * 0.5)
                        if phase == 2
                        else round(ship.calcshoot() * 0.2)
                    )
                )
                fprint(f"Dealt {power} damage to {enemy.name}.")
                enemy.take_damage(power)
                if enemy.defense < 1:
                    fprint(
                        f"{enemy.name}'s DEFENSE IS DOWN!",
                        clear=False,
                        color="light_green",
                    )
            elif choice == "DEFEND":
                if stamina >= 25:
                    fprint("Defending!")
                    stamina -= 10
                    defending = True
                else:
                    fprint("Not enough stamina!")

            else:
                stamina += random.randint(10, 25)
                health += random.randint(10, 20)
                if health > max_health:
                    health = max_health
        else:
            damage_taken = round(
                enemy.damage * 2
                + random.randint(-8, 8)
                * (0.8 if phase == 2 else (1.55 if phase == 3 else 1))
            )
            print()
            fprint("It's the enemy turn.", color="light_red", select=True, clear=False)
            print()
            fprint(
                f"{enemy.name} hits you {damage_taken if not defending else int(round(damage_taken * 0.3))} damage.",
                clear=False,
                select=True if ship.shield < 1 else False,
            )
            print()
            health -= damage_taken if not defending else int(round(damage_taken * 0.75))
            defending = False
        player_turn = not player_turn
    if enemy.health < 1:
        food_gain = random.randint(60, 140)
        energy_gain = random.randint(20, 40)
        credits_gain = random.randint(300, 520)
        fprint(
            f"Successfully defeated {enemy.name}.",
            "light_green",
        )
        fprint(f"You stand there, looking down at the monster you just killed.")
        fprint(
            f"When you blink, the body disappears. The only remains are a few coins lying on the ground."
        )
        fprint(f"You enter your spaceship.")
        bosslevel += 1
        ship.food += food_gain
        ship.energy += energy_gain
        ship.credits += credits_gain
    else:
        ship.health = 0
    for i in ship.programs:
        i.times_used = 0


events_list_1 = [
    fuel,
    food_station,
    shipwreck,
    wormhole,
    asteroid_field,
    enemy_ship,
    repair_station,
    repair_station,
]

events_list_2 = [
    fuel,
    food_station,
]

bosslevel = 0
