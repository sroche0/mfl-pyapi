import mflpyapi
from pprint import pprint

c = mflpyapi.Client()

# c.update_data_cache()
players = c.player.player_scores()
print(players)

for i in players['result']['playerscore']:
    print(i)

# c.roster.league = 60050
# resp = c.roster.get_rosters(12)

# pprint(resp)
