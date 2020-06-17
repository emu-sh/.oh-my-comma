#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys
t = time.time()
# if __package__ is None:
import sys
from os import path
# sys.path.append(path.abspath(path.join(path.dirname(__file__), 'py_utils')))
# sys.path.append(path.abspath(path.join(path.dirname(__file__), 'emu_commands')))

from py_utils.emu_utils import BaseFunctions
from py_utils.emu_utils import OPENPILOT_PATH
from emu_commands.fork import Fork
from emu_commands.update import Update
from emu_commands.panda import Panda
from emu_commands.debug import Debug
print(time.time() - t)
sys.path.append(OPENPILOT_PATH)  # for importlib
DEBUG = not path.exists('/data/params/d')

class Emu(BaseFunctions):
  def __init__(self, args):
    self.args = args
    self.commands = {'fork': Fork('🍴 control installed forks, or clone a new one'),
                     'update': Update('🎉 updates this tool, recommended to restart ssh session'),
                     'panda': Panda('🐼 panda interfacing tools'),
                     'debug': Debug('de-🐛-ing tools')}
    self.parse()

  def parse(self):
    cmd = self.next_arg()

    if cmd is None:
      self.print_commands(error_msg='You must specify a command for emu. Some options are:', ascii_art=True)
      return
    if cmd not in self.commands:
      self.print_commands(error_msg='Unknown command! Try one of these:')
      return

    self.commands[cmd].main(self.args, cmd)


if __name__ == "__main__":
  args = sys.argv[1:]
  if DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)
