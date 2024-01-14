import click
import urllib.parse
from multiprocessing import Process, Queue

from api import flask_app, OAuth
from db import db
from model.client import Client
from repository import ClientRepository

HH_REDIRECT_HOST = "localhost"
HH_REDIRECT_PORT = 1505
HH_REDIRECT_URI = f"http://{HH_REDIRECT_HOST}:{HH_REDIRECT_PORT}/oauth/hh"


def get_oauth_link(client_id: str) -> str:
    url = "https://hh.ru/oauth/authorize?"
    params = {"client_id": client_id,
              "redirect_uri": HH_REDIRECT_URI,
              "response_type": "code"}
    click.echo(url + urllib.parse.urlencode(params))
    return url + urllib.parse.urlencode(params)


def run_server(queue):
    flask_app.config['queue'] = queue
    flask_app.run(HH_REDIRECT_HOST, HH_REDIRECT_PORT, threaded=False, use_reloader=False)


def authorize(client_id: str) -> str:
    queue = Queue()

    server = Process(target=run_server, args=(queue,))
    click.launch(get_oauth_link(client_id))
    server.start()
    server.join()
    authorization_code = queue.get()
    if authorization_code is None:
        raise RuntimeError("No authorization code")
    click.echo(click.style("Authorization code was gotten", fg="green"))
    return authorization_code


def oauth(client_id: str, client_secret: str):
    authorization_code = authorize(client_id)
    oauth_api = OAuth(client_id, client_secret, HH_REDIRECT_URI)
    oauth_token_response = oauth_api.token(authorization_code)

    print(oauth_token_response)
    ClientRepository.upsert(
        Client(
            client_id=client_id,
            client_secret=client_secret,
            access_token=oauth_token_response.access_token,
            token_type=oauth_token_response.token_type,
            refresh_token=oauth_token_response.refresh_token,
            expires_in=oauth_token_response.expires_in
        )
    )



