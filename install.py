import os
import shutil


class RepoInfo:
  # define any needed files or dirs needed
  files = ['.bashrc']
  dirs = ['.config']

  basedir = '/home'  # where to install/copy files above


def main():
  # basedir = os.getcwd()
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  for file in RepoInfo.files:
    print(file)
    shutil.copyfile(file, RepoInfo.basedir)


if __name__ == "__main__":
  main()
