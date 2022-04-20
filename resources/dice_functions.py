from random import randint

# Necessary for initialization of database key

def calculate_modifiers(modifiers: list):
    modifier_total = 0
    for bonusModifier in modifiers:
        if bonusModifier:  # Make sure that only non-empty chars are used
            if "-" in bonusModifier:  # If it happens there's a - inside
                minus_i = bonusModifier.split("-")[1:]  # Take everything but the first one (So a bonus which is
                # supposed to be positive isn't included)
                if bonusModifier.split("-")[0]:  # If it is a legitimate character
                    pos_i = bonusModifier.split("-")[0]
                    modifier_total += int(pos_i)  # Make sure to add the bonusModifier to modifier_total if it exists
                for negativeModifier in minus_i:  # Loop through the modifiers which are negatives separately
                    if negativeModifier:
                        try:
                            modifier_total -= int(negativeModifier)
                        except ValueError:
                            print("Something wrong in dice rolling modifier")
                continue  # Restart the loop so you don't error
            try:
                modifier_total += int(bonusModifier)
            except ValueError:
                print("Something wrong in dice rolling modifier")
    return modifier_total


def rolling_dice(size_of_dice, times_to_roll=1):
    """Insert the amount of times you need to roll a certain dice"""
    dice_roller_results = []
    while times_to_roll > 0:
        dice_roll = randint(1, size_of_dice)
        dice_roller_results.append(dice_roll)
        times_to_roll -= 1
    return dice_roller_results


def dice_bot_logic(user_string: str):
    """Roll your dice with the syntax of [num_dice]d[dice_sides][modifiers]"""
    if 'd' in user_string:
        # Establish initial split of dice
        split_dice = user_string.split("d")
        dice_size_and_modifiers = split_dice[1]

        # Declare some values that are used for checks if they are filled
        dice_num = None
        pre_modifier = None
        first_modifier = None
        should_take_away = None
        dice_modifiers_string = None
        error_message = None
        total_modifier_sum = 0

        # Did they want multiple dice?
        if split_dice[0]:
            # Do they want a premodifier to the roll
            if "-" in split_dice[0]:
                existing_pre_mod = split_dice[0].split("-")
                pre_modifier = int(existing_pre_mod[0])
                should_take_away = True
                if existing_pre_mod[1]:
                    dice_num = int(existing_pre_mod[1])
            # Maybe its an addition
            elif "+" in split_dice[0]:
                existing_pre_mod = split_dice[0].split("+")
                pre_modifier = int(existing_pre_mod[0])
                should_take_away = False
                if existing_pre_mod[1]:
                    dice_num = int(existing_pre_mod[1])
            # Normal logic without premodifiers
            else:
                dice_num = int(split_dice[0])

        # Have they added modifiers?
        for character in dice_size_and_modifiers:
            if character == "+" or character == "-":
                first_modifier = character
                break

        # Split the dice_size_and_modifiers variable with the correct modifier
        if first_modifier:
            dice_size_amt_split = dice_size_and_modifiers.split(first_modifier, 1)
            # Declare variables for future use
            dice_size = int(dice_size_amt_split[0])
            dice_modifiers_string = str(first_modifier + dice_size_amt_split[1])
            loop_modifiers = dice_modifiers_string.split("+")
            total_modifier_sum = calculate_modifiers(loop_modifiers)
            # capabilities
        else:
            dice_size = int(split_dice[1])

        if dice_num:  # If dice_num exists
            rolled_results = rolling_dice(dice_size, dice_num)
            roll_total = 0
            for i in rolled_results:
                roll_total += i
            if first_modifier:
                roll_total += total_modifier_sum
        else:
            rolled_results = rolling_dice(dice_size)
            roll_total = 0
            for i in rolled_results:
                roll_total += i
            if first_modifier:
                roll_total += total_modifier_sum

        if pre_modifier:
            if should_take_away:
                roll_total = pre_modifier - roll_total
            else:
                roll_total += pre_modifier
            print(f"Rolled total: {roll_total}")
        else:
            print(f"Rolled total: {roll_total}")

        if not dice_num:
            dice_num = 1

        program_returns = {
            "pre_modifier": pre_modifier,
            "negative_pre": should_take_away,
            "dice_num": dice_num,
            "dice_size": dice_size,
            "dice_results": rolled_results,
            "modifiers": dice_modifiers_string,
            "modifier_total": total_modifier_sum,
            "roll_total": roll_total,
            "error_message": error_message
        }

        return program_returns
    else:
        print("Didn't put a D")
