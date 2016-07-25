# coding=utf-8
#
# Copyright 2016 Apperian, Inc.  All Rights Reserved.
#
from __future__ import print_function
import json
import os
import logging
import pkgutil
import requests
from modules import applications, groups, users, wrapping, publishing, bench, credentials
__author__ = 'Shawn Roche'

ENDPOINTS = json.loads(pkgutil.get_data('apperianapi', 'endpoints.json'))


class Pyapi(bench.Bench):
    def __init__(self, username, pw, region='default', verbose=False, php=None, py=None, uploader=None, org_psk=False):
        bench.Bench.__init__(self, region)
        self.verbose = verbose
        log_level = logging.DEBUG if self.verbose else logging.CRITICAL
        logging.basicConfig(format="[%(levelname)8s] %(message)s", level=log_level)
        self.username = username
        self.password = pw
        self.org_psk = org_psk
        self.py = py
        self.php = php
        self.uploader = uploader
        self.status = ''
        self.set_region(region)

    def auth(self, username=None, password=None):
        """
        Authenticate user to the API. If user and password params are left blank, function will use the
        credentials instance was started with

        :param username: User ID for a valid EASE user in your organization’s EASE account
        :param password: User’s password
        :return: Boolean
        """
        if username:
            self.username = username
        if password:
            self.password = password

        # Python auth
        payload = json.dumps({'user_id': self.username, 'password': self.password})
        url = '%s/users/authenticate/' % self.region['python']
        if self.verbose:
            logging.debug('Sending auth via {}'.format(url))
            logging.debug('Payload - {}'.format(payload))

        try:
            r = self.py_session.post(url, data=payload, timeout=10)
            resp = self.response_check(r)

        except requests.Timeout:
            logging.error('Timed out connecting to endpoint {}'.format(self.region['python']))
            resp = {
                'status': 404,
                'result': 404
            }

        if resp['status'] == 200:
            self.token = resp['result']['token']
            self.user_data = resp['result']
            if not self.org_psk:
                self.org_psk = self.user_data['organization']['psk']
            self.update_connectors()
        else:
            if self.verbose:
                logging.debug('Auth failed\n{}'.format(resp))

        self.status = resp['status']

    def set_region(self, region):
        """
        Change the region you access for this session and authenticates you to the new environment.
        If 'list' is provided as the value for region you will see a list of options to manually choose from.

        :param region: Optional. Provide alternate region string. Use region='list' to manually select one
        """

        if self.php and self.py:
            if not self.uploader:
                self.uploader = self.php.replace('easesvc', 'fupload')
            self.region = {
                'php': 'https://{}/ease.interface.php'.format(self.php),
                'python': 'https://{}'.format(self.py),
                'downloader': 'https://{}'.format(self.php.replace('easesvc', 'fdownload')),
                'uploader': 'https://{}'.format(self.uploader)
            }
        else:
            key = ENDPOINTS.get(region.lower())
            if key:
                self.region = key
            else:
                if region != 'list':
                    print("%s is not a valid format. Please make a selection from below:" % region)
                key = self.display_options(ENDPOINTS.keys(), 'region')
                self.region = ENDPOINTS[key]

        self.init_connectors()
        self.auth()

    def set_default_region(self):
        """
        Allows you to change the default region this module uses without having to manually edit endpoints.json
        If you have never run this function the default region will be North America
        """

        print("""
        You are about to change the default region this module uses for all future sessions.
        Make a selection from one of the below regions:
        """)
        ENDPOINTS['default'] = self.display_options(ENDPOINTS, 'region')
        self.region = ENDPOINTS['default']
        self.auth(self.username, self.password)

        package_dir, package = os.path.split(__file__)
        data_path = os.path.join(package_dir, 'data', 'endpoints.json')
        with open(data_path, 'wb') as f:
            f.write(json.dumps(ENDPOINTS, indent=4, separators=(',', ': ')))

    def init_connectors(self):
        """
        Gets called as part of set_region() and creates instances of each API connector
        """
        self.app = applications.Apps(self.region)
        self.group = groups.Groups(self.region)
        self.user = users.Users(self.region)
        self.publisher = publishing.Publish(self.region)
        self.wrapper = wrapping.Wrapper(self.region)
        self.credentials = credentials.Credentials(self.region)

    def update_connectors(self):
        """
        Gets called as part of auth() to update the session token of all the API Connector instances.
        For the connectors that call functions from other connectors it also updates the instances they reference
        """
        for module in [self.app, self.group, self.user, self.publisher, self.wrapper, self.credentials]:
            module.user_data = self.user_data
            module.org_psk = self.org_psk
            module.token = self.token
            module.py_session.headers.update({'X-TOKEN': self.token})
            module.php_payload["params"] = {"token": self.token}

        self.py_session.headers.update({'X-TOKEN': self.token})
        self.php_payload["params"] = {"token": self.token}
        self.publisher.switch_org(self.org_psk)
        self.app.publisher = self.publisher
        self.wrapper.app = self.app

    ######################################
    # Org Functions
    ######################################

    def org_delete(self, psk):
        """
        :param psk: psk of the organization to be deleted
        :return: returns "ok", "auth", or the error message
        """
        url = '%s/organizations/%s' % (self.region['python'], psk)
        r = self.py_session.delete(url)
        result = self.response_check(r, 'deleted_organization')
        return result
