import os
import shutil
import subprocess


class RepoInfo:
  # define any needed files or dirs
  files_powerline = {'.bashrc_powerline': '.bashrc'}
  files = {'.bashrc': '.bashrc'}
  dirs = ['.config']

  home = '/home'  # where to install/copy files above


def main():
  BASEDIR = os.path.dirname(os.path.abspath(__file__))
  try:
    has_powerline = not bool(subprocess.check_call(['powerline-shell'], stdout=subprocess.PIPE))
  except:
    has_powerline = False

  files = RepoInfo.files_powerline if has_powerline else RepoInfo.files
  for file in files:
    copying = '{}/{}'.format(BASEDIR, file)
    to = '{}/{}'.format(RepoInfo.home, files[file])
    shutil.copyfile(copying, to)
    print('Copied {} to {}!'.format(copying, to))


  for dr in RepoInfo.dirs:
    copying = '{}/{}'.format(BASEDIR, dr)
    to = '{}/{}'.format(RepoInfo.home, dr)
    if os.path.exists(to):
      shutil.rmtree(to)

    shutil.copytree(copying, to)
    print('Copied {} to {}!'.format(copying, to))


if __name__ == "__main__":
  print('Running installation...')
  main()
  print('Finished!')
