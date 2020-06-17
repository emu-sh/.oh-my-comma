from py_utils.colors import COLORS
from py_utils.emu_utils import ArgumentParser, BaseFunctions, warning, success

class CommandBase(BaseFunctions):
  def __init__(self, description):
    self.description = description
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
      print('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def parse_flags(self, parser):
    try:
      return parser.parse_args(self.args), None
    except Exception as e:
      return None, e



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
