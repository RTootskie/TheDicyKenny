from discord.ext import commands
from random import randint

class FateDice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print("Cog fatedice loaded")

    @commands.command(aliases=["fate"])
    async def _fate(self, ctx, modifier=None):
      """Rolls a set of fate dice"""
      roll_results = []      
      fate_ladder = {
        -7:"WTF!!!",
        -6:"Oh no!",
        -5:"Abysmal",
        -4:"Tragic",
        -3:"Awful",
        -2:"Terrible",
        -1:"Poor",
        0:"Mediocre",
        1:"Average",
        2:"Fair",
        3:"Good",
        4:"Great",
        5:"Superb",
        6:"Fantastic",
        7:"Epic",
        8:"Legendary",
        9:"Heroic",
        10:"Mythic",
        11:"Divine",
        12:"Godlike",
        15:"Hacker"
      }
      for dice in range(1, 5):
        roll_results.append(randint(1,6))

      roll_total = 0
      fate_roll_results = ""
      for fate_result in roll_results:
        if fate_result in range(1, 3):
          roll_total -= 1
          fate_roll_results += "[-] "
        elif fate_result in range(3, 5):
          fate_roll_results += "[  ] "
        elif fate_result in range(5, 7):
          roll_total += 1
          fate_roll_results += "[+] "
        else:
          print("Something went wrong")
      fate_roll_results.strip()
      if modifier:
        if "-" in modifier:
          split_modifier = modifier.split("-")
          correct_value = split_modifier[1]
          modified_roll_total = roll_total - int(correct_value)
        elif "+" in modifier:
          split_modifier = modifier.split("+")
          correct_value = split_modifier[1]
          modified_roll_total = roll_total + int(correct_value)

      if modifier:
        if modified_roll_total < -7:
          modified_roll_total = -7
        elif modified_roll_total > 12 and modified_roll_total != 15:
          modified_roll_total = 12

      if not modifier:
        await ctx.send(ctx.message.author.mention + f"\nYou got **{fate_ladder[roll_total]}** ({roll_total})\nYou rolled: {fate_roll_results}")
      else:
        if "-" in modifier:
          await ctx.send(ctx.message.author.mention + f"\nYou got **{fate_ladder[modified_roll_total]}** ({modified_roll_total})\nYou rolled: {fate_roll_results} -{correct_value}")
        elif "+" in modifier:
          await ctx.send(ctx.message.author.mention + f"\nYou got **{fate_ladder[modified_roll_total]}** ({modified_roll_total})\nYou rolled: {fate_roll_results} +{correct_value}")

def setup(bot):
    bot.add_cog(FateDice(bot))