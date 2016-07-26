import mflpyapi
from pprint import pprint

c = mflpyapi.Client()

c.roster.league = 60050
resp = c.roster.get_rosters(12)

pprint(resp)
