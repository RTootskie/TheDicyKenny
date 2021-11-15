import os
import d20
from random import choice, randint
import discord

from replit import db
from discord.ext import commands, tasks
from itertools import cycle

description = '''A Kenny that handles all your dice needs.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='*', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Brutal mass battle!"))

# for filename in os.listdir('./cogs'):
#   if filename.endswith('.py'):
#     bot.load_extension(f'cogs.{filename[:-3]}')

#('Gnasher', '5028')
# @bot.command()
# async def membertest(ctx, message):
#   totalname = ctx.message.author.name, ctx.message.author.discriminator
#   if str(totalname[0]) == "KennyJohn" and str(totalname[1]) == "8921" :
#     print("This is kenny")
#   else:
#     print("This isn't kenny")

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
                            print("You wrote something wrong, recheck my result.")
                continue  # Restart the loop so you don't error
            try:
                modifier_total += int(bonusModifier)
            except ValueError:
                print("You wrote something wrong, recheck my result.")
    return modifier_total

def rolling_dice(size_of_dice, times_to_roll=1):
    """Insert the amount of times you need to roll a certain dice"""
    dice_roller_results = []
    while times_to_roll > 0:
        dice_roller_results.append(randint(1, size_of_dice))
        times_to_roll -= 1
    return dice_roller_results


weapons = [
  "armfist",
  "dagger"
]

@bot.command()
async def attkroll(ctx, weapon: str, armtype: int):
  if weapon in weapons:
    print("1+1=2")
  else:
    if ctx.message.author.name == "Gnasher":
      await ctx.send(ctx.message.author.mention+"\nYou typed it wrong probably.")
    else:
      await ctx.send(ctx.message.author.mention+"\nThat weapon does not exist in my database.")


@bot.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
  responses = ["It is certain.",
  "It is decidedly so.",
  "Without a doubt.",
  "Yes - definitely.",
  "You may rely on it.",
  "As I see it, yes.",
  "Most likely.",
  "Outlook good.",
  "Yes.",
  "Signs point to yes.",
  "Reply hazy, try again.",
  "Ask again later.",
  "Better not tell you now.",
  "Cannot predict now.",
  "Concentrate and ask again.",
  "Don't count on it.",
  "My reply is no.",
  "My sources say no.",
  "Outlook not so good.",
  "Very doubtful.",
  "If your name is James, no."]
  await ctx.send(ctx.message.author.mention+f"\n**Question**: {question}\n**Answer**: {choice(responses)}")


def dice_bot_logic(user_string: str):
    """Roll your dice with the syntax of [num_dice]d[dice_sides][modifiers]"""
    print(f"The person just input: {user_string}")
    # Has the user inserted correct syntax

    if 'd' in user_string:
        # Establish initial split of dice
        split_dice = user_string.split("d")
        print(split_dice)
        dice_size_and_modifiers = split_dice[1]

        # Declare some values that are used for checks if they are filled
        dice_num = None
        pre_modifier = None
        first_modifier = None
        should_take_away = None
        dice_modifiers_string = None
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
            print(f"Total Bonus: {total_modifier_sum}")  # Good for logging
            # capabilities
        else:
            dice_size = int(split_dice[1])

        if dice_num:  # If dice_num exists
            print(dice_num)
            rolled_results = rolling_dice(dice_size, dice_num)
            print(rolled_results)
            roll_total = 0
            for i in rolled_results:
                print(f"Rolled {i}")
                roll_total += i
            if first_modifier:
                roll_total += total_modifier_sum
        else:
            rolled_results = rolling_dice(dice_size)
            print(rolled_results)
            roll_total = 0
            for i in rolled_results:
                print(f"Rolled {i}")
                roll_total += i
            if first_modifier:
                roll_total += total_modifier_sum

        if pre_modifier:
            if should_take_away:
                roll_total = pre_modifier - roll_total
            else:
                roll_total += pre_modifier
            print(f"You rolled a total of: {roll_total}")
        else:
            print(f"You rolled a total of: {roll_total}")

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
        }

        return program_returns
    else:
        print("You didn't put a D")


@bot.command()
async def r(ctx, input: str):
  """Rolls a dice in (N)dN format."""
  results_from_logic = dice_bot_logic(input)

  if results_from_logic["dice_size"] == 100:
    brackets = "("
    for dice_roll in results_from_logic["dice_results"]:
      if int(dice_roll) >= 96 or int(dice_roll) <= 5:
        if len(results_from_logic["dice_results"]) > 1:
            brackets += f"**{dice_roll}**, "
        else:
            brackets += f"**{dice_roll}**"
      else:
        if len(results_from_logic["dice_results"]) > 1:
            brackets += f"{dice_roll}, "
        else:
            brackets += f"{dice_roll}"
    brackets += ")"
    await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} {brackets} {results_from_logic['modifiers']}\n**Total:** {results_from_logic['roll_total']}")
  else:
    await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} {results_from_logic['modifiers']}\n**Total:** {results_from_logic['roll_total']}")

@bot.command()
async def rr(ctx, time: int, dice: str, opt="normal"):
  send_message = f"Rolling {time} times"
  count = int(time)
  total_roll = 0
  while count != 0:
      count -= 1
      rolling = str("1"+dice)
      result = d20.roll(rolling)
      formatted = str(result).replace("`","")
      modifiers = ""

      dice_split = str(result).split("d")
      dice_nr = str(dice_split[1]).split(" (")[0]

      if int(dice_nr) == 100:
          diceresult_left_side = formatted.split(" (")[1]
          diceresult_right_side = diceresult_left_side.split(") ")[0]
          check_modifier = dice.split(dice_nr)
          if len(check_modifier[1]) > 0:
              before_mods = diceresult_left_side.split(") ")[1]
              modifiers = before_mods.split(" =")[0]

          diceresults = diceresult_right_side.split(", ")
          brackets = "("
          counter = 0
          for i in diceresults:
              counter += 1
              i = i.replace("*","")
              if int(i) >= 96 or int(i) <= 5:
                  if len(diceresults) > 1 and counter != len(diceresults):
                      brackets += f"**{i}**, "
                  else:
                      brackets += f"**{i}**"
              else:
                  if len(diceresults) > 1 and counter != len(diceresults):
                      brackets += f"{i}, "
                  else:
                      brackets += f"{i}"
          brackets += ")"
          send_message += f"\n1d{dice_nr} {brackets} {modifiers} = {result.total}"
      else:
          send_message += f"\n{formatted}"
      total_roll += result.total
  send_message += f"\n{total_roll} total"
  await ctx.send(ctx.message.author.mention+f"\n{send_message}")

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

bot.run(os.getenv('TOKEN'))