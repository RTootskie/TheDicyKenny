import os
import d20
import discord
import logging

from replit import db
from discord.ext import commands
#from random import choice, randint
#from itertools import cycle

# Custom imports
from resources.players import players
from resources.dice_functions import dice_bot_logic

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''A Kenny that handles all your dice needs.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='*', description=description, intents=intents)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Brutal mass battle!"))

#('Gnasher', '5028')
# @bot.command()
# async def membertest(ctx, message):
#   totalname = ctx.message.author.name, ctx.message.author.discriminator
#   if str(totalname[0]) == "KennyJohn" and str(totalname[1]) == "8921" :
#     print("This is kenny")
#   else:
#     print("This isn't kenny")

# weapons = [
#   "armfist",
#   "dagger"
# ]

# @bot.command()
# async def attkroll(ctx, weapon: str, armtype: int):
#   if weapon in weapons:
#     print("1+1=2")
#   else:
#     if ctx.message.author.name == "Gnasher":
#       await ctx.send(ctx.message.author.mention+"\nYou typed it wrong probably.")
#     else:
#       await ctx.send(ctx.message.author.mention+"\nThat weapon does not exist in my database.")



#!!  Things to work on !!
#!!  * Create a message constructor so the command r simply goes through the list of results and prints the message accordingly
#!! * Create error message capability - Maybe through a function and a list of errors or array depending on the error type
#!! * Bring over the functionality of the dicebot to the iteration
#!! * Create a new functionality for the dice logic to roll an iteration and add bonuses to each rolls

@bot.command(aliases=["R"])
async def r(ctx, input: str):
  """Rolls a dice in (N)dN format."""
  results_from_logic = dice_bot_logic(input)
  logger.debug(db[f"{ctx.guild.id}_dice_hundred_rolls"])

  if results_from_logic["dice_size"] == 100:

    db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"] += 1
    if ctx.message.author.name in players:
      db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1

    brackets = "("
    for dice_roll in results_from_logic["dice_results"]:

      if dice_roll > 95:
        db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"] += 1
        if ctx.message.author.name in players:
          db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
      elif dice_roll < 6:
        db[f"{ctx.guild.id}_dice_hundred_rolls"]["low_ended_rolls"] += 1
        if ctx.message.author.name in players:
          db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1


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
    if results_from_logic["modifiers"]:
      await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} {brackets} {results_from_logic['modifiers']}\n**Total:** {results_from_logic['roll_total']}")
    else:
      await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} {brackets}\n**Total:** {results_from_logic['roll_total']}")
  else:
    if results_from_logic["modifiers"]:
      await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} {results_from_logic['dice_results']} {results_from_logic['modifiers']}\n**Total:** {results_from_logic['roll_total']}")
    else:
      await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} {results_from_logic['dice_results']}\n**Total:** {results_from_logic['roll_total']}")

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
          db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"] += 1
          if ctx.message.author.name in players:
            db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1
          diceresult_left_side = formatted.split(" (")[1]
          diceresult_right_side = diceresult_left_side.split(") ")[0]
          check_modifier = dice.split(dice_nr)
          if len(check_modifier[1]) > 0:
              before_mods = diceresult_left_side.split(") ")[1]
              modifiers = before_mods.split(" =")[0]

          diceresults = diceresult_right_side.split(", ")
          brackets = "("
          counter = 0
          for dice_roll in diceresults:
              counter += 1
              dice_roll = dice_roll.replace("*","")
              if int(dice_roll) >= 96 or int(dice_roll) <= 5:
                if int(dice_roll) > 95:
                  db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"] += 1
                  if ctx.message.author.name in players:
                    db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
                elif int(dice_roll) < 6:
                  db[f"{ctx.guild.id}_dice_hundred_rolls"]["low_ended_rolls"] += 1
                  if ctx.message.author.name in players:
                    db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1
                # Seperation for readability
                if len(diceresults) > 1 and counter != len(diceresults):
                    brackets += f"**{dice_roll}**, "
                else:
                    brackets += f"**{dice_roll}**"
              else:
                if len(diceresults) > 1 and counter != len(diceresults):
                    brackets += f"{dice_roll}, "
                else:
                    brackets += f"{dice_roll}"
          brackets += ")"
          send_message += f"\n1d{dice_nr} {brackets} {modifiers} = {result.total}"
      else:
          send_message += f"\n{formatted}"
      total_roll += result.total
  send_message += f"\n{total_roll} total"
  await ctx.send(ctx.message.author.mention+f"\n{send_message}")

bot.run(os.getenv('TOKEN'))