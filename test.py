import mflpyapi
from pprint import pprint

c = mflpyapi.Client()

c.update_data_cache()
players = c.player.dump_player_data()

for i in players['result']:
    if i['position'] == 'WR':
        print(sorted(i))

# c.roster.league = 60050
# resp = c.roster.get_rosters(12)

# pprint(resp)
