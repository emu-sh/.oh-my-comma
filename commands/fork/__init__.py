import shutil
import os
import json
from commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, error, success, warning, info, is_affirmative, check_output, most_similar
from py_utils.emu_utils import OPENPILOT_PATH, FORK_PARAM_PATH, COLORS

GIT_OPENPILOT_URL = 'https://github.com/commaai/openpilot'
COMMA_ORIGIN_NAME = 'commaai'
COMMA_DEFAULT_BRANCH = 'release2'

REMOTE_ALREADY_EXISTS = 'already exists'
DEFAULT_BRANCH_START = 'HEAD branch: '
REMOTE_BRANCHES_START = 'Remote branches:'
REMOTE_BRANCH_START = 'Remote branch:'


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
                           'current_branch': None,
                           'installed_forks': {},
                           'setup_complete': False}
    self._init()

  def _init(self):
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

  def reset(self):
    self.params = self.default_params
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
    self.description = '🍴 Manage installed forks, or install a new one'

    self.fork_params = ForkParams()
    self.stock_aliases = ['stock', COMMA_ORIGIN_NAME, 'origin']

    self.commands = {'switch': Command(description='🍴 Switch between any openpilot fork',
                                       flags=[Flag('username', '👤 The username of the fork\'s owner to install', required=False, dtype='str'),
                                              Flag(['-b', '--branch'], '🌿 Branch to switch to, will use default branch if not provided', required=False, dtype='str')]),
                     'list': Command(description='📜 See a list of installed forks and branches',
                                     flags=[Flag('fork', '🌿 See branches of specified fork', dtype='str')])}

  def _list(self):
    if not self._init():
      return
    flags, e = self.parse_flags(self.commands['list'].parser)
    if e is not None:
      error(e)
      self._help('list')
      return

    installed_forks = self.fork_params.get('installed_forks')
    if flags.fork is None:
      max_branches = 4  # max branches to display per fork when listing all forks
      success('Installed forks:')
      for idi, fork in enumerate(installed_forks):
        print('- {}{}{}'.format(COLORS.OKBLUE, fork, COLORS.ENDC), end='')
        current_fork = self.fork_params.get('current_fork')
        if current_fork == fork:
          print(' (current)')
        else:
          print()
        branches = installed_forks[fork]['installed_branches']
        current_branch = self.fork_params.get('current_branch')
        if current_branch in branches:
          branches.remove(current_branch)
          branches.insert(0, current_branch)  # move cur_branch to beginning

        if len(branches) > 0:
          success('   Branches:')
        for idx, branch in enumerate(branches):
          if idx < max_branches:
            print('   - {}{}{}'.format(COLORS.RED, branch, COLORS.ENDC), end='')
            if branch == current_branch and fork == current_fork:
              print(' (current)')
            else:
              print()
          else:
            print('   - {}...see more branches: {}emu fork list {}{}'.format(COLORS.RED, COLORS.CYAN, fork, COLORS.ENDC))
            break
        print()
    else:
      fork = flags.fork.lower()
      if fork in self.stock_aliases:
        fork = COMMA_ORIGIN_NAME
        flags.fork = COMMA_ORIGIN_NAME
      if fork not in installed_forks:
        error('{} not an installed fork! Try installing it with the {}switch{} command'.format(fork, COLORS.CYAN, COLORS.RED))
        return
      installed_branches = installed_forks[fork]['installed_branches']
      success('Installed branches for {}:'.format(flags.fork))
      for branch in installed_branches:
        print(' - {}{}{}'.format(COLORS.RED, branch, COLORS.ENDC))


  def _switch(self):
    if not self._init():
      return
    flags, e = self.parse_flags(self.commands['switch'].parser)
    if e is not None:
      error(e)
      self._help('switch')
      return
    else:  # since both are non-required we need custom logic to check user supplied sufficient args/flags
      if flags.username is flags.branch is None:
        error('You must supply either username or branch or both!')
        self._help('switch')
        return

    if flags.username is None:  # branch is specified, so use current checked out fork/username
      _current_fork = self.fork_params.get('current_fork')
      if _current_fork is not None:  # ...if available
        success('No username specified, using current fork: {}'.format(_current_fork))
        flags.username = _current_fork
      else:
        error('Current fork is unknown, please switch to a fork first before switching between branches!')
        return

    username = flags.username.lower()
    if username in self.stock_aliases:
      username = COMMA_ORIGIN_NAME
      flags.username = COMMA_ORIGIN_NAME

    installed_forks = self.fork_params.get('installed_forks')
    fork_in_params = True
    if username not in installed_forks:
      fork_in_params = False
      remote_url = 'https://github.com/{}/openpilot'.format(username)

      if not valid_fork_url(remote_url):
        error('Invalid username! {} does not exist'.format(remote_url))
        return

      r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'add', username, remote_url])
      if r.success and r.output == '':
        success('Remote added successfully!')
      elif r.success and REMOTE_ALREADY_EXISTS in r.output:
        # remote already added, update params
        info('Fork exists but wasn\'t in params, updating now...')
        self.__add_fork(username)
      else:
        error(r.output)
        return

    # fork has been added as a remote, switch to it
    if fork_in_params:
      info('Fetching {}\'s latest changes...'.format(flags.username))
    else:
      info('Fetching {}\'s fork, this may take a sec...'.format(flags.username))

    r = check_output(['git', '-C', OPENPILOT_PATH, 'fetch', username])
    if not r.success:
      error(r.output)
      return
    self.__add_fork(username)

    r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'show', username])
    remote_branches, default_remote_branch = self.__get_remote_branches(r)
    if remote_branches is None:
      return

    if DEFAULT_BRANCH_START not in r.output:
      error('Error: Cannot find default branch from fork!')
      return

    if flags.branch is None:  # user hasn't specified a branch, use remote's default branch
      if username == COMMA_ORIGIN_NAME:  # todo: use a dict for default branches if we end up needing default branches for multiple forks
        branch = COMMA_DEFAULT_BRANCH  # use release2 and default branch for stock
        fork_branch = 'commaai_{}'.format(branch)
      else:
        fork_branch = '{}_{}'.format(username, default_remote_branch)
        branch = default_remote_branch  # for command to checkout correct branch from remote, branch is previously None since user didn't specify

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
    remote_branch = f'{username}/{branch}'
    if branch not in installed_forks[username]['installed_branches']:
      info('New branch! Tracking and checking out {} from {}'.format(fork_branch, remote_branch))
      r = check_output(['git', '-C', OPENPILOT_PATH, 'checkout', '--track', '-b', fork_branch, remote_branch])
      if not r.success:
        error(r.output)
        return
      self.__add_branch(username, branch)  # we can deduce fork branch from username and original branch f({username}_{branch})
    else:  # already installed branch, checking out fork_branch from remote_branch
      r = check_output(['git', '-C', OPENPILOT_PATH, 'checkout', fork_branch])
      if not r.success:
        error(r.output)
        return
    # reset to remote/branch just to ensure we checked out fully. if remote branch has been force pushed, this will also reset local to remote
    r = check_output(['git', '-C', OPENPILOT_PATH, 'reset', '--hard', remote_branch])
    if not r.success:
      error(r.output)
      return
    self.fork_params.put('current_fork', username)
    self.fork_params.put('current_branch', branch)
    success('Successfully checked out {}/{} as {}'.format(flags.username, branch, fork_branch))

  def __add_fork(self, username):
    installed_forks = self.fork_params.get('installed_forks')
    if username not in installed_forks:
      installed_forks[username] = {'installed_branches': []}
      self.fork_params.put('installed_forks', installed_forks)

  def __add_branch(self, username, branch):  # assumes fork exists in params
    installed_forks = self.fork_params.get('installed_forks')
    installed_forks[username]['installed_branches'].append(branch)
    self.fork_params.put('installed_forks', installed_forks)

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
      return None, None
    if REMOTE_BRANCHES_START in r.output:
      start_remote_branches = r.output.index(REMOTE_BRANCHES_START)
      remote_branches_txt = r.output[start_remote_branches + len(REMOTE_BRANCHES_START):].split('\n')
      remote_branches = []
      for b in remote_branches_txt[1:]:  # remove first useless line
        b = b.replace('tracked', '').strip()
        if ' ' in b:  # end of branches
          break
        remote_branches.append(b)
    elif REMOTE_BRANCH_START in r.output:  # remote has single branch
      start_remote_branch = r.output.index(REMOTE_BRANCH_START)
      remote_branches = r.output[start_remote_branch + len(REMOTE_BRANCH_START):].split('\n')
      remote_branches = [b.replace('tracked', '').strip() for b in remote_branches if b.strip() != '' and 'tracked' in b]
    else:
      error('Unable to parse remote branches!')
      return None, None

    if len(remote_branches) == 0:
      error('Error getting remote branches!')
      return None, None

    start_default_branch = r.output.index(DEFAULT_BRANCH_START)  # get default branch to return
    default_branch = r.output[start_default_branch + len(DEFAULT_BRANCH_START):]
    end_default_branch = default_branch.index('\n')
    default_branch = default_branch[:end_default_branch]
    return remote_branches, default_branch

  # def _reset_hard(self):  # todo: this functionality
  #   # to reset --hard with this repo structure, we need to give it the actual remote's branch name, not with username prepended. like:
  #   # git reset --hard arne182/075-clean
  #   pass

  def _init(self):
    if os.path.isdir('/data/community/forks'):
      shutil.rmtree('/data/community/forks')  # remove to save space
    if self.fork_params.get('setup_complete'):
      if os.path.exists(OPENPILOT_PATH):
        r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'show'])
        if COMMA_ORIGIN_NAME in r.output.split('\n'):  # sign that we're set up correctly
          return True
      self.fork_params.put('setup_complete', False)  # some error with base origin, reclone
      self.fork_params.reset()
    warning('There was an error with your clone of commaai/openpilot, restarting initialization!')

    info('To set up emu fork management we will clone commaai/openpilot into {}'.format(OPENPILOT_PATH))
    info('Confirm you would like to continue')
    if not is_affirmative():
      error('Stopping initialization!')
      return

    # backup openpilot here to free up /data/openpilot
    if os.path.exists(OPENPILOT_PATH):
      bak_dir = '{}.bak'.format(OPENPILOT_PATH)
      idx = 0
      while os.path.exists(bak_dir):
        bak_dir = '{}{}'.format(bak_dir, idx)
        idx += 1
      shutil.move(OPENPILOT_PATH, bak_dir)
      success('Backed up your current openpilot install to {}'.format(bak_dir))

    info('Cloning commaai/openpilot into {}, please wait...'.format(OPENPILOT_PATH))
    r = run(['git', 'clone', '-b', COMMA_DEFAULT_BRANCH, GIT_OPENPILOT_URL, OPENPILOT_PATH])  # default to r2 for stock
    if not r:
      error('Error while cloning, please try again')
      return

    # rename origin to commaai so it's easy to switch to stock without any extra logic for url checking, etc
    r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'rename', 'origin', COMMA_ORIGIN_NAME])
    if not r.success:
      error(r.output)
      return

    success('Fork management set up successfully! You\'re on {}/{}'.format(COMMA_ORIGIN_NAME, COMMA_DEFAULT_BRANCH))
    success('To get started, try running: {}emu fork switch [fork_username] (branch){}'.format(COLORS.RED, COLORS.ENDC))
    self.fork_params.put('setup_complete', True)
    self.fork_params.put('current_fork', COMMA_ORIGIN_NAME)
    self.fork_params.put('current_branch', COMMA_DEFAULT_BRANCH)
    self.__add_fork(COMMA_ORIGIN_NAME)
