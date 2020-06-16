import click

@click.command()
@click.argument('location')
@click.option(
    '--api-key', '-a',
    help='your API key for the OpenWeatherMap API',
)
def main(location, api_key):
    print(location, api_key)


if __name__ == "__main__":
    main()
