# coding=utf-8
# Author: sroche0@gmail.com
import requests
import logging
from sys import stdout


class Bench(object):
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'http://www03.myfantasyleague.com/2015/export?&JSON=1&L=60050{}'
        self.type = ''
        self.player = ''
        self.team = ''
        self.roster = ''
        self.stat = ''
        self.league = ''

    @staticmethod
    def display_options(data, msg, narrow=False):
        valid, choice = False, ''
        print 'Possible Regions:'
        if narrow:
            try:
                for index, value in enumerate(data):
                    print "    %s. %s" % (index+1, value[narrow])
            except KeyError:
                print 'Passed value is not a key. Select from full list'
                for index, value in enumerate(data):
                    print "    %s. %s" % (index+1, value)
        else:
            for index, value in enumerate(data):
                print "    %s. %s" % (index+1, value)

        while not valid:
            try:
                choice = int(raw_input('\nPlease select the {} you would like to use: '.format(msg)))
                if 0 < choice <= len(data):
                    valid = True
                    choice -= 1
                else:
                    print 'Please select a valid option between 1 and {}'.format(len(data))
            except ValueError:
                print "Please enter a number."

        return data[choice]

    def response_check(self, requests_obj, *args):
        result = {'status': requests_obj.status_code}
        logging.debug(self.log('status_code = {}'.format(result['status'])))
        try:
            message = requests_obj.json()
            if 'error' in message.keys():
                logging.debug(self.log('Error found in response keys:'))
                logging.debug(message)
                message = message['error']
            else:
                if args:
                    try:
                        for arg in args:
                            message = message[arg]
                    except KeyError:
                        logging.error(self.log('Expected key not present in response'))
                        logging.debug(self.log('Keys in response json are: {}'.format(message.keys())))
                        result['status'] = 500
        except ValueError:
            logging.debug(self.log('Unable to get json from  response'))
            logging.debug(self.log(requests_obj.text))
            result['status'] = 500
            message = requests_obj.text

        result['result'] = message
        return result

    def change_base_url(self):
        pass

    def cache_data(self):
        pass

    @staticmethod
    def log(message):
        log_msg = '[MFL-PYAPI] {}'.format(message)
        return log_msg


    @staticmethod
    def status_print(message):
        stdout.write(message.ljust(30, '.'))
        stdout.flush()
