from emu_commands.base import CommandBase
from py_utils.emu_utils import run, error
from py_utils.emu_utils import UPDATE_PATH

class Update(CommandBase):
  def __init__(self, description):
    super().__init__(description)

  def _update(self):
    if not run(['sh', UPDATE_PATH]):
      error('Error updating!')
