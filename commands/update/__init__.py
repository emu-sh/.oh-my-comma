from commands.base import CommandBase
from py_utils.emu_utils import run, error
from py_utils.emu_utils import UPDATE_PATH


class Update(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'update'
    self.description = '🎉 Updates this tool'

  @staticmethod
  def _update():
    if not run(['sh', UPDATE_PATH]):
      error('Error updating!')
