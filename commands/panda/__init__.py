#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib
from commands.base import CommandBase, Command
from py_utils.emu_utils import run, error
from py_utils.emu_utils import OPENPILOT_PATH

class Panda(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'panda'
    self.description = '🐼 panda interfacing tools'

    self.commands = {'flash': Command(description='🐼 flashes panda with make recover (usually works with the C2)'),
                     'flash2': Command(description='🎍 flashes panda using Panda module (usually works with the EON)')}

  def _flash(self):
    r = run('make -C {}/panda/board recover'.format(OPENPILOT_PATH))
    if not r:
      error('Error running make command!')

  def _flash2(self):
    if not run('pkill -f boardd'):
      error('Error killing boardd! Is it running? (continuing...)')
    importlib.import_module('panda', 'Panda').Panda().flash()
