# coding=utf-8
#
import json
import logging
import os
import datetime
import requests
# import modules
from modules import bench, teams, stats, rosters, players
__author__ = 'sroche0@gmail.com'


class Client(bench.Bench):
    def __init__(self, verbose=False):
        bench.Bench.__init__(self)
        self.verbose = verbose
        self.app_path = os.path.expanduser('~/.mfl-pyapi/')
        self.application_init()
        self.logging_init()
        self.league = ''
        self.init_connectors()

    def init_connectors(self):
        """
        Gets called as part of set_league() and creates instances of each API connector
        """
        self.player = players.Players(self.league)
        self.team = teams.Teams(self.league)
        self.roster = rosters.Rosters(self.league)
        self.stat = stats.Stats(self.league)

        pass

    def update_connectors(self):
        """
        Gets called as part of auth() to update the session token of all the API Connector instances.
        For the connectors that call functions from other connectors it also updates the instances they reference
        """
        # for module in __all__:
        #     self.module.league = self.league
        #     # Do stuff to connectors
        #     pass

        self.session.headers.update({'X-TOKEN': self.token})

    def logging_init(self):
        cwd = os.getcwd()

        os.chdir(self.app_path)
        log_files = sorted([x for x in os.listdir('.') if '.log' in x], key=os.path.getctime)

        if len(log_files) > 4:
            os.remove(log_files[0])

        logging.basicConfig(filename='{}.log'.format(datetime.date.today()),
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
