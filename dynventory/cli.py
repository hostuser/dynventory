# -*- coding: utf-8 -*-

import click
from dynventory import Inventory

@click.command()
@click.option('--list', help='Lists all groups', is_flag=True)
@click.option('--host', help='Lists all vars for specified host')
def main(list, host):
    """Console script for dynventory"""
    inv = Inventory()

    if list:
        inv.list()

    elif host:
        inv.hostvars(host)


if __name__ == "__main__":
    main()
