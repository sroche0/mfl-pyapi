from . import bench


class Players(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'players'

    def dump_player_data(self, details=0, since='', players=''):
        """
        Lists all the players in the league and what teams they are on

        :param details: Set this value to 1 to return complete player details, including player IDs from other sources.
        :param since: Pass a unix timestamp via this parameter to receive only changes to the player database since that time.
        :param players: Pass a list of player ids separated by commas (or just a single player id) to receive back just the info on those players.
        :return:
        """
        endpoint = '{}&TYPE=players&DETAILS={}SINCE={}&PLAYERS={}'.format(self.base_url, details, since, players)

        r = self.session.get(endpoint)

        response = self.response_check(r, 'players', 'player')
        return response
