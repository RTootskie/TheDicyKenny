# Commented lines of redundant code to review back on
# This line is used to initialize the database in a given server
# db[f"{ctx.guild.id}_dice_rolls"] = {
# "total_rolls": 0,
# "max_rolls": 0,
# "min_rolls": 0,
# "players": {
#   "test_player": {
#     "total_rolls": 0,
#     "high_ended_rolls": 0,
#     "low_ended_rolls": 0,
#     }
#   }
# }

# Create a list of keys with player names for separate tracking
# for name in players:
#   db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name] = {
#     "total_rolls": 0,
#     "high_ended_rolls": 0,
#     "low_ended_rolls": 0
#   }

# @commands.command(aliases=["listresults","dicerolls","rollings"])
# async def _data(self, ctx):
#   """Gives you an overview of the dicerolls inside the database. Usage: *dicerolls """
#   total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"]
#   high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"]
#   low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"]

#   message = f"You have all rolled a total of **{total_rolls}** D100s.\nYou have all rolled a total of **{high_ended}** high open enders.\nYou have all rolled a total of **{low_ended}** low open enders.\n"

#   await ctx.send(ctx.message.author.mention +f"\n{message}")


# @commands.command(aliases=["playerresults","playerrolls"])
# async def _playerdata(self, ctx):
#   """Gives you an overview of the dicerolls inside the database. Usage: *dicerolls """
#   message = "*Player summary*:\n"
#   for name in main_game:
#     player_total_rolls = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["total_rolls"]
#     player_high_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["high_ended_rolls"]
#     player_low_ended = db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][name]["low_ended_rolls"]
    
#     message += f"\t**{name}**:\n"
#     message += f"\t\t*Total rolls*: {player_total_rolls}\n\t\t*High rolls*: {player_high_ended}\n\t\t*Low rolls*: {player_low_ended}\n"

#   await ctx.send(ctx.message.author.mention +f"\n{message}")

        # if min(1, int(dice_nr)) == int(result):
        #   db[f"{ctx.guild.id}_dice_rolls"]["min_rolls"] += 1
        #   if ctx.message.author.name in players:
        #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1
        # elif max(1, int(dice_nr)) == int(result):
        #   db[f"{ctx.guild.id}_dice_rolls"]["max_rolls"] += 1
        #   if ctx.message.author.name in players:
        #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
        # else:
        #   db[f"{ctx.guild.id}_dice_rolls"]["total_rolls"] += 1
        #   if ctx.message.author.name in players:
        #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1


        # db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"] += 1
    # db[f"{ctx.guild.id}_dice_rolls"]["total_rolls"] += 1
    # if ctx.message.author.name in players:
    #   db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1
    #   db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1

          # if dice_roll > 95:
      #   db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"] += 1
      #   db[f"{ctx.guild.id}_dice_rolls"]["max_rolls"] += 1
      #   if ctx.message.author.name in players:
      #     db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
      #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
      # elif dice_roll < 6:
      #   db[f"{ctx.guild.id}_dice_hundred_rolls"]["low_ended_rolls"] += 1
      #   db[f"{ctx.guild.id}_dice_rolls"]["min_rolls"] += 1
      #   if ctx.message.author.name in players:
      #     db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1
      #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1


          # if min(1, results_from_logic["dice_size"]) == dice_roll:
      #   db[f"{ctx.guild.id}_dice_rolls"]["min_rolls"] += 1
      #   if ctx.message.author.name in players:
      #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1
      # elif max(1, results_from_logic["dice_size"]) == dice_roll:
      #   db[f"{ctx.guild.id}_dice_rolls"]["max_rolls"] += 1
      #   if ctx.message.author.name in players:
      #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
      # else:


              # db[f"{ctx.guild.id}_dice_rolls"]["total_rolls"] += 1
        # if ctx.message.author.name in players:
        #   db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1


                  # db[f"{ctx.guild.id}_dice_hundred_rolls"]["total_rolls"] += 1
          # db[f"{ctx.guild.id}_dice_rolls"]["total_rolls"] += 1
          # if ctx.message.author.name in players:
          #   db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1
          #   db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["total_rolls"] += 1



                          # if int(dice_roll) > 95:
                #   db[f"{ctx.guild.id}_dice_hundred_rolls"]["high_ended_rolls"] += 1
                #   db[f"{ctx.guild.id}_dice_rolls"]["max_rolls"] += 1
                #   if ctx.message.author.name in players:
                #     db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
                #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["high_ended_rolls"] += 1
                # elif int(dice_roll) < 6:
                #   db[f"{ctx.guild.id}_dice_hundred_rolls"]["low_ended_rolls"] += 1
                #   db[f"{ctx.guild.id}_dice_rolls"]["min_rolls"] += 1
                #   if ctx.message.author.name in players:
                #     db[f"{ctx.guild.id}_dice_hundred_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1
                #     db[f"{ctx.guild.id}_dice_rolls"]["players"][ctx.message.author.name]["low_ended_rolls"] += 1
                # Seperation for readability