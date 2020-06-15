import os
import sys
import stat
import subprocess
from py_utils.colors import COLORS

DEBUG = not os.path.exists('/data/params/d')


class Command:
  def __init__(self, description=None, commands=None):
    self.description = description
    self.commands = commands


class CommandClass:
  debug_commands = {'controls': Command(description='logs controlsd to /data/output.log')}

  commands = {'update': Command(description='updates this tool, requires restart of ssh session'),
              'pandaflash': Command(description='pandaflash: flashes panda'),
              'pandaflash2': Command(description='pandaflash2: flashes panda without make recover'),
              'debug': Command(description='debugging tools', commands=debug_commands),
              'installfork': Command(description='Specify the fork URL after. Moves openpilot to openpilot.old')}


class Emu:
  def __init__(self, args):
    self.args = args
    self.cc = CommandClass()

    self.SYSTEM_BASHRC_PATH = '/home/.bashrc'
    self.COMMUNITY_PATH = '/data/community'
    self.COMMUNITY_BASHRC_PATH = '/data/community/.bashrc'
    self.OH_MY_COMMA_PATH = '/data/community/.oh-my-comma'
    self.UPDATE_PATH = '{}/update.sh'.format(self.OH_MY_COMMA_PATH)

    self.parse()

  def _update(self):
    try:
      r = subprocess.call(['sh', self.UPDATE_PATH])
    except:
      r = 1
    if r:
      self.error('Error calling update script!')

  def _pandaflash(self):
    print('panda flashing!')

  def _pandaflash2(self):
    print('panda flashing2!')

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
      desc = COLORS.CYAN + self.cc.commands[cmd].description
      # other format: to_append = '- {:>15}: {:>20}'.format(cmd, desc)
      to_append = '- {:<12} {}'.format(cmd + ':', desc)  # 12 is length of longest command + 1
      to_print.append(COLORS.OKGREEN + to_append)
    print('\n'.join(to_print) + COLORS.ENDC)

  def error(self, msg):
    print('{}{}{}'.format(COLORS.FAIL, msg, COLORS.ENDC))


if __name__ == "__main__":
  args = sys.argv[1:]
  if DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)
