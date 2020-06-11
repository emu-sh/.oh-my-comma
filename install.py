import os
import shutil


class RepoInfo:
  # define any needed files or dirs needed
  files = ['.bashrc']
  dirs = ['.config']

  home = '/home'  # where to install/copy files above


def main():
  BASEDIR = os.path.dirname(os.path.abspath(__file__))
  for file in RepoInfo.files:
    copying = '{}/{}'.format(BASEDIR, file)
    to = '{}/{}'.format(RepoInfo.home, file)
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
