from emu_commands.base import CommandBase, Command
from py_utils.emu_utils import run, kill, warning
from py_utils.emu_utils import OPENPILOT_PATH

class Debug(CommandBase):
  def __init__(self, description):
    super().__init__(description)
    self.commands = {'controlsd': Command(description='🔬 logs controlsd to /data/output.log')}

  def _controlsd(self):
    # r = run('pkill -f controlsd')  # terminates file for some reason  # todo: remove me if not needed
    r = kill('selfdrive.controls.controlsd')  # seems to work, some process names are weird
    if r is None:
      warning('controlsd is already dead! (continuing...)')
    run('python {}/selfdrive/controls/controlsd.py'.format(OPENPILOT_PATH), out_file='/data/output.log')
