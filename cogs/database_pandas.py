import logging
import pandas as pd

from replit import db
from resources.players import players, main_game
from discord.ext import commands

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./logs/database_functionalities.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# Logging

# DB Structure
"""
db["all_dicy_data"] = {
  "Dicy_Data": [0,0,0,0,0],
  "temp_account": [0,0,0,0,0],
} # Total Rolls - High Rolls - >60 Rolls - Low Rolls <40 Rolls
"""
# DB Keys
# print(db.keys())
# print(db["all_dicy_data"])

# Initialize the data from remote database
def generate_local_database():
  total_data = {}
  for data in db["all_dicy_data"]:
    total_data[data] = []
    for sub_data in db["all_dicy_data"][data]:
      total_data[data].append(sub_data)

  df = pd.DataFrame(total_data,
                    index=[
                      "Total Rolls",
                      "High Rolls",
                      ">60 Rolls",
                      "<40 Rolls",
                      "Low Rolls"
                      ])
  return df

class DiceData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print("Cog database loaded")

    @commands.command(aliases=["database","db","data"])
    async def _data(self, ctx, target="None"):
      """Gives you an overview of the dice rolls inside the database. Usage: *statistics [None,All,Specific Player] Will need to use Discord name. None- Global results, All- Global and Players, Specifc Player - Only the player's results"""

      data = generate_local_database()
      message = ""
      if target == "None":
        message += "*The global data:*\n"
        message += data["Dicy_Data"].to_string()
        print(data["Dicy_Data"].to_string())
      elif target.lower() == "all":
        message += "*The global and player data:*\n"
        players_to_list = ['Dicy_Data']
        for player in main_game:
          players_to_list.append(player)

        message += data[players_to_list].to_string()
        print(data[players_to_list].to_string())
      else:
        if target in players:
          message += f"*The data of **{target}** rolls*\n"
          message += data[target].to_string()
          print(data[target].to_string())
        else:
          message = "That player does not exist in our database."

      await ctx.send(ctx.message.author.mention +f"\n{message}")

def setup(bot):
    bot.add_cog(DiceData(bot))