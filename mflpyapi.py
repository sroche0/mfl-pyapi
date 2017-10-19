# coding=utf-8
#
import json
import logging
import os
from datetime import date
import requests
try:
    import keyring
    keyring.get_keyring()
except ImportError:
    import getpass
    keyring = False

from libs import bench, teams, stats, rosters, players
__author__ = 'sroche0@gmail.com'


class Client(bench.Bench):
    def __init__(self, verbose=False, host=None, league_id=None, year=None, username=None, password=None):
        bench.Bench.__init__(self)
        self.verbose = verbose
        self.app_path = os.path.expanduser('~/.mfl-pyapi/')
        self.league_id = league_id
        self.year = year
        self.host = host
        self.team_id = ''
        self.user = username
        self.password = password

        self.application_init()
        self.logging_init()

        self.player = players.Players()
        self.team = teams.Teams()
        self.roster = rosters.Rosters()
        self.stat = stats.Stats()

        self.session = requests.Session()
        self.base_url = 'http://{}/{}/export?&JSON=1&L={}'.format(self.host, self.year, self.league_id)
        self.auth()

        # self.update_data_cache()

    def auth(self):
        """
        authenticates to the API
        :return:
        """
        url = "https://{}/{}/login?USERNAME={}&PASSWORD={}&XML=1".format(self.host, self.year, self.user, self.password)
        r = self.session.get(url)
        response = self.response_check(r)

        self.session.headers.update({"Cookie": r.headers['Set-Cookie']})

        self.sync_connectors()

    def update_data_cache(self):
        """
        Gets called as part of __init__() and checks if the cached data needs to be updated
        """
        if date.fromtimestamp(os.path.getmtime('{}/player_data.json'.format(self.app_path))) < date.today():
            tmp_player_data = self.player.dump_player_data()
            if tmp_player_data['status'] in [200, 302]:
                self.player_data = tmp_player_data
                with open('{}/player_data.json'.format(self.app_path), 'wb') as f:
                    f.write(json.dumps(self.player_data['result'], indent=2, separators=(',', ': ')))

            self.sync_connectors()

    def sync_connectors(self):
        for m in [self.player, self.team, self.roster, self.stat]:
            m.league_id = self.league_id
            m.player_data = self.player_data
            m.session = self.session
            m.year = self.year
            m.league_id = self.league_id
            m.team_id = self.team_id
            m.host = self.host

    def logging_init(self):
        cwd = os.getcwd()

        os.chdir(self.app_path)
        log_files = sorted([x for x in os.listdir('.') if '.log' in x], key=os.path.getctime)

        if len(log_files) > 4:
            os.remove(log_files[0])

        logging.basicConfig(filename='{}.log'.format(date.today()),
                            format="[%(levelname)8s] %(message)s",
                            level=logging.DEBUG
                            )

        logging.info('=' * 80)
        logging.info('New Run'.center(80))
        logging.info('=' * 80)

        os.chdir(cwd)

    def application_init(self):
        """
        Initialize the mfl pyapi application. Check the app directory to load default configs and
        cached data from.

        If this is the first run, or files are missing, create default files for future use.

        :return:
        """

        if not os.path.exists(self.app_path):
            print('First time run detected, creating app directory at {}'.format(self.app_path))
            print('To set default values for future runs, edit config.json in app directory')
            os.makedirs(self.app_path)

        if not os.path.exists('{}/config.json'.format(self.app_path)):
            with open('{}/config.json'.format(self.app_path), 'w') as f:
                config = {'league_id': self.league_id,
                          'team_id': self.team_id,
                          'host': self.host,
                          'year': self.year,
                          'user': self.user
                          }
                json.dump(config, f)

        else:
            with open('{}/config.json'.format(self.app_path), 'r') as f:
                defaults = json.load(f)

            if defaults.get('league_id') and not self.league_id:
                self.league_id = defaults.get('league_id')

            if defaults.get('team_id') and not self.team_id:
                self.team_id = defaults.get('team_id')

            if defaults.get('host') and not self.host:
                self.host = defaults.get('host')

            if defaults.get('year') and not self.year:
                self.year = defaults.get('year')

            if defaults.get('user') and not self.user:
                self.user = defaults.get('user')

            if keyring:
                self.password = keyring.get_password('mfl-pyapi', self.user)
            else:
                self.password = getpass.getpass()

        if os.path.exists('{}/player_data.json'.format(self.app_path)):
            with open('{}/player_data.json'.format(self.app_path), 'r') as f:
                self.player_data = json.load(f)

    def load_params(self):
        """
        Loads params from config.json
        :return:
        """
        pass
