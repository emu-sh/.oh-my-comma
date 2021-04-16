#!/usr/bin/python
# -*- coding: utf-8 -*-
from commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, kill, warning, check_output, is_affirmative, error, info
from py_utils.emu_utils import OPENPILOT_PATH


class Debug(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'debug'
    self.description = 'de-🐛-ing tools'

    self.commands = {'controlsd': Command(description='🔬 logs controlsd to /data/output.log by default',
                                          flags=[Flag(['-o', '--output'], 'Name of file to save log to', dtype='str')]),
                     'reload': Command(description='🔄 kills the current openpilot session and restarts it (all without rebooting)')}
    self.default_path = '/data/output.log'

  def _reload(self):
    info('This will kill the current openpilot tmux session, create a new session adding its PID to the app cpuset, and relaunch openpilot.')
    info('Confirm you would like to continue')
    if not is_affirmative():
      error('Aborting!')
      return

    r = check_output('tmux kill-session -t comma')
    if r.success:
      info('Killed the current openpilot session')
    else:
      warning('Error killing current openpilot session, continuing...')

    r = check_output(['tmux', 'new', '-s', 'comma', '-d', "touch /data/openpilot/test_file; /data/openpilot/launch_openpilot.sh"])
    # r = check_output(['touch', '/data/openpilot/test_file'])
    # r = check_output(['tmux', 'new', '-s', 'comma', '-d', "'touch /data/openpilot/test_file; /data/openpilot/launch_openpilot.sh'"])




  def _kill_and_create_tmux_session(self):
    r = check_output(['tmux', 'new', '-s', 'comma'])
    return r.success


  def _controlsd(self):
    flags = self.get_flags('controlsd')
    out_file = self.default_path
    if flags.output is not None:
      out_file = flags.output
    # r = run('pkill -f controlsd')  # terminates file for some reason  # todo: remove me if not needed
    r = kill('selfdrive.controls.controlsd')  # seems to work, some process names are weird
    if r is None:
      warning('controlsd is already dead! (continuing...)')
    run('python {}/selfdrive/controls/controlsd.py'.format(OPENPILOT_PATH), out_file=out_file)
