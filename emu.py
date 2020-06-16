import click


@click.group()
def main():
  pass

@main.command()
@click.argument('location')
@click.option(
  '--api-key', '-a',
  help='your API key for the OpenWeatherMap API',
)
def current(location, api_key):
  pass
