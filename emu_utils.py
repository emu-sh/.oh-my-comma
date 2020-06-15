import sys
sys.path.append('/data/openpilot')
import os
import importlib
import subprocess
import time
import psutil
from py_utils.colors import COLORS

DEBUG = not os.path.exists('/data/params/d')


def run(cmd, out_file=None):
  """
  If cmd is a string, it is split into a list, otherwise it doesn't modify cmd.
  The status is returned, True being success, False for failure
  """
  if isinstance(cmd, str):
    cmd = cmd.split()

  f = None
  if isinstance(out_file, str):
    f = open(out_file, 'a')

  try:
    r = subprocess.call(cmd, stdout=f)
    return not r
  except Exception as e:
    print(e)
    return False


def kill(procname):
  for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == procname:
      proc.kill()
      return True
  return None


def error(msg):
  print('{}{}{}'.format(COLORS.FAIL, msg, COLORS.ENDC))


def warning(msg):
  print('{}{}{}'.format(COLORS.WARNING, msg, COLORS.ENDC))


class Command:
  def __init__(self, description=None, commands=None):
    self.description = description
    self.commands = commands


class CommandClass:
  debug_commands = {'controlsd': Command(description='logs controlsd to /data/output.log')}

  commands = {'update': Command(description='updates this tool, requires restart of ssh session'),
              'pandaflash': Command(description='pandaflash: flashes panda with make recover'),
              'pandaflash2': Command(description='pandaflash2: flashes panda using Panda module'),
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

    self.arg_idx = 0
    self.parse()

  def _update(self):
    if not run(['sh', self.UPDATE_PATH]):
      error('Error updating!')

  def _pandaflash(self):
    r = run('make -C /data/openpilot/panda/board recover')
    if not r:
      error('Error running make command!')

  def _pandaflash2(self):
    if not run('pkill -f boardd'):
      error('Error killing boardd! Is it running?')
      return
    importlib.import_module('panda', 'Panda').Panda().flash()

  def _debug(self):
    cmd = self.get_next_arg()
    if cmd is None:
      print("You must specify a command for emu debug. Some options are:")
      self.print_commands('debug_commands')
      return
    if cmd not in self.cc.debug_commands:
      print('Unsupported debug command! Try one of these:')
      self.print_commands('debug_commands')
      return
    self.start_function_from_str(cmd)

  def _controlsd(self):
    # PYTHONPATH=/data/openpilot python /data/openpilot/selfdrive/controls/controlsd.py 2>&1 | tee /data/output.log
    # r = run('pkill -f controlsd')  # terminated file for some reason
    r = kill('selfdrive.controlsd')  # seems to work, some process names are weird
    if r is None:
      warning('controlsd is already dead! (continuing...)')
    run('python /data/openpilot/selfdrive/controls/controlsd.py', out_file='/data/output.log')

    # print(r)


  def _installfork(self):
    print('Install fork menu')

  def parse(self):
    if len(self.args) == 0:
      print('You must specify a command for emu. Some options are:')
      self.print_commands()
      return
    cmd = self.get_next_arg()
    if cmd not in self.cc.commands:
      print('Unsupported command! Try one of these:')
      self.print_commands()
      return

    self.start_function_from_str(cmd)

  def start_function_from_str(self, cmd):
    cmd = '_' + cmd
    if not hasattr(self, cmd):
      print('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def print_commands(self, command='commands'):
    cmd_list = getattr(self.cc, command)
    cmds = [cmd for cmd in cmd_list]
    to_print = []
    for cmd in cmds:
      desc = COLORS.CYAN + cmd_list[cmd].description
      # other format: to_append = '- {:>15}: {:>20}'.format(cmd, desc)
      to_append = '- {:<12} {}'.format(cmd + ':', desc)  # 12 is length of longest command + 1
      to_print.append(COLORS.OKGREEN + to_append)
    print('\n'.join(to_print) + COLORS.ENDC + '\n')

  def get_next_arg(self, lower=True):
    # print(self.args)
    # print(len(self.args), self.arg_idx)
    if len(self.args) - 1 < self.arg_idx:
      return None
    arg = self.args[self.arg_idx]
    self.arg_idx += 1
    if lower:
      arg = arg.lower()
    # print(arg)
    return arg


if __name__ == "__main__":
  args = sys.argv[1:]
  if DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)
