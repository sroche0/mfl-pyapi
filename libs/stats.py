from . import bench


class Stats(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'stats'

    def list(self, team=False, player=False):
        """
        Lists all stats for the current season to date. Can be filtered by team or by player. Default will return stat
        dump for whole league
        :param team: Unique ID of the team to filter for
        :param player: Unique ID of the player to filter for
        :return:
        """

    def get_player_stats(self, player, week=False):
        """
        Lists the stat breakdown by week for a given player. Can also be filtered to only return a specific week or a
        range of weeks

        :param player: Unique ID of the player to filter for
        :param week: Optional. Can be a single week or a range ex: 1-4. If blank will default to season to date
        :return:
        """
