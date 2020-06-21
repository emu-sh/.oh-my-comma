from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, warning, error, check_output

class Info(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'info'
    self.description = '📈 Statistics about your device'

    self.commands = {'battery': Command(description='🔋 see information about the state of your battery')}

  def _battery(self):
    r = check_output('dumpsys batterymanager')
    if not r:
      error('Unable to get battery status!')
      return
    print('success: {}'.format(r.status))
    print(r.output)
    print()
    warning('Hah, sucker!')
