from py_utils.colors import COLORS
from py_utils.emu_utils import ArgumentParser, BaseFunctions, warning, success

class BaseCommand(BaseFunctions):
  def __init__(self, description):
    self.description = description

  def main(self, args, cmd_name):
    self.args = args
    cmd = self.next_arg()
    if cmd is None:
      self.print_commands(error_msg='You must specify a command for emu {}. Some options are:'.format(cmd_name))
      return
    if cmd not in self.commands:
      self.print_commands(error_msg='Unknown command! Try one of these:')
      return
    self.start_function_from_str(cmd)

  def start_function_from_str(self, cmd):
    cmd = '_' + cmd
    if not hasattr(self, cmd):
      print('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def parse_flags(self, parser):
    try:
      return parser.parse_args(self.args), None
    except Exception as e:
      return None, e

  def _help(self, cmd):
    # if cmd is None:
    #   self.print_commands(error_msg='You must specify a command to get help with! Some are:')
    #   return
    # if cmd not in self.cc.commands:
    #   self.print_commands(error_msg='Unknown command! Try one of these:')
    #   return

    description = self.commands[cmd].description
    print('{}>>  Description: {}{}'.format(COLORS.CYAN, description, COLORS.ENDC))

    flags = self.commands[cmd].flags

    flags_to_print = []
    if flags is not None and len(flags) > 0:
      print('{}>>  Flags:{}'.format(COLORS.WARNING, COLORS.ENDC))
      for flag in flags:
        aliases = COLORS.SUCCESS + ', '.join(flag.aliases) + COLORS.WARNING
        flags_to_print.append(COLORS.WARNING + '  - {}: {}'.format(aliases, flag.description) + COLORS.ENDC)
      print('\n'.join(flags_to_print))

    commands = self.commands[cmd].commands
    cmds_to_print = []
    if commands is not None and len(commands) > 0:
      print('{}>>  Commands:{}'.format(COLORS.OKGREEN, COLORS.ENDC))
      for cmd in commands:
        # cmds_to_print.append('  - {}: {}'.format(cmd, commands[cmd].description))
        # aliases = COLORS.SUCCESS + ', '.join(flag.aliases) + COLORS.WARNING
        cmds_to_print.append(COLORS.FAIL + '  - {}: {}'.format(cmd, success(commands[cmd].description, ret=True)) + COLORS.ENDC)
      print('\n'.join(cmds_to_print))

class Flag:
  def __init__(self, aliases, description, has_value=False):
    self.aliases = aliases
    self.description = description
    self.has_value = has_value

class Command:
  def __init__(self, description=None, commands=None, flags=None):
    self.parser = ArgumentParser()
    self.description = description
    self.commands = commands
    self.has_flags = False
    self.flags = flags
    if flags is not None:
      self.has_flags = True
      for flag in flags:
        # for each flag, add it as argument with aliases.
        # if flag.has_value, parse value as string, if not, assume flag is boolean
        action = 'store_true' if not flag.has_value else None
        self.parser.add_argument(*flag.aliases, action=action)
