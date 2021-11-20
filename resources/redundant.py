# Commented lines of redundant code to review back on
  # This line is used to initialize the database in a given server
  # db[f"{ctx.guild.id}_dice_hundred_rolls"] = {
  #   "total_rolls": 0,
  #   "high_ended_rolls": 0,
  #   "low_ended_rolls": 0,
  #   "players": {
  #     "test_player": {
  #       "total_rolls": 0,
  #       "high_ended_rolls": 0,
  #       "low_ended_rolls": 0,
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