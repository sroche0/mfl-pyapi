from . import bench


class Players(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'players'

    def list(self, details=0, since='', players=''):
        """
        Lists all the players in the league and what teams they are on

        :param details: Set this value to 1 to return complete player details, including player IDs from other sources.
        :param since: Pass a unix timestamp via this parameter to receive only changes to the player database since
                        that time.
        :param players: Pass a list of player ids separated by commas (or just a single player id) to receive back just
                        the info on those players.
        :return:
        """
        if isinstance(players, list):
            players = ','.join(players)

        endpoint = '{}&TYPE=players&DETAILS={}SINCE={}&PLAYERS={}'.format(self.base_url, details, since, players)

        r = self.session.get(endpoint)

        response = self.response_check(r, 'players', 'player')
        return response

    def scores(self, league_id='', week='', year='', players='', position='', status='', rules='', count=''):
        """
        All player scores for a given league/week, including all rostered players as well as all free agents.

        :param league_id: League Id (optional).
        :param week: If the week is specified, it returns the data for that week, otherwise the current week data is
                        returned. If the value is 'YTD', then it returns year-to-date data. If the value is 'AVG',
                        then it returns a weekly average.
        :param year: The year for the data to be returned.
        :param players: Pass a list of player ids separated by commas (or just a single player id) to receive back
                        just the info on those players.
        :param position: Return only players from this position.
        :param status: If set to 'freeagent', returns only players that are fantasy league free agents.
        :param rules: If set, and a league id passed, it re-calculates the fantasy score for each player according to
                        that league's rules. This is only valid when specifying the current year and current week.
        :param count: Limit the result to this many players.

        :return: Requested scores
        """
        if not league_id:
            league_id = self.league_id

        if not year:
            year = self.year

        if isinstance(players, list):
            players = ','.join(players)

        endpoint = '{}&TYPE=playerScores&L={}&W={}&YEAR={}&PLAYERS={}&POSITION={}&STATUS={}&RULES={}&COUNT={}'.format(
            self.base_url,
            league_id,
            week,
            year,
            players,
            position,
            status,
            rules,
            count
        )
        print(endpoint)

        r = self.session.get(endpoint)

        response = self.response_check(r, 'playerScores')
        return response
