from emu_commands.base import CommandBase
from py_utils.emu_utils import run, error
from py_utils.emu_utils import UPDATE_PATH

class Update(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'update'
    self.description = '🎉 updates this tool, recommended to restart ssh session'
    # todo: don't we need commands here?

  def _update(self):
    if not run(['sh', UPDATE_PATH]):
      error('Error updating!')
