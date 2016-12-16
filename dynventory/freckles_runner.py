#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.utils.display import Display
from ansible.executor import playbook_executor

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print json.dumps({host.name: result._result}, indent=4)

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'verbosity'])

class FrecklesRunner(object):

    def __init__(self, playbook, become_pass, verbosity=0):

        self.options = Options()
        self.options.verbosity = verbosity

        self.display = Display()
        self.display.verbosity = self.options.verbosity
        playbook_executor.verbosity = self.options.verbosity

        passwords = {'become_pass': become_pass}

        self.loader = DataLoader()
        self.loader.set_vault_password(os.environ['VAULT_PASS'])

        self.variable_manager = VariableManager()
        self.variable_manager.extra_vars = self.run_data




Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
# initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None, become_method=None, become_user=None, check=False)
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()
