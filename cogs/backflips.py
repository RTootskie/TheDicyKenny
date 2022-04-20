from discord.ext import commands
import json


class Backflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog backflip loaded")

    @commands.command(aliases=["backflip", "backflips", "skorost", "speedboi", "speedboy"])
    async def _backflips(self, ctx):
        with open("resources/backflips.json", "r") as f:
            backflip_database = json.loads(f.read())

        successes = ":white_check_mark:  " * backflip_database["goodflips"]
        failures = ":x:  " * backflip_database["badflips"]

        await ctx.send(ctx.message.author.mention +
                    f"\n**Successes**: {successes}\n**Failures**: {failures}")


def setup(bot):
    bot.add_cog(Backflip(bot))
