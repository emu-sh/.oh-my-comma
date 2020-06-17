#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import importlib
import shutil
if __package__ is None:
  import sys
  from os import path
  sys.path.append(path.abspath(path.join(path.dirname(__file__), 'py_utils')))
  sys.path.append(path.abspath(path.join(path.dirname(__file__), 'emu_commands')))

  from py_utils.colors import COLORS
  from py_utils.emu_utils import run, kill, error, warning, success, verify_fork_url, is_affirmative, ArgumentParser, BaseFunctions
  from py_utils.emu_utils import SYSTEM_BASHRC_PATH, COMMUNITY_PATH, COMMUNITY_BASHRC_PATH, OH_MY_COMMA_PATH, UPDATE_PATH, OPENPILOT_PATH, EMU_ART
  from emu_commands.base import CommandBase, Flag, Command
  from emu_commands.fork import Fork
  from emu_commands.update import Update
  from emu_commands.panda import Panda
  from emu_commands.debug import Debug

sys.path.append(OPENPILOT_PATH)  # for importlib
DEBUG = not path.exists('/data/params/d')


# class CommandClass:
#
#
#   #             'help':   Command(description='Type `emu help command` to get flags 🚩 and syntax for command')}


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

  def print_commands(self, error_msg=None, ascii_art=False):
    to_print = []
    if ascii_art:
      print(EMU_ART)

    if error_msg is not None:
      error(error_msg)
    for cmd in self.commands:
      desc = COLORS.CYAN + self.commands[cmd].description
      # other format: to_append = '- {:>15}: {:>20}'.format(cmd, desc)
      to_append = '- {:<12} {}'.format(cmd + ':', desc)  # 12 is length of longest command + 1
      to_print.append(COLORS.OKGREEN + to_append)
    print('\n'.join(to_print) + COLORS.ENDC + '\n')


  # def _help(self, commands=None):
  #   cmd = self.next_arg()
  #   if cmd is None:
  #     self.print_commands(error_msg='You must specify a command to get help with! Some are:')
  #     return
  #   if cmd not in self.cc.commands:
  #     self.print_commands(error_msg='Unknown command! Try one of these:')
  #     return
  #
  #   description = self.cc.commands[cmd].description
  #   print('{}>>  Description: {}{}'.format(COLORS.CYAN, description, COLORS.ENDC))
  #   print('{}>>  Flags:{}'.format(COLORS.WARNING, COLORS.ENDC))
  #   flags = self.cc.commands[cmd].flags
  #
  #   flags_to_print = []
  #   if flags is None:
  #     warning('  - None')
  #   elif flags is not None and len(flags) > 0:
  #     for flag in flags:
  #       aliases = COLORS.SUCCESS + ', '.join(flag.aliases) + COLORS.WARNING
  #       flags_to_print.append(COLORS.WARNING + '  - {}: {}'.format(aliases, flag.description) + COLORS.ENDC)
  #     print('\n'.join(flags_to_print))
  #   else:
  #     print('Unknown to parse flags, this is awkward...')
  #
  #   print('{}>>  Commands:{}'.format(COLORS.OKGREEN, COLORS.ENDC))
  #
  #   commands = self.cc.commands[cmd].commands
  #   cmds_to_print = []
  #   if commands is None:
  #     success('  - None')
  #   elif commands is not None and len(commands) > 0:
  #   elif commands is not None and len(commands) > 0:
  #     for cmd in commands:
  #       # cmds_to_print.append('  - {}: {}'.format(cmd, commands[cmd].description))
  #       # aliases = COLORS.SUCCESS + ', '.join(flag.aliases) + COLORS.WARNING
  #       cmds_to_print.append(COLORS.FAIL + '  - {}: {}'.format(cmd, success(commands[cmd].description, ret=True)) + COLORS.ENDC)
  #     print('\n'.join(cmds_to_print))


if __name__ == "__main__":
  args = sys.argv[1:]
  if DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)

# cc = CommandClass()
