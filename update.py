import os
import subprocess
from install import main as install


def main():
  if not os.path.exists('/home/comma-dotfiles'):
    raise Exception('Please install to /home/comma-dotfiles!')

  os.chdir('/home/comma-dotfiles')

  try:
    update_success = not bool(subprocess.check_call(['git', 'pull'], stdout=subprocess.PIPE))
  except:
    update_success = False

  if update_success:
    # print('Updated successfully!')
    install()
  else:
    raise Exception('Error with git pull!')


if __name__ == "__main__":
  print('Running update...')
  main()
  print('Finished!')
