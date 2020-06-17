from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, kill, warning, error
from py_utils.emu_utils import OPENPILOT_PATH

class Debug(CommandBase):
  def __init__(self, description):
    super().__init__(description)
    self.commands = {'controlsd': Command(description='🔬 logs controlsd to /data/output.log',
                                          flags=[Flag(['-f', '--file'], 'Name of file to save log to', has_value=True)])}

  def _controlsd(self):
    # if self.next_arg(ingest=False) is None:
    #   error('You must supply command arguments!')
    #   self._help('controlsd')
    #   return
    flags, e = self.parse_flags(self.commands['controlsd'].parser)
    if e is not None:
      error(e)
      return

    print(flags.log_file)
    print(type(flags.file))
    return
    # r = run('pkill -f controlsd')  # terminates file for some reason  # todo: remove me if not needed
    r = kill('selfdrive.controls.controlsd')  # seems to work, some process names are weird
    if r is None:
      warning('controlsd is already dead! (continuing...)')
    run('python {}/selfdrive/controls/controlsd.py'.format(OPENPILOT_PATH), out_file='/data/output.log')
