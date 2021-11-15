import discord

from random import choice
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
description = '''A Kenny that handles all your dice needs.'''

bot = commands.Bot(command_prefix='*', description=description, intents=intents)

@bot.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
  responses = ["It is certain.",
  "It is decidedly so.",
  "Without a doubt.",
  "Yes - definitely.",
  "You may rely on it.",
  "As I see it, yes.",
  "Most likely.",
  "Outlook good.",
  "Yes.",
  "Signs point to yes.",
  "Reply hazy, try again.",
  "Ask again later.",
  "Better not tell you now.",
  "Cannot predict now.",
  "Concentrate and ask again.",
  "Don't count on it.",
  "My reply is no.",
  "My sources say no.",
  "Outlook not so good.",
  "Very doubtful.",
  "If your name is James, no."]
  await ctx.send(ctx.message.author.mention+f"\n**Question**: {question}\n**Answer**: {choice(responses)}")