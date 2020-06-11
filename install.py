import os
import shutil


class RepoInfo:
  # define any needed files or dirs needed
  files = ['.bashrc']
  dirs = ['.config']

  basedir = '/home'  # where to install/copy files above


def main():
  basedir = os.getcwd()
  for file in RepoInfo.files:
    print('{}/{}'.format(basedir, file))
    shutil.copyfile('{}/{}'.format(basedir, file), basedir)


if __name__ == "__main__":
  main()
