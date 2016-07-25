import bench


class Rosters(bench.Bench):
    def __init__(self, league):
        bench.Bench.__init__(self)
        self.league = league

    def get_rosters_by_week(self, team=False, week=False):
        """
        Will return the starting roster and bench players by week of the season so far. Can be filterd to only return a
        specific and to a specific week or week range

        :param team: Unique ID of the team to filter
        :param week: Optional. Can be a single week or a range (ex: 1-4). If blank will default to season to date
        :return:
        """