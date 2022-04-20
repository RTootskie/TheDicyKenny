import pandas as pd
import json

from table2ascii import table2ascii as t2a

from resources.players import players, main_game
from discord.ext import commands


class DiceData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog database loaded")

    @commands.command(aliases=["database", "db", "data"])
    async def _data(self, ctx):
        """Gives you an overview of the dice rolls inside the database. Usage: *statistics [None,All,Specific Player] Will need to use Discord name. None- Global results, All- Global and Players, Specifc Player - Only the player's results"""

        message = ""
        embedded_table = None

        message += "*The global and player data:*\n"
        values_for_table = [[], [], [], [], [], [], []]

        players_to_list = []

        for player in main_game:
            players_to_list.append(player)

        with open("resources/database.json", "r") as f:
            player_database = json.loads(f.read())

		
        for player in main_game:
            temporary_list = []
            total_rolls = 0
            high_rolls = 0
            over_sixty_rolls = 0
            middle_rolls = 0
            over_forty_rolls = 0
            low_rolls = 0
            most_rolled = max(player_database[player], key=player_database[player].get)
            for i in player_database[player]:
                # Total Rolls for Player
                total_rolls += player_database[player][i]
                # High Rolls for Player
                if int(i) >= 96:
                    high_rolls += player_database[player][i]
                elif int(i) <= 95 and int(i) >= 60:
                    over_sixty_rolls += player_database[player][i]
                elif int(i) <= 59 and int(i) >= 41:
                    middle_rolls += player_database[player][i]
                elif int(i) <= 40 and int(i) >= 6:
                    over_forty_rolls += player_database[player][i]
                elif int(i) <= 5:
                    low_rolls += player_database[player][i]
            if player == "Ashen":
                total_rolls += 790
                high_rolls += 37
                over_sixty_rolls += 296
                middle_rolls += 110
                over_forty_rolls += 303
                low_rolls += 44
            if player == "Capitan_Scythe":
                total_rolls += 581
                high_rolls += 28
                over_sixty_rolls += 219
                middle_rolls += 75
                over_forty_rolls += 232
                low_rolls += 27
            if player == "Gnasher":
                total_rolls += 137
                high_rolls += 5
                over_sixty_rolls += 54
                middle_rolls += 17
                over_forty_rolls += 55
                low_rolls += 6
            if player == "KennyJohn":
                total_rolls += 695
                high_rolls += 29
                over_sixty_rolls += 258
                middle_rolls += 98
                over_forty_rolls += 272
                low_rolls += 38
            if player == "Sancronis":
                total_rolls += 477
                high_rolls += 24
                over_sixty_rolls += 179
                middle_rolls += 59
                over_forty_rolls += 185
                low_rolls += 30
            if player == "Vidavian":
                total_rolls += 422
                high_rolls += 26
                over_sixty_rolls += 182
                middle_rolls += 40
                over_forty_rolls += 156
                low_rolls += 18
            if player == "Dicy_Data":
                total_rolls += 3102
                high_rolls += 149
                over_sixty_rolls += 1007
                middle_rolls += 580
                over_forty_rolls += 1203
                low_rolls += 163                                                                                
            values_for_table[0].append(total_rolls)
            values_for_table[1].append(high_rolls)
            values_for_table[2].append(over_sixty_rolls)
            values_for_table[3].append(middle_rolls)
            values_for_table[4].append(over_forty_rolls)
            values_for_table[5].append(low_rolls)
            values_for_table[6].append(most_rolled)
        
        players_to_list.insert(0, "RollType")
        values_for_table[0].insert(0, "Total Rolls")
        values_for_table[1].insert(0, "High Rolls")
        values_for_table[2].insert(0, ">60 Rolls")
        values_for_table[3].insert(0, "Middle Rolls")
        values_for_table[4].insert(0, "<40 Rolls")
        values_for_table[5].insert(0, "Low Rolls")
        values_for_table[6].insert(0, "Most Rolled")
        

        embedded_table = t2a(
            header=players_to_list,
            body=values_for_table,
        )

        if embedded_table:
            await ctx.send(ctx.message.author.mention+f"\n{message}```{embedded_table}```")
        else:
            await ctx.send(ctx.message.author.mention + f"\n*No table was generated, error in code*")

def setup(bot):
    bot.add_cog(DiceData(bot))
