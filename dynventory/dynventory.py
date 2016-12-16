# -*- coding: utf-8 -*-

import yaml
import sys
import os

DEFAULT_CONTAINER_FILE = "/home/markus/projects/ansible/dynventory/example.yml"

class Inventory(object):

    def __init__(self, inventory_yaml=DEFAULT_CONTAINER_FILE):

        self.inventory_yaml = inventory_yaml

        if type(self.inventory_yaml) == dict:
            self.inventory = self.inventory_yaml
        elif os.path.exists(self.inventory_yaml):
            stream = open(self.inventory_yaml, "r")
            self.inventory = yaml.load(stream)
        else:
            # try to load string as yaml
            yaml.load(self.inventory_yaml)

        self.groups = {}
        self.hosts = {}

        # get all groups
        inv_groups = self.inventory.get("groups", {})

        for name, details in inv_groups.iteritems():
            self.groups[name] = {}
            self.groups[name]["hosts"] = details.get("hosts", [])
            self.groups[name]["vars"] = details.get("vars", {})

        # get all hosts
        inv_hosts = self.inventory.get("hosts", {})
        for name, details in inv_hosts.iteritems():
            self.hosts[name] = inv_hosts.get(name, {})

    def assemble_meta(self):
        # build _meta dict to enable ansible caching
        meta = {}
        result = {}
        for group in self.groups.keys():
            meta[group] = {"hostvars": {}}
            for host in self.groups[group]["hosts"]:
                if self.hosts.get(host, False):
                    meta[group]["hostvars"][host] = self.hosts[host]

            result[group] = self.groups[group]
            result["_meta"] = meta[group]

        return result

    def list(self, incl_meta=True):
        if incl_meta:
            return self.assemble_meta()
        else:
            return self.groups

    def hostvars(self, hostname):
        return self.hosts[hostname]

if __name__ == "__main__":

    inv = Inventory()

    if len(sys.argv) == 1:
        sys.exit()

    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        inv.list()

    if len(sys.argv) == 3 and sys.argv[1] == "--host":
        hostname = sys.argv[2]
        inv.hostvars(hostname)
