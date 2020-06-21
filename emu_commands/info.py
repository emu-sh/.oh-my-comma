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
    battery_idxs = {'level': 7}
    success('Battery info:')
    for name in battery_idxs:
      idx = battery_idxs[name]
      info = r[idx]
      value = info.split(': ')[1]
      print('{}{}{}{}{}'.format(COLORS.WARNING, name.title(), COLORS.SUCCESS, value, COLORS.ENDC))


    print('START')
    print(r)
    print('END')
    # print('{}{}{}'.format(COLORS.SUCCESS, r.decode("utf-8"), COLORS.ENDC))
