from . import bench


class Rosters(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'rosters'

    def get_rosters(self, team=False, week=''):
        """
        Will return the starting roster and bench players by week of the season so far. Can be filterd to only return a
        specific and to a specific week or week range

        :param team: Unique ID of the team to filter
        :param week: Optional. If blank will default to current week
        :return:
        """
        endpoint = '&TYPE={}&W={}'.format(self.type, week)
        r = self.session.get(self.base_url.format(endpoint))
        response = self.response_check(r, 'rosters', 'franchise')

        if team:
            response['result'] = [x for x in response['result'] if x['id'] == str(team).rjust(4, '0')]

        return response
