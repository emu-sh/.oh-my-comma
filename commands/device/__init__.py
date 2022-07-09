#!/usr/bin/python
# -*- coding: utf-8 -*-
from commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import error, check_output, COLORS, success, info
from py_utils.hardware import EON, PC, TICI


class Device(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'device'
    self.description = '📈 Statistics about your device'

    self.commands = {
      'reboot': Command(description='⚡ safely reboot your device'),
      'shutdown': Command(description='🔌 safely shutdown your device',
                          flags=[Flag(['-r', '--reboot'], 'An alternate way to reboot your device', dtype='bool')]),
    }
    if EON:  # Android-specific commands
      self.commands['battery'] = Command(description='🔋 see information about the state of your battery')
      self.commands['settings'] = Command(description='⚙️ open the Settings app',
                                          flags=[Flag(['-c', '--close'], 'Closes the settings application', dtype='bool')])

  def _settings(self):
    flags = self.get_flags('settings')
    if flags.close:
      check_output('kill $(pgrep com.android.settings)', shell=True)
      success('⚙️ Closed settings!')
    else:
      check_output('am start -a android.settings.SETTINGS')
      success('⚙️ Opened settings!')

  def _shutdown(self):
    flags = self.get_flags('shutdown')
    if flags.reboot:
      self._reboot()
      return
    if EON:
      check_output('am start -n android/com.android.internal.app.ShutdownActivity')
    else:
      check_output('sudo shutdown')
    success('🌙 Goodnight!')

  @staticmethod
  def _reboot():
    if EON:
      check_output('am start -a android.intent.action.REBOOT')
    else:
      check_output('sudo reboot')
    success('👋 See you in a bit!')

  @staticmethod
  def _battery():
    # TODO: add some power stats on TICI?

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
      battery_info = r[idx]

      value = float(battery_info.split(': ')[1])
      if name == 'temperature':
        value /= 10
        value = str(value) + '°C'
      else:
        value = str(value) + '%'

      value = COLORS.SUCCESS + str(value)
      name = COLORS.WARNING + name.title()
      print('- {}: {}{}'.format(name, value, COLORS.ENDC))
