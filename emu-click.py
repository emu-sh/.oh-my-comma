import click


@click.group()
def main():
  pass

@main.command()
@click.argument('clone_url')
@click.option(
  '--lite', '-l',
  help='Fast cloning, clones only one branch with all commits flattened',
)
@click.option(
  '--branch', '-b',
  help='Specify the branch to clone, with this flag only that branch is cloned',
)
def installfork(clone_url, lite):
  print(clone_url, lite)


if __name__ == "__main__":
  main()
