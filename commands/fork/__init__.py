#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil
import os
import json
from datetime import datetime
from commands.base import CommandBase, Command, Flag
from py_utils.emu_utils import run, error, success, warning, info, is_affirmative, check_output, most_similar, TimeDebugger
from py_utils.emu_utils import OPENPILOT_PATH, FORK_PARAM_PATH, COLORS, OH_MY_COMMA_PATH

GIT_OPENPILOT_URL = 'https://github.com/commaai/openpilot'
REMOTE_ALREADY_EXISTS = 'already exists'
DEFAULT_BRANCH_START = 'HEAD branch: '
REMOTE_BRANCHES_START = 'Remote branches:\n'
REMOTE_BRANCH_START = 'Remote branch:'
CLONING_PATH = '{}/.cloning'.format(OH_MY_COMMA_PATH)


def set_cloning(cloning):
  if cloning:
    if not os.path.exists(CLONING_PATH):
      with open(CLONING_PATH, 'w') as f:
        pass
  else:
    if os.path.exists(CLONING_PATH):
      os.remove(CLONING_PATH)


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
                           'last_prune': None,
                           'setup_complete': False}
    self._init()

  def _init(self):
    if os.path.exists(FORK_PARAM_PATH):
      try:
        self._read()
        for param in self.default_params:
          if param not in self.params:
            self.params[param] = self.default_params[param]
        return
      except:
        pass

    self.params = self.default_params  # default params
    self._write()  # failed to read, just write default

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


class RemoteInfo:
  def __init__(self, fork_name, username_aliases, default_branch):
    self.username = None  # to be added by Fork.__get_remote_info function
    self.fork_name = fork_name
    self.username_aliases = username_aliases
    self.default_branch = default_branch


class Fork(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'fork'
    self.description = '🍴 Manage installed forks, or install a new one'

    self.fork_params = ForkParams()
    self.remote_defaults = {'commaai': RemoteInfo('openpilot', ['stock', 'origin'], 'release2'),
                            'dragonpilot-community': RemoteInfo('dragonpilot', ['dragonpilot'], 'devel-i18n')}  # devel-i18n isn't most stable, but its name remains the same

    self.comma_origin_name = 'commaai'
    self.comma_default_branch = self.remote_defaults['commaai'].default_branch

    self.commands = {'switch': Command(description='🍴 Switch between any openpilot fork',
                                       flags=[Flag('username', '👤 The username of the fork\'s owner to switch to, will use current fork if not provided', required=False, dtype='str'),
                                              Flag(['-b', '--branch'], '🌿 Branch to switch to, will use default branch if not provided', required=False, dtype='str')]),
                     'list': Command(description='📜 See a list of installed forks and branches',
                                     flags=[Flag('fork', '🌿 See branches of specified fork', dtype='str')])}

  def _list(self):
    if not self._init():
      return
    flags, e = self.parse_flags(self.commands['list'].parser)
    specified_fork = flags.fork
    if e is not None:
      error(e)
      self._help('list')
      return

    installed_forks = self.fork_params.get('installed_forks')
    if specified_fork is None:
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
      specified_fork = specified_fork.lower()
      remote_info = self.__get_remote_info(specified_fork)
      if remote_info is not None:  # there's an overriding default username available
        specified_fork = remote_info.username
      if specified_fork not in installed_forks:
        error('{} not an installed fork! Try installing it with the {}switch{} command'.format(specified_fork, COLORS.CYAN, COLORS.RED))
        return
      installed_branches = installed_forks[specified_fork]['installed_branches']
      success('Installed branches for {}:'.format(specified_fork))
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
        error('You must supply either username or branch or both')
        self._help('switch')
        return

    username = flags.username
    branch = flags.branch
    if username is None:  # branch is specified, so use current checked out fork/username
      _current_fork = self.fork_params.get('current_fork')
      if _current_fork is not None:  # ...if available
        info('Assuming current fork for username: {}'.format(COLORS.SUCCESS + _current_fork + COLORS.ENDC))
        username = _current_fork
      else:
        error('Current fork is unknown, please switch to a fork first before switching between branches!')
        return

    username = username.lower()
    remote_info = self.__get_remote_info(username)
    if remote_info is not None:  # user entered an alias (ex. stock, dragonpilot)
      username = remote_info.username

    installed_forks = self.fork_params.get('installed_forks')
    fork_in_params = True
    if username not in installed_forks:
      fork_in_params = False
      if remote_info is not None:
        remote_url = f'https://github.com/{username}/{remote_info.fork_name}'  # dragonpilot doesn't have a GH redirect
      else:  # for most forks, GH will redirect from /openpilot if user renames fork
        remote_url = f'https://github.com/{username}/openpilot'

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
      info('Fetching {}\'s latest changes...'.format(COLORS.SUCCESS + username + COLORS.WARNING))
    else:
      info('Fetching {}\'s fork, this may take a sec...'.format(COLORS.SUCCESS + username + COLORS.WARNING))

    td = TimeDebugger('ms', silent=False)
    r = run(['git', '-C', OPENPILOT_PATH, 'fetch', username])
    td.print('git fetch')
    if not r:
      error('Error while fetching remote, please try again')
      return
    td.reset()
    self.__add_fork(username)
    td.print('__add_fork function')
    self.fork_params.put('last_prune', '16')
    self.__prune_remote_branches(username)
    td.print('prune remote branches')
    r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'show', username])
    td.print('remote show')
    remote_branches, default_remote_branch = self.__get_remote_branches(r)
    td.print('__get_remote_branches')
    td.print(total=True)
    if remote_branches is None:
      return

    if DEFAULT_BRANCH_START not in r.output:
      error('Error: Cannot find default branch from fork!')
      return

    if branch is None:  # user hasn't specified a branch, use remote's default branch
      if remote_info is not None:  # there's an overriding default branch specified
        remote_branch = remote_info.default_branch
        local_branch = '{}_{}'.format(remote_info.username, remote_branch)
      else:
        local_branch = '{}_{}'.format(username, default_remote_branch)
        remote_branch = default_remote_branch  # for command to checkout correct branch from remote, branch is previously None since user didn't specify
    elif len(branch) > 0:
      local_branch = f'{username}_{branch}'
      remote_branch = branch
      if remote_branch not in remote_branches:
        error('The branch you specified does not exist!')
        self.__show_similar_branches(remote_branch, remote_branches)  # if possible
        return
    else:
      error('Error with branch!')
      return

    # checkout remote branch and prepend username so we can have multiple forks with same branch names locally
    if remote_branch not in installed_forks[username]['installed_branches']:
      info('New branch! Tracking and checking out {} from {}'.format(local_branch, f'{username}/{remote_branch}'))
      r = run(['git', '-C', OPENPILOT_PATH, 'checkout', '--track', '-b', local_branch, f'{username}/{remote_branch}'])
      if not r:
        error('Error while checking out branch, please try again')
        return
      self.__add_branch(username, remote_branch)  # we can deduce fork branch from username and original branch f({username}_{branch})
    else:  # already installed branch, checking out fork_branch from f'{username}/{branch}'
      r = check_output(['git', '-C', OPENPILOT_PATH, 'checkout', local_branch])
      if not r.success:
        error(r.output)
        return
    # reset to remote/branch just to ensure we checked out fully. if remote branch has been force pushed, this will also reset local to remote
    r = check_output(['git', '-C', OPENPILOT_PATH, 'reset', '--hard', f'{username}/{remote_branch}'])
    if not r.success:
      error(r.output)
      return
    self.fork_params.put('current_fork', username)
    self.fork_params.put('current_branch', remote_branch)
    success('Successfully checked out {}/{} as {}'.format(username, remote_branch, local_branch))

  def __add_fork(self, username, branch=None):
    installed_forks = self.fork_params.get('installed_forks')
    if username not in installed_forks:
      installed_forks[username] = {'installed_branches': []}
      if branch is not None:
        installed_forks[username]['installed_branches'].append(branch)
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

  def __prune_remote_branches(self, username):  # remove deleted remote branches locally
    # TODO: Limit this operation to once every day. Takes about 300 ms every switch command
    last_prune = self.fork_params.get('last_prune')
    if isinstance(last_prune, str) and datetime.now().strftime("%d") == last_prune:
      print('not pruning, still same day')
      return
    print('days different, pruning!')

    r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'prune', username, '--dry-run'])
    if r.output == '':  # nothing to prune
      return
    branches_to_prune = [b.strip() for b in r.output.split('\n') if 'would prune' in b]
    branches_to_prune = [b[b.index(username):] for b in branches_to_prune]

    error('\nDeleted remote branches detected:')
    for b in branches_to_prune:
      print(COLORS.CYAN + '  - {}'.format(b) + COLORS.ENDC)
    warning('\nWould you like to delete them locally?')
    if is_affirmative():
      r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'prune', username])
      if r.success:
        success('Pruned local branches successfully!')
      else:
        error('Please try again, something went wrong:')
        print(r.output)

    self.fork_params.put('last_prune', datetime.now().strftime("%d"))

  def __get_remote_info(self, username):
    for default_username in self.remote_defaults:
      remote_info = self.remote_defaults[default_username]
      remote_info.username = default_username  # add dict key to class instance so we don't have to return a tuple
      remote_info.username_aliases.append(default_username)  # so default branch works when user enters the actual name
      if username in remote_info.username_aliases:
        return remote_info
    return None

  @staticmethod
  def __get_remote_branches(r):
    # get remote's branches to verify from output of command in parent function
    if not r.success:
      error(r.output)
      return None, None
    if REMOTE_BRANCHES_START in r.output:
      start_remote_branches = r.output.index(REMOTE_BRANCHES_START)
      remote_branches_txt = r.output[start_remote_branches + len(REMOTE_BRANCHES_START):].split('\n')
      remote_branches = []
      for b in remote_branches_txt:
        b = b.replace('tracked', '').strip()
        if 'stale' in b:  # support stale/to-be-pruned branches
          b = b.split(' ')[0].split('/')[-1]
        if ' ' in b or b == '':  # end of branches
          break
        remote_branches.append(b)
    elif REMOTE_BRANCH_START in r.output:  # remote has single branch, shouldn't need to handle stale here
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
        if self.comma_origin_name in r.output.split('\n'):  # sign that we're set up correctly todo: check all forks exist as remotes
          return True
      self.fork_params.put('setup_complete', False)  # renamed origin -> commaai does not exist, restart setup
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
    set_cloning(True)  # don't git fetch on new sessions
    r = run(['git', 'clone', '-b', self.comma_default_branch, GIT_OPENPILOT_URL, OPENPILOT_PATH])  # default to stock/release2 for setup
    set_cloning(False)
    if not r:
      error('Error while cloning, please try again')
      return

    # rename origin to commaai so it's easy to switch to stock without any extra logic for url checking, etc
    r = check_output(['git', '-C', OPENPILOT_PATH, 'remote', 'rename', 'origin', self.comma_origin_name])
    if not r.success:
      error(r.output)
      return
    # rename release2 to commaai_release2 to align with emu fork standards
    check_output(['git', '-C', OPENPILOT_PATH, 'branch', '-m', f'{self.comma_origin_name}_{self.comma_default_branch}'])

    success('Fork management set up successfully! You\'re on {}/{}'.format(self.comma_origin_name, self.comma_default_branch))
    success('To get started, try running: {}emu fork switch (username) [-b BRANCH]{}'.format(COLORS.RED, COLORS.ENDC))
    self.__add_fork(self.comma_origin_name, self.comma_default_branch)
    self.fork_params.put('setup_complete', True)
    self.fork_params.put('current_fork', self.comma_origin_name)
    self.fork_params.put('current_branch', self.comma_default_branch)
    return True
