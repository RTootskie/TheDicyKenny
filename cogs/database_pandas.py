import pandas as pd

from table2ascii import table2ascii as t2a

from replit import db
from resources.players import players, main_game
from discord.ext import commands

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
		embedded_table = None
		if target == "None":
			message += "*The global data:*\n"
			message += data["Dicy_Data"].to_string()
		elif target.lower() == "all":
			message += "*The global and player data:*\n"
			values_for_table = []
			
			players_to_list = ["RollType"]
			for player in main_game:
				players_to_list.append(player)

			count = len(db["all_dicy_data"]["Dicy_Data"])
			iteration = 0
			while count > 0:
				temporary_list = []
				for player in main_game:
					temporary_list.append(str(db["all_dicy_data"][player][iteration]))
				iteration += 1
				values_for_table.append(temporary_list)
				count -= 1

			first_column = ["Total Rolls", "High Rolls", ">60 Rolls", "<40 Rolls", "Low Rolls"]

			num_entry = 0
			for list in values_for_table:
				list.insert(0, first_column[num_entry])
				num_entry += 1

			embedded_table = t2a(
														header=players_to_list,
														body=values_for_table,
			)
		else:
			if target in players:
				message += f"*The data of **{target}** rolls*\n"
				message += data[target].to_string()
			else:
				message = "That player does not exist in our database."

		if embedded_table:
			await ctx.send(ctx.message.author.mention+f"\n{message}```{embedded_table}```")
		else:
			await ctx.send(ctx.message.author.mention +f"\n*No table was generated, error in code*")

	@commands.command(aliases=["clear"])
	async def _clear(self, ctx, target="None"):
		"""Clear your dice data"""
		message = ""
		if target == "None":
			message += "*To clear your data add argument **all** to the command*\n"
		elif target.lower() == "all":
			if ctx.message.author.name in players:
				message += "*Your data has been cleared*\n"
				iteration = 0
				for data_values in db["all_dicy_data"][ctx.message.author.name]:
					db["all_dicy_data"]["Dicy_Data"][iteration] -= db["all_dicy_data"][ctx.message.author.name][iteration]
					db["all_dicy_data"][ctx.message.author.name][iteration] = 0
					iteration += 1
			else:
				message += "*There is no data to clear*\n"
		else:
			message = "Invalid target."

		await ctx.send(ctx.message.author.mention +f"\n{message}")

	@commands.command(aliases=["resetdb"])
	async def _resetdb(self, ctx, target="None"):
		"""Clear all dice data"""
		message = ""
		if ctx.message.author.name == "KennyJohn":
			if target == "None":
				message += "*To clear the data add argument **all** to the command*\n"
			elif target.lower() == "all":
					message += "*The data has been cleared*\n"
					for data_values in db["all_dicy_data"]:
						iteration = 0
						for entry_name in db["all_dicy_data"][data_values]:
							db["all_dicy_data"][data_values][iteration] = 0
							iteration += 1
			else:
				message = "Invalid target."
		else:
			message += "**You're not my dad**"

		await ctx.send(ctx.message.author.mention +f"\n{message}")
	

def setup(bot):
    bot.add_cog(DiceData(bot))