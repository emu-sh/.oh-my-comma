import shutil
import importlib
from emu_commands.base import CommandBase, Command
from py_utils.emu_utils import run, kill, error, warning, success, verify_fork_url, is_affirmative, ArgumentParser
from py_utils.emu_utils import SYSTEM_BASHRC_PATH, COMMUNITY_PATH, COMMUNITY_BASHRC_PATH, OH_MY_COMMA_PATH, UPDATE_PATH, OPENPILOT_PATH, EMU_ART

class Panda(CommandBase):
  def __init__(self, description):
    super().__init__(description)
    self.commands = {'flash': Command(description='flashes 🐼 with make recover (usually works with the EON)'),
                     'flash2': Command(description='flashes 🐼 using 🐼 module (usually works with the C2)')}

  def _flash(self):
    r = run('make -C {}/panda/board recover'.format(OPENPILOT_PATH))
    if not r:
      error('Error running make command!')

  def _flash2(self):
    if not run('pkill -f boardd'):
      error('Error killing boardd! Is it running? (continuing...)')
    importlib.import_module('panda', 'Panda').Panda().flash()
