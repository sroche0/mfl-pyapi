from . import bench


class Teams(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'teams'

    def list(self):
        """
        Lists all the teams in the league

        :return:
        """
        endpoint = '&TYPE={}'.format(self.type)
        url = self.base_url.format(endpoint)
        r = self.session.get(url)
        response = self.response_check(r, 'rosters', 'franchise')

        return response
