# -*- coding: utf-8 -*-

import click
from freckles import Freckles
import pprint
import py
import yaml
import os
import json

DEFAULT_INDENT = 2

class Config(object):

    def __init__(self, *args, **kwargs):
        self.config_dir = click.get_app_dir('freckles')
        self.config_file = py.path.local(self.config_dir).join('config.yml')
        self.config = dict(*args, **kwargs)

    def load(self):
        """load yaml config from disk"""

        try:
            yaml_string = self.config_file.read()
            if yaml:
                self.config.update(yaml.load(yaml_string))
        except py.error.ENOENT:
            pass

    def save(self):
        """save yaml config to disk"""

        if not self.config:
            self.config = {"build_dir": os.path.join(self.config_dir, "build_dir")}

        self.config_file.ensure()
        with self.config_file.open('w') as f:
            yaml.dump(self.config, f, default_flow_style=True)

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(invoke_without_command=True)
@pass_config
@click.pass_context
@click.option('--hosts', help='comma-separated list of hosts (default: \'localhost\')', default="localhost", nargs=1)
@click.option('--dotfiles', help='base-path(s) for dotfile directories (can be used multiple times)', type=click.Path(exists=True, dir_okay=True, readable=True, resolve_path=True), multiple=True)
def cli(ctx, config, hosts, dotfiles):
    config.load()

    if not config.config:
        config.save()

    config.hosts = hosts
    config.dotfiles = dotfiles
    config.freckles = create_freckles(config.dotfiles, config.hosts)

    if ctx.invoked_subcommand is None:
        run(config)


@cli.command()
@pass_config
def playbook(config):

    play = config.freckles.create_playbook()
    click.echo(play)

@cli.command()
@pass_config
def inventory(config):

    inv = config.freckles.create_inventory()
    inv_json = json.dumps(inv, sort_keys=True, indent=DEFAULT_INDENT)

    click.echo(inv_json)

def create_freckles(dotfile_dirs, hosts):

    inv_hosts = {}
    for host in hosts.split(","):
        if host == "localhost" or host == "127.0.0.1":
            inv_hosts[host] = {"ansible_connection": "local"}
        else:
            inv_hosts[host] = {}

    freckles = Freckles("local_apps", dotfile_dirs, hosts=inv_hosts)
    return freckles


def run(config):

    click.echo("XXX")




if __name__ == "__main__":
    cli()
