import click
import docspace


@click.command()
@click.option('--reset/--no-reset', default=False, help='Delete existing group keys in config')
def configure(reset):
    """Configure resource and authentication keys"""
    docspace.config.update(None, reset)


@click.group()
def main():
    pass


main.add_command(configure)


if __name__ == '__main__':
    main()
