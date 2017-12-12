# coding=utf-8
# Author: sroche0@gmail.com
import requests
import logging
from sys import stdout


class Bench(object):
    def __init__(self):
        self.session = ''
        self.type = ''
        self.player_id = ''
        self.team_id = ''
        self.roster = ''
        self.stat = ''
        self.league_id = ''
        self.host = ''
        self.year = ''
        self.player_data = []
        self.base_url = ''

    @staticmethod
    def display_options(data, msg, narrow=False):
        valid, choice = False, ''
        print('Select one from below:')
        if narrow:
            try:
                for index, value in enumerate(data):
                    print("    {}. {}".format(index+1, value[narrow]))
            except KeyError:
                print('Passed value is not a key. Select from full list')
                for index, value in enumerate(data):
                    print("    {}. {}".format(index+1, value))
        else:
            for index, value in enumerate(data):
                print("    {}. {}".format(index+1, value))

        while not valid:
            try:
                choice = int(eval(input('\nPlease select the {} you would like to use: '.format(msg))))
                if 0 < choice <= len(data):
                    valid = True
                    choice -= 1
                else:
                    print('Please select a valid option between 1 and {}'.format(len(data)))
            except ValueError:
                print("Please enter a number.")

        return data[choice]

    def change_base_url(self):
        pass

    def cache_data(self):
        pass

    @staticmethod
    def status_print(message):
        stdout.write(message.ljust(30, '.'))
        stdout.flush()

    def request_method(self, f):


        pass

