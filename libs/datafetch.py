from . import bench
import logging


class Players(bench.Bench):
    def __init__(self):
        bench.Bench.__init__(self)
        self.type = 'players'

    def response_check(self, requests_obj, *args):
        result = {
            'status': requests_obj.status_code,
            'http_code': requests_obj.status_code,
            'headers': requests_obj.headers
        }
        logging.debug('status_code = {}'.format(result['status']))
        try:
            message = requests_obj.json()
            if 'error' in list(message.keys()):
                logging.debug('Error found in response keys:')
                logging.debug(message)
                message = message['error']
            else:
                if args:
                    try:
                        for arg in args:
                            message = message[arg]
                    except KeyError:
                        logging.error('Expected key not present in response')
                        logging.debug('Keys in response json are: {}'.format(message.keys()))
                        result['status'] = 500
        except ValueError:
            logging.error('Unable to get json from  response')
            logging.debug(requests_obj.text)
            result['status'] = 500
            message = requests_obj.text

        result['result'] = message
        return result

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
        
        params = {
            'TYPE': 'players',
            'DETAILS': details,
            'SINCE': since,
            'PLAYERS': players,
            'JSON': '1'
        }

        r = self.session.get(self.base_url, params=params)

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

        params = {
            'TYPE': 'playerScores',
            'L': league_id,
            'W': week,
            'YEAR': year,
            'PLAYERS': players,
            'POSITION': position,
            'STATUS': status,
            'RULES': rules,
            'COUNT': count,
            'JSON': '1'
        }

        r = self.session.get(self.base_url, params=params)

        response = self.response_check(r, 'playerScores', 'playerScore')
        return response

    def injuries(self, week=''):
        """
        The player ID, status (IR, Out, Questionable, Doubtful, Probable) and details (i.e., 'Knee', 'Foot', 'Ribs',
        etc.) of all players on the official NFL injury report.

        :param week: If the week is not specified, it defaults to the most recent week that injury data is available.
        :return:
        """
        params = {
            'TYPE': 'injuries',
            'W': week,
            'JSON': '1'
        }

        r = self.session.get(self.base_url, params=params)

        response = self.response_check(r, 'injuries', 'injury')
        response['result'] = [response['result'][x] for x in response['result']]
        return response

    def adp(self, days, time, franchises, is_ppr, is_keeper, is_mock, injured, cutoff, details):
        """
        :param days: This returns draft data from the past number of days specified by this parameter.
                        Valid values are 1, 7, 14 and 30.
        :param time: This returns draft data since the start of the closest 2-week intervale to the specified
                        unix time. These intervals are the ones listed in the ADP Report. If both the DAYS and TIME
                        arguments are passed, TIME takes precedence.
        :param franchises: This returns draft data from just leagues with this number of franchises.
                            Valid values are 8, 10, 12, 14 or 16. If the value is 8, it returns data from leagues with
                            8 or less franchises. If the value is 16 it returns data from leagues with 16 or more
                            franchises.
        :param is_ppr: Filters the data returned as follows: If set to 0, data is from leagues that not use a PPR
                        scoring system; if set to 1, only from PPR scoring system; if set to -1 (or not set), all
                        leagues.
        :param is_keeper: Filters the draft data returns as follows: If set to 0, redrafts leagues only; if set to 1,
                            keeper leagues only; if set to 2, rookie-only drafts; if set to 3, MFL Public Leagues.
                            Default is 0.
        :param is_mock: If set to 1, returns data from mock draft leagues only. If set to 0, excludes data from mock
                        draft leagues. If set to -1, returns all
        :param injured: If set to 1, it includes players that are injured. If not set or set to 0, it excludes
                        injured players.
        :param cutoff: Only returns data for players selected in at least this ppercentage of drafts.
                        So if you pass 10, it means that players selected in less than 10% of all drafts will not be
                        returned. Note that if the value is less than 5, the results may be unpredicatble.
        :param details: If set to 1, it returns the leagues that were included in the results.

        :return:
        """
        params = {
            'TYPE': 'adp',
            'DAYS': days,
            'TIME': time,
            'FRANCHISES': franchises,
            'IS_PPR': is_ppr,
            'IS_KEEPER': is_keeper,
            'IS_MOCK': is_mock,
            'INJURED': injured,
            'CUTOFF': cutoff,
            'DETAILS': details,
            'JSON': '1'
        }

        r = self.session.get(self.base_url, params=params)

        response = self.response_check(r, 'adp', 'player')
        response['result'] = [response['result'][x] for x in response['result']]
        return response

    def top_adds(self, week=''):
        """
        The most-added players across all MyFantasyLeague.com-hosted leagues, as well as the percentage of leagues that
        they've been added in. Only players that have been added in more than 2% of our leagues will be displayed.

        :param week: If the week is specified, it returns the data for that week, otherwise the most current data is
                        returned.
        :return:
        """
        params = {
            'TYPE': 'topAdds',
            'W': week,
            'JSON': '1'
        }

        r = self.session.get(self.base_url, params=params)

        response = self.response_check(r, 'topAdds', 'player')
        response['result'] = [response['result'][x] for x in sorted(response['result'].keys())]
        return response

    def top_drops(self, week=''):
        """
        The most-dropped players across all MyFantasyLeague.com-hosted leagues, as well as the percentage of leagues
        that they've been dropped in. Only players that have been dropped in more than 2% of our leagues will be
        displayed.

        :param week: If the week is specified, it returns the data for that week, otherwise the most current data is
                        returned.
        :return:
        """
        params = {
            'TYPE': 'topDrops',
            'W': week,
            'JSON': '1'
        }

        r = self.session.get(self.base_url, params=params)

        response = self.response_check(r, 'topDrops', 'player')
        response['result'] = [response['result'][x] for x in sorted(response['result'].keys())]
        return response
