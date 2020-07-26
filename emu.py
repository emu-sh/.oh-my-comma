#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if __package__ is None:
  import sys
  from os import path
  sys.path.append(path.abspath(path.join(path.dirname(__file__), 'py_utils')))
  sys.path.append(path.abspath(path.join(path.dirname(__file__), 'commands')))

  from py_utils.emu_utils import BaseFunctions
  from py_utils.emu_utils import OPENPILOT_PATH
  from commands import EMU_COMMANDS

sys.path.append(OPENPILOT_PATH)  # for importlib
DEBUG = not path.exists('/data/params/d')

class Emu(BaseFunctions):
  def __init__(self, args):
    self.name = 'emu'
    self.args = args
    self.commands = {cmd.name: cmd for cmd in EMU_COMMANDS}
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
