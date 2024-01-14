import click
from flask import Flask, request, jsonify
import os
import signal
import logging
import requests

from model.api import OAuthTokenResponse

flask_app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@flask_app.route('/oauth/<provider>', methods=['GET'])
def oauth(provider):
    match provider:
        case 'hh':
            code = request.args.get('code', default=None, type=str)
        case _:
            return jsonify({"status": "ERROR", "message": "Wrong provider"})
    if code is None:
        return jsonify({"status": "ERROR", "message": "No code in redirect URI params"})
    flask_app.config['queue'].put(code)

    return jsonify({"status": "SUCCESSFUL"})


@flask_app.teardown_request
def shutdown_process(response):
    os.kill(os.getpid(), signal.SIGINT)


def json_api_factory(response_model: type):
    def json_api(func):
        def json_api_wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if res.status_code == 200:
                return response_model(**res.json())
            else:
                click.echo(click.style(f"Request failed {res.status_code}: {res.json()}", fg='red'))

        return json_api_wrapper

    return json_api


class OAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @json_api_factory(OAuthTokenResponse)
    def token(self, authorization_code: str) -> OAuthTokenResponse:
        url = "https://hh.ru/oauth/token"
        body = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": authorization_code
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        res = requests.post(url, data=body, headers=headers)
        return res

    @json_api_factory(OAuthTokenResponse)
    def refresh_token(self, refresh_token: str) -> OAuthTokenResponse:
        url = "https://hh.ru/oauth/token"
        body = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "refresh_token": refresh_token
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        res = requests.post(url, data=body, headers=headers)
        return res
