import sys
import os
from py_utils.colors import COLORS

DEBUG = not os.path.exists('/data/params/d')


class Command:
  def __init__(self, description=None, commands=None):
    self.description = description
    self.commands = commands


class CommandClass:
  debug_commands = {'controld': Command(description='logs controlsd to /data/output.log')}

  commands = {'update': Command(description='updates this tool, requires restart of ssh session'),
              'pandaflash': Command(description='pandaflash: flashes panda'),
              'pandaflash2': Command(description='pandaflash2: flashes panda without make recover'),
              'debug': Command(description='debugging tools', commands=debug_commands),
              'installfork': Command(description='Specify the fork URL after. Moves openpilot to openpilot.old')}


class Emu:
  def __init__(self, args):
    # print(args)
    self.args = args
    self.cc = CommandClass()
    self.parse()

  def _update(self):
    print('updating!')

  def _pandaflash(self):
    print('panda flashing!')

  def parse(self):
    if len(self.args) == 0:
      print('You must specify a command for emu. Some options are:')
      self.print_commands()
      return
    if self.args[0].lower() not in self.cc.commands:
      print('Unsupported command! Try one of these:')
      self.print_commands()
      return

    cmd = self.args[0].lower()
    self.start_function_from_str(cmd)

  def start_function_from_str(self, cmd):
    cmd = '_' + cmd
    if not hasattr(self, cmd):
      print('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def print_commands(self):
    cmds = [cmd for cmd in self.cc.commands]
    to_print = []
    for cmd in cmds:
      desc = self.cc.commands[cmd].description
      to_append = '{}- {}: {}{}'.format(COLORS.OKGREEN, cmd, COLORS.CYAN, desc)
      to_print.append(to_append)
    print('\n'.join(to_print) + COLORS.ENDC)


if __name__ == "__main__":
  args = sys.argv[1:]
  if DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)
