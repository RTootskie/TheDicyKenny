import os
import random
import discord
from replit import db
from discord.ext import commands
import logging

##### LOGGING ########
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
##### LOGGING ########
description = '''A Kenny that handles all your dice needs.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def r(ctx, dice: str, *opt):
    """Rolls a dice in (N)dN format."""
    params = dice.split('d')
    rolls = None
    roll_and_sub = params[1].split('-')
    roll_and_add = params[1].split('+')

    total = 0
    dice_total = 0
    is_modifier = None
    result = []

    if len(str(params[0])) > 0:
      rolls = int(params[0])

    if '+' in roll_and_sub[0]:
      limit = int(roll_and_add[0])
    else:
      limit = int(roll_and_sub[0])

    split_modifiers = dice.split(str(limit))
    modifiers = split_modifiers[1]

    if not rolls:
        result.append(random.randint(1, limit))
    else:
      for r in range(rolls):
          result.append(random.randint(1, limit))

    if len(str(limit)) == len(str(params[1])):
        is_modifier = False
    else:
        is_modifier = True

    for i in result:
        dice_total += i

    if is_modifier:
        total += dice_total+(eval(modifiers))
    else:
        total = dice_total

    if rolls:
      await ctx.send(ctx.message.author.mention+"\n"+f"**Rolled:** {rolls}d{limit}={result} ({dice_total}) {modifiers}\n**Total:** {total}")
    else:
      if limit == 100:
        if result[0] > 95 or result[0] < 5:
          await ctx.send(ctx.message.author.mention+"\n"+f"**Rolled:** __1d{limit}=**{result}**__ {modifiers}\n**Total:** {total}")
        else:
          await ctx.send(ctx.message.author.mention+"\n"+f"**Rolled:** 1d{limit}={result} {modifiers}\n**Total:** {total}")
      else:
          await ctx.send(ctx.message.author.mention+"\n"+f"**Rolled:** 1d{limit}={result} {modifiers}\n**Total:** {total}")

@bot.command()
async def rr(ctx, time: int, dice: str, *opt):
  """Rolls N amount of N-sided dice"""
  params = dice.split('d')
  rolls = time
  roll_and_sub = params[1].split('-')
  roll_and_add = params[1].split('+')

  total = 0
  is_modifier = None
  result = []

  if '+' in roll_and_sub[0]:
    limit = int(roll_and_add[0])
  else:
    limit = int(roll_and_sub[0])

  split_modifiers = dice.split(str(limit))
  modifiers = split_modifiers[1]

  while rolls != 0:
    result.append(random.randint(1, limit))
    rolls -= 1

  if len(str(limit)) == len(str(params[1])):
      is_modifier = False
  else:
      is_modifier = True

  send_message = f"Rolling {time} times.\n"
  for i in result:
    current_value = 0
    current_value += i
    if is_modifier:
      current_value += eval(modifiers)
      if limit == 100:
        if int(i) > 95 or int(i) < 5:
          quote = f"__1d{limit} (**{i}**) {modifiers} = {current_value}__\n"
        else:
          quote = f"1d{limit} ({i}) {modifiers} = {current_value}\n"
      else:
        quote = f"1d{limit} ({i}) {modifiers} = {current_value}\n"
      send_message += quote
    else:
      if limit == 100:
        if i > 95 or i < 5:
          quote = f"__1d{limit} (**{i}**) = {current_value}__\n"
        else:
          quote = f"1d{limit} ({i}) = {current_value}\n"
      else:
        quote = f"1d{limit} ({i}) = {current_value}\n"
      send_message += quote
    total += current_value

  await ctx.send(ctx.message.author.mention+"\n"+send_message+f"{total} total.")

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