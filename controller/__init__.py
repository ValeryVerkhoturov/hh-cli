import click
import service


@click.group()
@click.version_option()
def cli():
    pass


@click.command()
@click.option('-I', '--client-id', prompt='Client ID')
@click.option('-S', '--client-secret', prompt='Client secret')
def oauth(client_id: str, client_secret: str):
    service.oauth(client_id, client_secret)


cli.add_command(oauth)
