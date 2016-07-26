# coding=utf-8
#
import json
import logging
import os
from datetime import date
import requests
from modules import bench, teams, stats, rosters, players
__author__ = 'sroche0@gmail.com'


class Client(bench.Bench):
    def __init__(self, league=False, verbose=False):
        bench.Bench.__init__(self)
        self.verbose = verbose
        self.app_path = os.path.expanduser('~/.mfl-pyapi/')
        self.application_init()
        self.logging_init()
        self.league = league
        self.player = players.Players()
        self.team = teams.Teams()
        self.roster = rosters.Rosters()
        self.stat = stats.Stats()
        self.update_data_cache()

    def update_data_cache(self):
        """
        Gets called as part of __init__() and checks if the cached data needs to be updated
        """
        if date.fromtimestamp(os.path.getmtime('{}/player_data.json'.format(self.app_path))) < date.today():
            tmp_player_data = self.player.list()
            if tmp_player_data['status'] in [200, 302]:
                self.player_data = tmp_player_data
                with open('{}/player_data.json'.format(self.app_path), 'wb') as f:
                    f.write(json.dumps(self.player_data['result'], indent=2, separators=(',', ': ')))

            self.update_connectors()

    def update_connectors(self):
        for module in [self.player, self.team, self.roster, self.stat]:
            module.league = self.league
            module.player_data = self.player_data

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
        if not os.path.exists(self.app_path):
            print 'First time run detected, creating app directory at {}'.format(self.app_path)
            print 'To set default values for future runs, edit config.json in app directory'
            os.makedirs(self.app_path)

        if not os.path.exists('{}/config.json'.format(self.app_path)):
            with open('{}/config.json'.format(self.app_path), 'wb') as f:
                example = {'league_id': '',
                           'team_id': '',
                           'base_url': ''
                           }
                f.write(json.dumps(example, indent=2, separators=(',', ': ')))

        if not os.path.exists('{}/player_data.json'.format(self.app_path)):
            with open('{}/player_data.json'.format(self.app_path), 'wb') as f:
                example = {'players': ''}
                f.write(json.dumps(example, indent=2, separators=(',', ': ')))

    def load_params(self):
        """
        Loads params from config.json
        :return:
        """
        pass
