import os
import discord
import logging

from replit import db
from discord.ext import commands

# Custom imports
from resources.dice_functions import dice_bot_logic
from resources.players import players

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./logs/discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='*',
                   description='A Kenny that handles all your dice needs.',
                   intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="Brutal mass battle!"))


# TODO Create a message constructor so the command r simply goes through the list of results and prints the message accordingly
# TODO Create error message capability - Maybe through a function and a list of errors or array depending on the error type
# TODO Bring over the functionality of the dicebot to the iteration
# TODO Create a new functionality for the dice logic to roll an iteration and add bonuses to each rolls
# TODO Make sure that if a modifier has another D then you can roll again.

def add_entries_to_database(dice_roll, size_of_dice, author):
  db["all_dicy_data"]["Dicy_Data"][0] += 1
  if author in players:
    db["all_dicy_data"][author][0] += 1

  #or dice_roll == max(1, size_of_dice)
  #or dice_roll == min(1, size_of_dice)

  if determine_d100(size_of_dice):
    # Add to High Roll and > 60 Roll
    if dice_roll > 95:
        db["all_dicy_data"]["Dicy_Data"][1,2] += 1
        if author in players:
          db["all_dicy_data"][author][1,2] += 1
    # Add to > 60 Roll        
    elif dice_roll >= 60:
      db["all_dicy_data"]["Dicy_Data"][2] += 1
      if author in players:
        db["all_dicy_data"][author][2] += 1
    # Add to <40 Roll
    elif dice_roll <= 40:
      db["all_dicy_data"]["Dicy_Data"][3] += 1
      if author in players:
        db["all_dicy_data"][author][3] += 1
    # Add to Low Roll and <40 Roll
    elif dice_roll < 6:
      db["all_dicy_data"]["Dicy_Data"][3,4] += 1
      if author in players:
        db["all_dicy_data"][author][3,4] += 1

  else:
    if dice_roll == max(1, size_of_dice):
      db["all_dicy_data"]["Dicy_Data"][1] += 1
      if author in players:
        db["all_dicy_data"][author][1] += 1
    elif dice_roll == min(1, size_of_dice):
      db["all_dicy_data"]["Dicy_Data"][4] += 1
      if author in players:
        db["all_dicy_data"][author][4] += 1


def determine_d100(size_of_dice):
    """Takes the input dice and returns true or false"""
    return int(size_of_dice) == 100

# DB Structure
"""
db["all_dicy_data"] = {
  "Dicy_Data": [0,0,0,0,0],
  "temp_account": [0,0,0,0,0],
} # Total Rolls - High Rolls - >60 Rolls - <40 Rolls - Low Rolls 
"""

def dice_are_open_ender(size_of_dice, list_of_dice, author):
    """Receive a list of dice results and decide how they should be formatted."""
    message_variable = ""
    dice_iterator = 0
    for roll_result in list_of_dice:
      add_entries_to_database(roll_result, size_of_dice, author)
      
      dice_iterator += 1
      if determine_d100(size_of_dice):  # Are D100s being rolled
          if int(roll_result) > 95 or int(roll_result) < 6:
              roll_result = f"**{roll_result}**"
      else:
          if int(roll_result) == min(1, size_of_dice) or int(roll_result) == max(1, size_of_dice):
              roll_result = f"**{roll_result}**"

      if int(dice_iterator) == len(list_of_dice):
          message_variable += f"{roll_result}"
      else:
          message_variable += f"{roll_result}, "

    return message_variable


@bot.command(aliases=["R"])
async def r(ctx, user_dice_string: str):
    """Rolls in the (N)dN format."""
    results_from_logic = dice_bot_logic(user_dice_string)
    dice_results = dice_are_open_ender(results_from_logic["dice_size"],
                                       results_from_logic["dice_results"],
                                       ctx.message.author.name)

    if results_from_logic["modifiers"]:
        await ctx.send(
            ctx.message.author.mention +
            f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} "
            + f"({dice_results}) {results_from_logic['modifiers']}\n" +
            f"**Total:** {results_from_logic['roll_total']}")
    else:
        await ctx.send(
            ctx.message.author.mention +
            f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} "
            + f"({dice_results})\n" +
            f"**Total:** {results_from_logic['roll_total']}")


@bot.command(aliases=["RR"])
async def rr(ctx, time: int, dice: str):
    """Rolls N amount of dice in (N) dN format."""
    send_message = f"Rolling {time} times"
    count = int(time)
    total_sum = 0
    while count != 0:
        count -= 1
        results_from_logic = dice_bot_logic(dice)
        dice_results = dice_are_open_ender(results_from_logic["dice_size"],
                                           results_from_logic["dice_results"],
                                           ctx.message.author.name)
        if results_from_logic['modifiers']:
            send_message += f"\n1d{results_from_logic['dice_size']} ({dice_results}) {results_from_logic['modifiers']} = {results_from_logic['roll_total']}"
        else:
            send_message += f"\n1d{results_from_logic['dice_size']} ({dice_results}) = {results_from_logic['roll_total']}"

        total_sum += int(results_from_logic['roll_total'])
    send_message += f"\n{total_sum} total"
    await ctx.send(ctx.message.author.mention + f"\n{send_message}")


# @bot.command(aliases=["database"])
# async def data(ctx):
#   data = total_data
#   await ctx.send(ctx.message.author.mention + f"\n{data}")

bot.run(os.getenv('TOKEN'))
