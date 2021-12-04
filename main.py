import os
import discord
import logging

from discord.ext import commands

# Custom imports
from resources.dice_functions import dice_bot_logic

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='*', description='A Kenny that handles all your dice needs.', intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Brutal mass battle!"))


# TODO Create a message constructor so the command r simply goes through the list of results and prints the message accordingly
# TODO Create error message capability - Maybe through a function and a list of errors or array depending on the error type
# TODO Bring over the functionality of the dicebot to the iteration
# TODO Create a new functionality for the dice logic to roll an iteration and add bonuses to each rolls
# TODO Make sure that if a modifier has another D then you can roll again.

def determine_d100(size_of_dice):
    """Takes the input dice and returns true or false"""
    return int(size_of_dice) == 100


def dice_are_open_ender(size_of_dice, list_of_dice):
    """Receive a list of dice results and decide how they should be formatted."""
    message_variable = ""
    dice_iterator = 0
    for roll_result in list_of_dice:
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
    dice_results = dice_are_open_ender(results_from_logic["dice_size"], results_from_logic["dice_results"])

    if results_from_logic["modifiers"]:
        await ctx.send(ctx.message.author.mention +
                       f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} " +
                       f"({dice_results}) {results_from_logic['modifiers']}\n" +
                       f"**Total:** {results_from_logic['roll_total']}")
    else:
        await ctx.send(ctx.message.author.mention +
                       f"\n**Rolled:** {results_from_logic['dice_num']}d{results_from_logic['dice_size']} " +
                       f"({dice_results})\n" +
                       f"**Total:** {results_from_logic['roll_total']}")


@bot.command()
async def rr(ctx, time: int, dice: str):
    """Rolls N amount of dice in (N) dN format."""
    send_message = f"Rolling {time} times"
    count = int(time)
    total_sum = 0
    while count != 0:
        count -= 1
        results_from_logic = dice_bot_logic(dice)
        dice_results = dice_are_open_ender(results_from_logic["dice_size"], results_from_logic["dice_results"])
        if results_from_logic['modifiers']:
            send_message += f"\n1d{results_from_logic['dice_size']} ({dice_results}) {results_from_logic['modifiers']} = {results_from_logic['roll_total']}"
        else:
            send_message += f"\n1d{results_from_logic['dice_size']} ({dice_results}) = {results_from_logic['roll_total']}"

        total_sum += int(results_from_logic['roll_total'])
    send_message += f"\n{total_sum} total"
    await ctx.send(ctx.message.author.mention + f"\n{send_message}")


bot.run(os.getenv('TOKEN'))
