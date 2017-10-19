from . import bench


class Players(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'players'

    def list(self):
        """
        Lists all the players in the league and what teams they are on
        :return:
        """
        endpoint = '&TYPE={}'.format(self.type)
        r = self.session.get(self.base_url.format(endpoint))

        response = self.response_check(r, 'players', 'player')
        return response
