import os
import subprocess
from install import main as install


def main():
  if not os.path.exists('/home/comma-dotfiles'):
    raise Exception('Please run install.py first!')

  r = subprocess.check_call(['cd', '/home/comma-dotfiles'])
  print(str(r))
  r = subprocess.check_call(['git', 'pull'])
  print(str(r))
  print('Updated successfully!')
  install()


if __name__ == "__main__":
  print('Running update...')
  main()
  print('Finished!')
