from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, warning, error, check_output, COLORS, success

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
    r = r.decode('utf-8').split('\n')
    r = [i.strip() for i in r if i != ''][1:]
    battery_idxs = {'level': 7, 'temperature': 10}
    success('Battery info:')
    for name in battery_idxs:
      idx = battery_idxs[name]
      info = r[idx]

      name = COLORS.WARNING + name.title()
      value = float(info.split(': ')[1])

      if name == 'temperature':
        value /= 10
        value = str(value) + ' °C'
      else:
        value = str(value) + '%'
      value = COLORS.SUCCESS + str(value)

      print('  {}: {}{}'.format(name, value, COLORS.ENDC))
