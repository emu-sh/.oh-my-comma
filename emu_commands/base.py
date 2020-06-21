from py_utils.colors import COLORS
from py_utils.emu_utils import ArgumentParser, BaseFunctions, success, error

class CommandBase(BaseFunctions):
  def __init__(self):
    self.commands = {}

  def main(self, args, cmd_name):
    self.args = args
    cmd = self.next_arg()
    if len(self.commands) > 0:
      if cmd is None:
        self.print_commands(error_msg='You must specify a command for emu {}. Some options are:'.format(cmd_name))
        return
      if cmd not in self.commands:
        self.print_commands(error_msg='Unknown command! Try one of these:')
        return
      self.start_function_from_str(cmd)
    else:
      self.start_function_from_str(cmd_name)

  def start_function_from_str(self, cmd):
    cmd = '_' + cmd
    if not hasattr(self, cmd):
      error('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def parse_flags(self, parser):
    try:
      return parser.parse_args(self.args), None
    except Exception as e:
      return None, e

  def _help(self, cmd, show_description=True, leading=''):
    description = self.commands[cmd].description
    if show_description:
      print('{}>>  Description 📚: {}{}'.format(COLORS.CYAN, description, COLORS.ENDC))

    flags = self.commands[cmd].flags

    flags_to_print = []
    if flags is not None and len(flags) > 0:
      print(leading + '{}>>  Flags 🎌:{}'.format(COLORS.WARNING, COLORS.ENDC))
      for flag in flags:
        aliases = COLORS.SUCCESS + ', '.join(flag.aliases) + COLORS.WARNING
        flags_to_print.append(leading + COLORS.WARNING + '  - {}: {}'.format(aliases, flag.description) + COLORS.ENDC)
      print('\n'.join(flags_to_print))

    commands = self.commands[cmd].commands
    cmds_to_print = []
    if commands is not None and len(commands) > 0:
      print(leading + '{}>>  Commands 💻:{}'.format(COLORS.OKGREEN, COLORS.ENDC))
      for cmd in commands:
        cmds_to_print.append(leading + COLORS.FAIL + '  - {}: {}'.format(cmd, success(commands[cmd].description, ret=True)) + COLORS.ENDC)
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
        self.parser.add_argument(*flag.aliases, help=flag.description, action=action)
