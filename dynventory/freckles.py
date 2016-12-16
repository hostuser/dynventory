# -*- coding: utf-8 -*-

from dynventory import Inventory
import os
import yaml
import pprint
import json


KEYWORDS = ["pkgs", "dotfiles"]

FRECKLES_METADATA_FILENAME = ".freckles"
FRECKLES_DEFAULT_PROFILE = "<all>"
FRECKLES_DEFAULT_PACKAGE_STATE = "present"
FRECKLES_DEFAULT_PACKAGE_SUDO = True
FRECKLES_DEFAULT_BUILD_DIR = os.path.join(os.path.expanduser("~"), ".config", "freckles", "build")

class Freckles(object):

    def __init__(self, group_name, base_dirs, default_pkg_state=FRECKLES_DEFAULT_PACKAGE_STATE, default_pkg_sudo=FRECKLES_DEFAULT_PACKAGE_SUDO, hosts={u"localhost": {u"ansible_connection": u"local"}}):

        self.group_name = group_name
        self.base_dirs = base_dirs
        self.hosts = hosts

        self.apps = {}
        for dir in base_dirs:
            for item in os.listdir(dir):
                if not item.startswith(".") and os.path.isdir(os.path.join(dir, item)):
                    # defaults
                    self.apps[item] = {"dotfiles": os.path.join(dir, item), "pkgs": [item], "pkg_state": default_pkg_state, "pkg_sudo": default_pkg_sudo}
                    freckles_metadata_file = os.path.join(dir, item, FRECKLES_METADATA_FILENAME)
                    if os.path.exists(freckles_metadata_file):
                        stream = open(freckles_metadata_file, 'r')
                        self.apps[item] = yaml.load(stream)

    def list_all(self):
        pprint.pprint(self.apps)

    def list(self, package_managers="apt", tags=None):
        print yaml.dump(self.apps, default_flow_style=False)

    def create_inventory(self):

        groups = {app: {"vars": details, "hosts": [host for host in self.hosts.keys()]} for app, details in self.apps.iteritems()}
        hosts = self.hosts

        inv = Inventory({"groups": groups, "hosts": hosts})
        return inv.list()

    def create_playbook(self):

        play = []

        for app, details in self.apps.iteritems():
            hosts = app
            roles = ["ansible-freckles"]
            play.append({"hosts": hosts, "roles": roles})

        return yaml.safe_dump(play, default_flow_style=False)
