import click
import os
import docspace


@click.command()
@click.option('--reset/--no-reset', default=False, help='Delete existing group keys in config')
def configure(reset):
    """Configure resource and authentication keys"""
    docspace.config.update(None, reset)


@click.command()
@click.option('--debug/--no-debug', default=None, help='Override debug config')
def run(debug):
    """Run a local server of the docspace app"""
    script_path = docspace.app.project.settings.BASE_DIR / 'manage.py'
    cmd = f"python {script_path} runserver"
    if debug is not None:
        cmd = "DEBUG=" + str(int(debug)) + " " + cmd
    os.system(cmd)


@click.group()
def main():
    pass


main.add_command(configure)
main.add_command(run)


if __name__ == '__main__':
    main()
