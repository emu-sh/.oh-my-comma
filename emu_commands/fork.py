import shutil
import os
import json
from emu_commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, error, success, warning, info, is_affirmative, check_output, most_similar
from py_utils.emu_utils import OPENPILOT_PATH, FORKS_PATH, FORK_PARAM_PATH, COLORS


COMMAAI_PATH = FORKS_PATH + '/commaai'
GIT_OPENPILOT_URL = 'https://github.com/commaai/openpilot'

REMOTE_ALREADY_EXISTS = 'already exists'
DEFAULT_BRANCH_START = 'HEAD branch: '
REMOTE_BRANCHES_START = 'Remote branches:'


def valid_fork_url(url):
  import urllib.request
  try:
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    urllib.request.urlopen(request)
    return True
  except Exception as e:
    return False

class ForkParams:
  def __init__(self):
    self.default_params = {'current_fork': None,
                           'installed_forks': {},
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
    self.stock_aliases = ['stock', 'commaai', 'origin']

    # todo: add list command
    self.commands = {'switch': Command(description='🍴 Switch between forks or install a new one',
                                       flags=[Flag('username', '👤 The username of the fork\'s owner to install', required=True, dtype='str'),
                                              Flag('branch', '🌿 Branch to switch to', dtype='str')])}

  def _switch(self):
    if not self._init():
      return
    flags, e = self.parse_flags(self.commands['switch'].parser)
    if e is not None:
      error(e)
      return

    username = flags.username.lower()
    if username in self.stock_aliases:
      username = 'commaai'
      flags.username = 'commaai'

    fork_in_params = True
    if username not in self.fork_params.get('installed_forks'):
      fork_in_params = False
      clone_url = 'https://github.com/{}/openpilot'.format(username)

      if not valid_fork_url(clone_url):
        error('Invalid username! {} does not exist'.format(clone_url))
        return

      r = check_output(['git', '-C', COMMAAI_PATH, 'remote', 'add', username, clone_url])
      if r.success and r.output == '':
        success('Remote added successfully!')
      elif r.success and REMOTE_ALREADY_EXISTS in r.output:
        # remote already added, update params
        info('Fork exists but wasn\'t in params, updating now...')
        installed_forks = self.fork_params.get('installed_forks')
        installed_forks[username] = {'installed_branches': []}
        self.fork_params.put('installed_forks', installed_forks)
      else:
        error(r.output)
        return

    # fork has been added as a remote, switch to it
    # todo: probably should write a function that checks installed forks, but should be fine for now
    if fork_in_params:
      info('Fetching {}\'s latest changes...'.format(flags.username))
    else:
      info('Fetching {}\'s fork, this may take a sec...'.format(flags.username))

    r = check_output(['git', '-C', COMMAAI_PATH, 'fetch', username])
    print(r.output)
    if not r.success:
      error(r.output)
      return

    r = check_output(['git', '-C', COMMAAI_PATH, 'remote', 'show', username])
    remote_branches = self.__get_remote_branches(r)

    if DEFAULT_BRANCH_START not in r.output:
      error('Error: Cannot find default branch from fork!')
      return

    if flags.branch is None:
      start_default_branch = r.output.index(DEFAULT_BRANCH_START)
      default_branch = r.output[start_default_branch+len(DEFAULT_BRANCH_START):]
      end_default_branch = default_branch.index('\n')
      default_branch = default_branch[:end_default_branch]
      fork_branch = '{}_{}'.format(username, default_branch)
      branch = default_branch  # for command to checkout correct branch from remote, branch is previously None since user didn't specify

    elif len(flags.branch) > 0:
      fork_branch = f'{username}_{flags.branch}'
      branch = flags.branch
      if remote_branches is None:
        return
      if branch not in remote_branches:
        error('The branch you specified does not exist!')
        self.__show_similar_branches(branch, remote_branches)  # if possible
        return

    else:
      error('Error with branch!')
      return

    # checkout remote branch and prepend username so we can have multiple forks with same branch names locally
    installed_forks = self.fork_params.get('installed_forks')
    remote_branch = f'{username}/{branch}'
    if branch not in installed_forks[username]['installed_branches']:
      info('New branch! Tracking and checking out {} from {}'.format(fork_branch, remote_branch))
      r = check_output(['git', '-C', COMMAAI_PATH, 'checkout', '--track', '-b', fork_branch, remote_branch])
      if not r.success:
        error(r.output)
        return
      installed_forks[username]['installed_branches'].append(branch)  # we can deduce fork branch from username and original branch f({username}_{branch})
      self.fork_params.put('installed_forks', installed_forks)
    else:  # already installed branch, checking out fork_branch from remote_branch
      r = check_output(['git', '-C', COMMAAI_PATH, 'checkout', fork_branch])
      if not r.success:
        error(r.output)
        return

    success('Successfully checked out {}/{} as {}'.format(flags.username, branch, fork_branch))

  def __show_similar_branches(self, branch, branches):
    if len(branches) > 0:
      info('Did you mean:')
      close_branches = most_similar(branch, branches)[:5]
      for idx in range(len(close_branches)):
        cb = close_branches[idx]
        if idx == 0:
          cb = COLORS.OKGREEN + cb
        else:
          cb = COLORS.CYAN + cb
        print(' - {}{}'.format(cb, COLORS.ENDC))

  def __get_remote_branches(self, r):
    # get remote's branches to verify from output of command in parent function
    if not r.success:
      error(r.output)
      return
    start_remote_branches = r.output.index(REMOTE_BRANCHES_START)
    remote_branches_txt = r.output[start_remote_branches + len(REMOTE_BRANCHES_START):].split('\n')
    remote_branches = []
    for b in remote_branches_txt[1:]:  # remove first useless line
      b = b.replace('tracked', '').strip()
      if ' ' in b:  # end of branches
        break
      remote_branches.append(b)
    if len(remote_branches) == 0:
      error('Error getting remote branches!')
      return
    return remote_branches

  def _reset_hard(self):  # todo: this functionality
    # to reset --hard with this repo structure, we need to give it the actual remote's branch name, not with username prepended. like:
    # git reset --hard arne182/075-clean
    pass

  def _init(self):
    if self.fork_params.get('setup_complete'):
      if os.path.exists(COMMAAI_PATH):  # ensure we're really set up (directory got deleted?)
        branches = check_output(['git', '-C', COMMAAI_PATH, 'branch'])
        if branches.success and 'master' in branches.output:
          return True  # already set up
      self.fork_params.put('setup_complete', False)  # some error with base origin, reclone
      warning('There was an error with your clone of commaai/openpilot, restarting initialization!')
      shutil.rmtree(COMMAAI_PATH)  # clean slate

    info('To set up emu fork management we will clone commaai/openpilot into /data/community/forks')
    info('Please confirm you would like to continue')
    if not is_affirmative():
      error('Stopping initialization!')
      return

    info('Cloning commaai/openpilot into /data/community/forks, please wait...')
    r = check_output(['git', 'clone', GIT_OPENPILOT_URL, COMMAAI_PATH, '--depth', '1'])
    print('output: {}'.format(r.output))  # todo: remove, just need to see the output of without depth 1
    if not r.success or 'done' not in r.output:
      error('Error while cloning, please try again')
      return

    # so it's easy to switch to stock without any extra logic for origin
    r = check_output(['git', '-C', COMMAAI_PATH, 'remote', 'rename', 'origin', 'commaai'])
    print(r.output)
    print(r.success)
    if not r.success:
      error(r.output)
      return
    self.fork_params.put('setup_complete', True)
    success('Fork management set up successfully!')
