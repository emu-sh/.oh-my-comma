import sys

DEBUG = True


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
    print(args)
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

    self.start_command_from_str(cmd)
    # if cmd == 'update':
    #   print('updating!')
    # elif cmd == 'pandaflash':
    #   print('pandaflash')
    # elif cmd == 'pandaflash2':
    #   print('pandaflash2')
    # elif cmd == 'debug':
    #   print('debug')
    # elif cmd == 'installfork':
    #   print('debug')

  def start_command_from_str(self, cmd):
    getattr(self, '_{}'.format(cmd))

  def print_commands(self):
    cmds = [cmd for cmd in self.cc.commands]
    # descs = [self.cc.commands[cmd].description for cmd in cmds]
    to_print = []
    for cmd in cmds:
      desc = self.cc.commands[cmd].description
      to_print.append('- {}: {}'.format(cmd, desc))
    print('\n'.join(to_print))


if __name__ == "__main__":
  args = sys.argv[1:]
  if len(args) == 0 and DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)
