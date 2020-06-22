from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, warning, error, check_output, COLORS, success

class Uninstall(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'uninstall'
    self.description = 'Uninstalls emu'

  def _uninstall(self):
    print('Are you sure you want to uninstall?')
    input()
