import os
import click


class Repo(object):
  def __init__(self, home=None, debug=False):
    self.home = os.path.abspath(home or '.')
    self.debug = debug


@click.group()
@click.option('--repo-home', envvar='REPO_HOME', default='.repo')
@click.option('--debug/--no-debug', default=False,
              envvar='REPO_DEBUG')
@click.pass_context
def cli(ctx, repo_home, debug):
  ctx.obj = Repo(repo_home, debug)
