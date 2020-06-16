import psutil
import requests
import subprocess
from py_utils.colors import COLORS


SYSTEM_BASHRC_PATH = '/home/.bashrc'
COMMUNITY_PATH = '/data/community'
COMMUNITY_BASHRC_PATH = '/data/community/.bashrc'
OH_MY_COMMA_PATH = '/data/community/.oh-my-comma'
UPDATE_PATH = '{}/update.sh'.format(OH_MY_COMMA_PATH)
OPENPILOT_PATH = '/data/openpilot'

def run(cmd, out_file=None):
  """
  If cmd is a string, it is split into a list, otherwise it doesn't modify cmd.
  The status is returned, True being success, False for failure
  """
  if isinstance(cmd, str):
    cmd = cmd.split()

  f = None
  if isinstance(out_file, str):
    f = open(out_file, 'a')

  try:
    r = subprocess.call(cmd, stdout=f)
    return not r
  except Exception as e:
    print(e)
    return False

def kill(procname):
  for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == procname:
      proc.kill()
      return True
  return None

def is_affirmative():
  i = None
  print(COLORS.PROMPT)
  while i not in ['y', 'n', 'yes', 'no']:
    i = input('[Y/n]: ').lower().strip()
  print(COLORS.ENDC)
  return i in ['y', 'yes']

def error(msg, end='\n'):
  print('{}{}{}'.format(COLORS.FAIL, msg, COLORS.ENDC), end=end)

def warning(msg, end='\n'):
  print('{}{}{}'.format(COLORS.WARNING, msg, COLORS.ENDC), end=end)

def success(msg, end='\n'):
  print('{}{}{}'.format(COLORS.SUCCESS, msg, COLORS.ENDC), end=end)

def verify_fork_url(url):
  if url[:4].lower() != 'http':
    url = 'http://' + url
  try:
    return requests.get(url).status_code == 200
  except:
    return False
