from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, warning, error, check_output, COLORS

class Info(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'info'
    self.description = '📈 Statistics about your device'

    self.commands = {'battery': Command(description='🔋 see information about the state of your battery')}

  def _battery(self):
    r = check_output('dumpsys batterymanager')
    if not r or not isinstance(r, bytes):
      error('Unable to get battery status!')
      return
    print('{}{}{}'.format(COLORS.SUCCESS, r.decode("utf-8"), COLORS.ENDC))
