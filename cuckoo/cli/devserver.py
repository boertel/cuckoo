import os
import socket
import click
import sys

from subprocess import list2cmdline
from honcho.manager import Manager

from .base import cli

DEFAULT_HOST_NAME = socket.gethostname().split('.', 1)[0].lower()


@cli.command()
@click.option('--port', '-p', default=3002)
@click.option('--workers/--no-workers', default=False)
@click.option('--ngrok/--no-ngrok', default=False)
@click.option('--ngrok-domain', default='cuckoo-{}'.format(DEFAULT_HOST_NAME))
def devserver(port, workers, ngrok, ngrok_domain):
    os.environ.setdefault('FLASK_DEBUG', '1')

    if ngrok:
        os.environ['SERVER_NAME'] = '{}.ngrok.io'.format(ngrok_domain)
        root_url = 'https://{}'.format(os.environ['SERVER_NAME'])
        os.environ['SSL'] = '1'
    else:
        root_url = 'http://localhost:{}'.format(port)

    click.echo('Launching Cuckoo on {}'.format(root_url))

    daemons = [
        ('web', ['cuckoo', 'run', '--port={}'.format(port)]),
    ]

    if workers:
        daemons.append(
            ('worker', ['cuckoo', 'worker', '--cron', '--log-level=INFO']),
        )

    if ngrok:
        daemons.append(
            ('ngrok', ['ngrok', 'http',
                       '-subdomain={}'.format(ngrok_domain), str(port)])
        )

    cwd = os.path.realpath(os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir))

    manager = Manager()
    for name, cmd in daemons:
        manager.add_process(
            name,
            list2cmdline(cmd),
            quiet=False,
            cwd=cwd,
        )

    manager.loop()
    sys.exit(manager.returncode)
