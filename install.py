import os
import shutil
import subprocess


class RepoInfo:
  # define any needed files or dirs
  files = ['.bashrc', '.powerline']
  dirs = ['.config']
  req = files + dirs

  home = '/home'  # where to install/copy files above


def main():
  BASEDIR = os.path.dirname(os.path.abspath(__file__))
  info = RepoInfo()

  for req in info.req:
    copying = '{}/{}'.format(BASEDIR, req)
    to = '{}/{}'.format(RepoInfo.home, req)
    if req in info.files:
      shutil.copyfile(copying, to)
      print('Copied file {} to {}!'.format(copying, to))
    elif req in info.dirs:
      if os.path.exists(to):
        shutil.rmtree(to)

      shutil.copytree(copying, to)
      print('Copied directory {} to {}!'.format(copying, to))


if __name__ == "__main__":
  print('Running installation...')
  main()
  print('\nFinished! Remember to reconnect to finish the install/update.')
