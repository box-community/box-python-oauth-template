""" Manage oAuth2 for Box"""
from boxsdk import OAuth2
from app.config import AppConfig

import webbrowser


def get_oauth(config: AppConfig) -> OAuth2:
    """Returns a boxsdk OAuth2 object"""
    oauth = OAuth2(
        client_id=config.client_id,
        client_secret=config.client_secret,
    )
    return oauth


def open_browser(auth_url: str):
    """Opens a browser to the auth_url"""
    webbrowser.open(auth_url)
