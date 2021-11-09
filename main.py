import os
import random
import discord
import d20
from replit import db
from discord.ext import commands

description = '''A Kenny that handles all your dice needs.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='*', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="James be an absolute hero! <3"))

@bot.command()
async def r(ctx, input: str, opt="normal"):
  """Rolls a dice in (N)dN format."""
  result = d20.roll(input)
  formatted = str(result).replace("`","")
  modifiers = ""

  dice_split = str(result).split("d")
  dice_amt = str(dice_split[0])
  dice_nr = str(dice_split[1]).split(" (")[0]

  if int(dice_nr) == 100:
    diceresult_left_side = formatted.split(" (")[1]
    diceresult_right_side = diceresult_left_side.split(") ")[0]
    check_modifier = input.split(dice_nr)
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
    await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {dice_amt}d{dice_nr} {brackets} {modifiers}\n**Total:** {result.total}")
  else:
    formatted = formatted.replace(" = ","\n**Total:** ")
    await ctx.send(ctx.message.author.mention+f"\n**Rolled:** {formatted}")

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