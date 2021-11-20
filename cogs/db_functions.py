from discord.ext import commands
from replit import db
from resources.players import main_game

class DiceData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print("Cog database loaded")

    @commands.command(aliases=["listresults","dicerolls","rollings"])
    async def _data(self, ctx):
      """Gives you an overview of the dicerolls inside the database. Usage: *dicerolls """
      total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"]
      high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"]
      low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"]

      message = f'You have all rolled a total of **{total_rolls}** D100s.\n'
      message += f"You have all rolled a total of **{high_ended}** high open enders.\n"
      message += f"You have all rolled a total of **{low_ended}** low open enders.\n"
      for name in main_game:
        player_total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["total_rolls"]
        player_high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["high_ended_rolls"]
        player_low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["low_ended_rolls"]
        
        message += f"\t**{name}**:\n"
        message += f"\t\t**Total rolls**: {player_total_rolls}\n"
        message += f"\t\t**High rolls**: {player_high_ended}\n"
        message += f"\t\t**Low rolls**: {player_low_ended}\n"

      await ctx.send(ctx.message.author.mention +f"\n{message}")


    @commands.command(aliases=["playerresults","playerrolls"])
    async def _playerdata(self, ctx):
      """Gives you an overview of the dicerolls inside the database. Usage: *dicerolls """
      message = "*Player summary*:\n"
      for name in main_game:
        player_total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["total_rolls"]
        player_high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["high_ended_rolls"]
        player_low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["low_ended_rolls"]
        
        message += f"\t**{name}**:\n"
        message += f"\t\t*Total rolls*: {player_total_rolls}\n"
        message += f"\t\t*High rolls*: {player_high_ended}\n"
        message += f"\t\t*Low rolls*: {player_low_ended}\n"

      await ctx.send(ctx.message.author.mention +f"\n{message}")

def setup(bot):
    bot.add_cog(DiceData(bot))
