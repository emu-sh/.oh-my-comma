#!/usr/bin/python
# -*- coding: utf-8 -*-
from commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, warning, error, check_output, COLORS, success

class Device(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'device'
    self.description = '📈 Statistics about your device'

    self.commands = {'battery': Command(description='🔋 see information about the state of your battery'),
                     'reboot': Command(description='⚡ safely reboot your device'),
                     'shutdown': Command(description='🔌 safely shutdown your device',
                                         flags=[Flag(['-r', '--reboot'], 'An alternate way to reboot the device', dtype='bool')]),
                     'settings': Command(description='⚙️ open the Settings app')}

  def _settings(self):
    check_output('am start -a android.settings.SETTINGS')
    success('⚙️ Opened settings!')

  def _reboot(self):
    check_output('am start -a android.intent.action.REBOOT')
    success('👋 See you in a bit!')

  def _shutdown(self):
    flags, e = self.parse_flags(self.commands['shutdown'].parser)
    if e is None and flags.reboot:
      self._reboot()
      return
    check_output('am start -n android/com.android.internal.app.ShutdownActivity')
    success('🌙 Goodnight!')

  def _battery(self):
    r = check_output('dumpsys batterymanager')
    if not r:
      error('Unable to get battery status!')
      return
    r = r.output.split('\n')
    r = [i.strip() for i in r if i != ''][1:]
    battery_idxs = {'level': 7, 'temperature': 10}
    success('Battery info:')
    for name in battery_idxs:
      idx = battery_idxs[name]
      info = r[idx]

      value = float(info.split(': ')[1])
      if name == 'temperature':
        value /= 10
        value = str(value) + '°C'
      else:
        value = str(value) + '%'

      value = COLORS.SUCCESS + str(value)
      name = COLORS.WARNING + name.title()
      print('- {}: {}{}'.format(name, value, COLORS.ENDC))
