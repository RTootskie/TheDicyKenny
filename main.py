import os
import discord
import logging
import json
import itertools

from random import randint
from discord.ext import commands

# Custom imports
from resources.dice_functions import dice_bot_logic
from resources.players import players

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Tapasya resting while others fight."))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        success_words = [
            "success",
            "awesome",
            "good",
            "amazing",
            "epic",
            "cool",
        ]
        fail_words = [
            "fail",
            "bad",
            "terrible",
            "horrendus",
            "suicidal"
        ]
        if "backflip" in message.content.lower():
            if any(word in message.content.lower() for word in success_words):
                with open("resources/backflips.json", "r") as f:
                    backflip_database = json.loads(f.read())

                backflip_database["goodflips"] += 1

                with open("resources/backflips.json", "w+") as f:
                    json.dump(backflip_database, f)
                await message.channel.send(message.author.mention +
                                           "\nHe survived???? AGAIN????")
            elif any(word in message.content.lower() for word in fail_words):
                with open("resources/backflips.json", "r") as f:
                    backflip_database = json.loads(f.read())

                backflip_database["badflips"] += 1

                with open("resources/backflips.json", "w+") as f:
                    json.dump(backflip_database, f)
                await message.channel.send(message.author.mention +
                                           "\nHope he can't do them again.")
            else:
                await message.channel.send(message.author.mention +
                                           "\nI don't know if that was a good or a bad one.")
        elif "bad" in message.content.lower():
            await message.channel.send(message.author.mention +
                                       "\nI'm sorry, I've been a baaaaaaaaaaaaad bot. :smiling_imp: ")
        elif "good" in message.content.lower():
            await message.channel.send(message.author.mention +
                                       "\nThank you for the compliment! :blush:")
        elif "fuck you" in message.content.lower():
            await message.channel.send(message.author.mention +
                                       "\nI hope you like low open enders. >:)")
        else:
            await message.channel.send(message.author.mention +
                                       "\nI'm sorry, I haven't been programmed to be that self-aware yet.")

    await bot.process_commands(message)


# TODO Create error message capability - Maybe through a function and a list of errors or array depending on the error type
# TODO Make sure that if a modifier has another D then you can roll again.
# TODO Feature to respond when they are mentioned

def add_entries_to_database(dice_roll, size_of_dice, author):
    """Determine the correct position for new entries and add them to the replit database"""
    with open("resources/database.json", "r") as f:
        player_database = json.loads(f.read())

    #print(sum(map(player_database["KennyJohn"].get, str(range(1, 2+1)))))
    

    if str(dice_roll) not in player_database["Dicy_Data"]:
        player_database["Dicy_Data"][str(dice_roll)] = 0
    ##################################################
    if str(dice_roll) not in player_database[author]:
        player_database[author][str(dice_roll)] = 0

    player_database["Dicy_Data"][str(dice_roll)] += 1
    player_database[author][str(dice_roll)] += 1
    
    
    #print(sum(map(player_database["KennyJohn"].get, range(1, 100+1))))
            

    with open("resources/database.json", "w+") as f:
        json.dump(player_database, f)


def determine_d100(size_of_dice):
    """Takes the input dice and returns true or false"""
    return int(size_of_dice) == 100


def dice_are_open_ender(size_of_dice, list_of_dice, author):
    """Receive a list of dice results and decide how they should be formatted."""
    message_variable = ""
    dice_iterator = 0
    for roll_result in list_of_dice:
        dice_iterator += 1
        if determine_d100(size_of_dice):  # Are D100s being rolled
            if author in players:
                add_entries_to_database(roll_result, size_of_dice, author)
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


@bot.command(aliases=["Real"])
async def real(ctx, modifier=None):
    """Rolls 2d10 as you would in real life."""
    first_dice = randint(0,9)
    sec_dice = randint(0,9)

    if first_dice == 0:
        if sec_dice == 0:
            result = "100"
        else:
            result = "0"+str(sec_dice)
    else:
        result = str(first_dice)+str(sec_dice)

    result = int(result) # Turn the result to int type

    if modifier:
        if "-" in modifier:
            total_mod = int(modifier.split("-")[1])
            had_modifier = "-"
            total_result = result-total_mod
        elif "+" in modifier:
            total_mod = int(modifier.split("+")[1])
            had_modifier = "+"
            total_result = result+total_mod

    if modifier:
        await ctx.send(
                ctx.message.author.mention +
                f"\n**You rolled the dice:** `{str(first_dice)}` and `{str(sec_dice)}`\n"
                +f"This means you rolled: (**{str(result)}**{str(had_modifier)}{str(total_mod)})\n"
                +f"Total: **{str(total_result)}**")
    else:
        await ctx.send(
            ctx.message.author.mention +
            f"\n**You rolled the dice:** `{str(first_dice)}` and `{str(sec_dice)}`\n"
            +f"This means you rolled: (**{str(result)}**)\n"
            +f"Total: **{str(result)}**")

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
    if time <= 50:
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
    else:
        await ctx.send(ctx.message.author.mention + f"\nWoah cowboy, you trying to kill me?")


@bot.command(aliases=["chances"])
async def chance(ctx, chances: int, target: int):
    """Rolls for amount of N chances and reports back how many of those rolls hit the X target"""
    send_message = ""
    # Set count to equal as chances
    count = int(chances)
    total_rolls_hit = 0
    # Set a dictionary to get roll numbers
    roll_numbers = {}
    # While loop until the count is 0
    while count != 0:
        count -= 1
        results_from_logic = dice_bot_logic("d100")
    #######################################################################        
        # Is that dice result (displayed in a list first element) over or equal to the target
        if results_from_logic["dice_results"][0] >= target:
            # Increment the total rolls
            total_rolls_hit += 1
            # Does the key already exist
            if results_from_logic["dice_results"][0] not in roll_numbers:
                # If it doesn't give it a value of 1
                roll_numbers[results_from_logic["dice_results"][0]] = 1
            else:
                # If it does increment it by 1
                roll_numbers[results_from_logic["dice_results"][0]] += 1
    #######################################################################
    
    # Custom send message from the dictionary variable
    for key in reversed(sorted(roll_numbers)):
        send_message += str(key)+": "+str(roll_numbers[key])+"\n"
    
    # Send the message with mentions to the author name
    await ctx.send(ctx.message.author.mention +
                   f"\n*I will roll {chances} times and see how many match or exceed {target}*\n" +
                   f"Hit Rolls: {total_rolls_hit}" +
                   f"\n{send_message}")

bot.run(os.getenv('TOKEN'))
