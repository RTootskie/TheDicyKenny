import logging

from discord.ext import commands
from replit import db
from resources.players import main_game, players

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./logs/database_functionalities.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def add_total_rolls_to_database(dice_database_to_add, playername, d100_database_to_add=None):
  """Using the parameters add the diceroll to the correct database and under the correct player"""
  dice_database_to_add["total_rolls"] += 1
  if playername in players:
    dice_database_to_add["players"][playername]["total_rolls"] += 1
  if d100_database_to_add:
    d100_database_to_add["total_rolls"] += 1
    if playername in players:
      d100_database_to_add["players"][playername]["total_rolls"] += 1

def add_d100_highlow_rolls_to_database(dice_database_to_add, diceroll, playername, d100_database_to_add=None):
  """Using parameters add the currently performed dice roll to the correct database and under the correct player"""
  if diceroll > 95:
    dice_database_to_add["max_rolls"] += 1
    if playername in players:
      dice_database_to_add["players"][playername]["high_ended_rolls"] += 1
  elif diceroll < 6:
    dice_database_to_add["min_rolls"] += 1
    if playername in players:
      dice_database_to_add["players"][playername]["low_ended_rolls"] += 1
  if d100_database_to_add:
    if diceroll > 95:
      d100_database_to_add["high_ended_rolls"] += 1
    if playername in players:
      d100_database_to_add["players"][playername]["high_ended_rolls"] += 1
    elif diceroll < 6:
      d100_database_to_add["low_ended_rolls"] += 1
      if playername in players:
        d100_database_to_add["players"][playername]["low_ended_rolls"] += 1

def add_highlow_rolls_to_database(dice_database_to_add, diceroll, dicesize, playername):
  """Using parameters add the currently performed dice roll to the correct database and under the correct player"""
  if min(1, dicesize) == diceroll:
    dice_database_to_add["max_rolls"] += 1
    if playername in players:
      dice_database_to_add["players"][playername]["high_ended_rolls"] += 1
  elif max(1, dicesize) == diceroll:
    dice_database_to_add["min_rolls"] += 1
    if playername in players:
      dice_database_to_add["players"][playername]["low_ended_rolls"] += 1

class DiceData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print("Cog database loaded")

    @commands.command(aliases=["STATS","stats", "statistics"])
    async def _statistics(self, ctx, target="None"):
      """Gives you an overview of the D100 rolls inside the database. Usage: *statistics [None,All,Specific Player] Will need to use Discord name. None- Global results, All- Global and Players, Specifc Player - Only the player's results"""
      total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"]
      high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"]
      low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"]

      if target == "None":
        message = f"You have all rolled a total of **{total_rolls}** D100s.\nYou have all rolled a total of **{high_ended}** high open enders.\nYou have all rolled a total of **{low_ended}** low open enders.\n"
      elif target == "All" or target == "all":
        message = f"You have all rolled a total of **{total_rolls}** D100s.\nYou have all rolled a total of **{high_ended}** high open enders.\nYou have all rolled a total of **{low_ended}** low open enders.\n"
        for name in main_game:
          player_total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["total_rolls"]
          player_high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["high_ended_rolls"]
          player_low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["low_ended_rolls"]

          message += f"\t**{name}**:\n"
          message += f"\t\t*Total rolls*: {player_total_rolls}\n\t\t*High rolls*: {player_high_ended}\n\t\t*Low rolls*: {player_low_ended}\n"
      else:
        if target in players:
          player_total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][target]["total_rolls"]
          player_high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][target]["high_ended_rolls"]
          player_low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][target]["low_ended_rolls"]

          message = f"\t**{target}**:\n"
          message += f"\t\t*Total rolls*: {player_total_rolls}\n\t\t*High rolls*: {player_high_ended}\n\t\t*Low rolls*: {player_low_ended}\n"
        else:
          message = "That player does not exist in our database."
      
      await ctx.send(ctx.message.author.mention +f"\n{message}")
    


    @commands.command(aliases=["allrolls","alldice"])
    async def _alldice(self, ctx, target="None"):
      """Gives you an overview of the dice rolls inside the database. Usage: *statistics [None,All,Specific Player] Will need to use Discord name. None- Global results, All- Global and Players, Specifc Player - Only the player's results"""
      total_rolls = db[f"{ctx.guild.id}_dice_rolls"]["total_rolls"]
      high_ended = db[f"{ctx.guild.id}_dice_rolls"]["max_rolls"]
      low_ended = db[f"{ctx.guild.id}_dice_rolls"]["min_rolls"]

      if target == "None":
        message = f"You have all rolled a total of **{total_rolls}** dice.\nYou have all rolled a total of **{high_ended}** high results.\nYou have all rolled a total of **{low_ended}** minimum results.\n"
      elif target == "All" or target == "all":
        message = f"You have all rolled a total of **{total_rolls}** dice.\nYou have all rolled a total of **{high_ended}** high results.\nYou have all rolled a total of **{low_ended}** minimum results.\n"
        for name in main_game:
          player_total_rolls = db[f"{ctx.guild.id}_dice_rolls"]["players"][name]["total_rolls"]
          player_high_ended = db[f"{ctx.guild.id}_dice_rolls"]["players"][name]["high_ended_rolls"]
          player_low_ended = db[f"{ctx.guild.id}_dice_rolls"]["players"][name]["low_ended_rolls"]

          message += f"\t**{name}**:\n"
          message += f"\t\t*Total rolls*: {player_total_rolls}\n\t\t*High rolls*: {player_high_ended}\n\t\t*Low rolls*: {player_low_ended}\n"
      else:
        if target in players:
          player_total_rolls = db[f"{ctx.guild.id}_dice_rolls"]["players"][target]["total_rolls"]
          player_high_ended = db[f"{ctx.guild.id}_dice_rolls"]["players"][target]["high_ended_rolls"]
          player_low_ended = db[f"{ctx.guild.id}_dice_rolls"]["players"][target]["low_ended_rolls"]

          message = f"\t**{target}**:\n"
          message += f"\t\t*Total rolls*: {player_total_rolls}\n\t\t*High rolls*: {player_high_ended}\n\t\t*Low rolls*: {player_low_ended}\n"
        else:
          message = "That player does not exist in our database."

      await ctx.send(ctx.message.author.mention +f"\n{message}")

def setup(bot):
    bot.add_cog(DiceData(bot))
