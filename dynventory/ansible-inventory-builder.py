#!/usr/bin/env python

import yaml
import pprint
import sys

DEFAULT_CONTAINER_FILE="/home/markus/projects/elwood/boxes.yml"

class Inventory(object):

    def __init__(self, container_yaml_file=DEFAULT_CONTAINER_FILE):
        self.container_file = container_yaml_file

        stream = open(container_yaml_file, "r")
        self.containers = yaml.load(stream)
        self.groups = {}
        self.hosts = {}

        for name,c in self.containers.items():
            if not c:
                continue
            for host,v in c.items():
                ip = v["ip"]
                self.hosts[ip] = {}
                for prop,prop_value in v.items():

                    self.hosts[ip][prop] = prop_value

                for group in v.get("groups"):
                    if not self.groups.get(group, None):
                        self.groups[group] = {"hosts": [], "vars": {"ansible_user": "ansible"}, "children": []}
                    self.groups[group]["hosts"].append(v.get("ip"))

    def list(self):
        pprint.pprint(self.groups)

    def hostvars(self, hostname):
        # TODO
        pprint.pprint(self.hosts[hostname])

if __name__ == "__main__":

    inv = Inventory()

    if len(sys.argv) == 1:
        sys.exit()

    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        inv.list()

    if len(sys.argv) == 3 and sys.argv[1] == "--host":
        hostname = sys.argv[2]
        inv.hostvars(hostname)
