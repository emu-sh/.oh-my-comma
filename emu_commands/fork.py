import shutil
import os
import json
from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, error, warning, success, warning, info, is_affirmative, check_output
from py_utils.emu_utils import OPENPILOT_PATH, FORKS_PATH, FORK_PARAM_PATH


COMMAAI_PATH = FORKS_PATH + '/commaai'
GIT_OPENPILOT_URL = 'https://github.com/commaai/openpilot'


class ForkParams:
  def __init__(self):
    self.default_params = {'current_fork': None,
                           'installed_forks': [],
                           'setup_complete': False}
    self._init()

  def _init(self):
    if not os.path.exists(FORKS_PATH):
      os.mkdir(FORKS_PATH)
    self.params = self.default_params  # start with default params
    if not os.path.exists(FORK_PARAM_PATH):  # if first time running, just write default
      self._write()
      return
    self._read()

  def get(self, key):
    return self.params[key]

  def put(self, key, value):
    self.params.update({key: value})
    self._write()

  def _read(self):
    with open(FORK_PARAM_PATH, "r") as f:
      self.params = json.loads(f.read())

  def _write(self):
    with open(FORK_PARAM_PATH, "w") as f:
      f.write(json.dumps(self.params, indent=2))


class Fork(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'fork'
    self.description = '🍴 manage installed forks, or clone a new one'

    self.fork_params = ForkParams()

    # todo: remove install, add list command, allow switch command to install before switching
    self.commands = {'install': Command(description='🦉 Whoooose fork do you wanna install?',
                                        flags=[Flag(['clone_url'], '🍴 URL of fork to clone', has_value=True),
                                               Flag(['-l', '--lite'], '💡 Clones only the default branch with all commits flattened for quick cloning'),
                                               Flag(['-b', '--branch'], '🌿 Specify the branch to clone after this flag', has_value=True)]),
                     'switch': Command(description='Switch between downloaded openpilot forks',
                                       flags=[Flag('switch_type', 'Switch between branches or forks?', has_value=True)])}

  def _switch(self):
    if not self._init():
      return
    flags, e = self.parse_flags(self.commands['switch'].parser)
    if e is not None:
      error(e)
      return
    if flags.switch_type not in ['fork', 'branch']:
      error('Please specify whether you want to switch between a fork or a branch')
      return

  def _init(self):
    if self.fork_params.get('setup_complete'):
      return True  # already set up
    info('To set up emu fork management we will clone commaai/openpilot into /data/community/forks')
    info('Please confirm you would like to continue')

    if not is_affirmative():
      error('Stopping initialization!')
      return False
    info('Cloning commaai/openpilot into /data/community/forks')
    r = check_output('git clone {} {}'.format(GIT_OPENPILOT_URL, COMMAAI_PATH))
    if not r:
      error('Error while cloning, please try again')
      return False
    self.fork_params.put('setup_complete', True)
    success('Fork management set up successfully!')
    return True

  # def _install(self):  # todo: to be replaced with switch command
  #   if self.next_arg(ingest=False) is None:
  #     error('You must supply command arguments!')
  #     self._help('install')
  #     return
  #
  #   flags, e = self.parse_flags(self.commands['install'].parser)
  #   if e is not None:
  #     error(e)
  #     return
  #
  #   if flags.clone_url is None:
  #     error('You must specify a fork URL to clone!')
  #     return
  #
  #   OPENPILOT_TEMP_PATH = '{}.temp'.format(OPENPILOT_PATH)
  #   if os.path.exists(OPENPILOT_TEMP_PATH):
  #     warning('{} already exists, should it be deleted to continue?'.format(OPENPILOT_TEMP_PATH))
  #     if is_affirmative():
  #       shutil.rmtree(OPENPILOT_TEMP_PATH)
  #     else:
  #       error('Exiting...')
  #       return
  #
  #   # Clone fork to temp folder
  #   warning('Fork will be installed to {}'.format(OPENPILOT_PATH))
  #   clone_flags = []
  #   if flags.lite:
  #     warning('- Performing a lite clone! (--depth 1)')
  #     clone_flags.append('--depth 1')
  #   if flags.branch is not None:
  #     warning('- Only cloning branch: {}'.format(flags.branch))
  #     clone_flags.append('-b {} --single-branch'.format(flags.branch))
  #   if len(clone_flags):
  #     clone_flags.append('')
  #   try:  # catch ctrl+c and clean up after
  #     r = run('git clone {}{} {}'.format(' '.join(clone_flags), flags.clone_url, OPENPILOT_TEMP_PATH))  # clone to temp folder
  #   except:
  #     r = False
  #
  #   # If openpilot.bak exists, determine a good non-exiting path
  #   # todo: make a folder that holds all installed forks and provide an interface of switching between them
  #   bak_dir = '{}.bak'.format(OPENPILOT_PATH)
  #   bak_count = 0
  #   while os.path.exists(bak_dir):
  #     bak_count += 1
  #     bak_dir = '{}.{}'.format(bak_dir, bak_count)
  #
  #   if r:
  #     success('Cloned successfully! Installing fork...')
  #     if os.path.exists(OPENPILOT_PATH):
  #       shutil.move(OPENPILOT_PATH, bak_dir)  # move current installation to old dir
  #     shutil.move(OPENPILOT_TEMP_PATH, OPENPILOT_PATH)  # move new clone temp folder to main installation dir
  #     success("Installed! Don't forget to restart your device")
  #   else:
  #     error('\nError cloning specified fork URL!', end='')
  #     if os.path.exists(OPENPILOT_TEMP_PATH):  # git usually does this for us
  #       error(' Cleaning up...')
  #       shutil.rmtree(OPENPILOT_TEMP_PATH)
  #     else:
  #       print()
