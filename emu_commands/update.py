import shutil
from os import path
from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, kill, error, warning, success, verify_fork_url, is_affirmative, ArgumentParser
from py_utils.emu_utils import SYSTEM_BASHRC_PATH, COMMUNITY_PATH, COMMUNITY_BASHRC_PATH, OH_MY_COMMA_PATH, UPDATE_PATH, OPENPILOT_PATH, EMU_ART

class Update(CommandBase):
  def __init__(self, description):
    super().__init__(description)

  def _update(self):
    if not run(['sh', UPDATE_PATH]):
      error('Error updating!')
