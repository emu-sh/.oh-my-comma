#!/usr/bin/python
# -*- coding: utf-8 -*-
from commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, kill, warning, check_output, is_affirmative, error, info, success
from py_utils.emu_utils import OPENPILOT_PATH


class Debug(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'debug'
    self.description = 'de-🐛-ing tools'

    self.commands = {'controlsd': Command(description='🔬 logs controlsd to /data/output.log by default',
                                          flags=[Flag(['-o', '--output'], 'Name of file to save log to', dtype='str')]),
                     'reload': Command(description='🔄 kills the current openpilot session and restarts it (all without rebooting)')}

  @staticmethod
  def _reload():
    info('This will kill the current openpilot tmux session, set up a new one properly, and relaunch openpilot.')
    info('Confirm you would like to continue')
    if not is_affirmative():
      error('Aborting!')
      return

    r = check_output('tmux kill-session -t comma')
    if r.success:
      info('Killed the current openpilot session')
    else:
      warning('Error killing current openpilot session, continuing...')

    # Command below thanks to mlp
    r = check_output(['tmux', 'new', '-s', 'comma', '-d',
                      "echo $$ > /dev/cpuset/app/tasks;"  # add pid of current shell to app cpuset
                      "echo $PPID > /dev/cpuset/app/tasks;"  # (our parent, tmux, also gets all the cores)
                      "/data/openpilot/launch_openpilot.sh"])
    if r.success:
      success('Succesfully started a new tmux session for openpilot!')
      success('Type tmux a to attach to it')

  def _controlsd(self):
    out_file = '/data/output.log'
    flags = self.get_flags('controlsd')
    if flags.output is not None:
      out_file = flags.output
    # r = run('pkill -f controlsd')  # terminates file for some reason  # todo: remove me if not needed
    r = kill('selfdrive.controls.controlsd')  # seems to work, some process names are weird
    if r is None:
      warning('controlsd is already dead! (continuing...)')
    run('python {}/selfdrive/controls/controlsd.py'.format(OPENPILOT_PATH), out_file=out_file)
