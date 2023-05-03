""" Manage oAuth2 for Box"""
from datetime import datetime, timedelta
import json
import os.path
from boxsdk import OAuth2
from app.config import AppConfig


def oauth_from_config(config: AppConfig) -> OAuth2:
    """
    Returns a boxsdk OAuth2 object
    from the configuration file
    """
    return OAuth2(
        client_id=config.client_id,
        client_secret=config.client_secret,
        store_tokens=store_tokens,
    )


def store_tokens(access_token: str, refresh_token: str):
    """Stores the access and refresh tokens in a file"""
    access_token_expires_on = datetime.today() + timedelta(minutes=60)
    refresh_token_expires_on = datetime.today() + timedelta(days=60)
    oauth_json = {
        "access_token": access_token,
        "access_token_expires_on": str(access_token_expires_on),
        "refresh_token": refresh_token,
        "refresh_token_expires_on": str(refresh_token_expires_on),
    }
    with open(".oauth.json", "w", encoding="UTF-8") as file:
        file.write(json.dumps(oauth_json, indent=4))


def oauth_from_previous() -> OAuth2:
    """
    Returns an OAuth2 object
    Instatiated from the .oauth.json file
    and the configurations
    """

    oauth = oauth_from_config(AppConfig())
    if not os.path.isfile(".oauth.json"):
        return oauth

    with open(".oauth.json", "r", encoding="UTF-8") as file:
        oauth_json = file.read()

    oauth_dict = json.loads(oauth_json)

    oauth = OAuth2(
        client_id=AppConfig().client_id,
        client_secret=AppConfig().client_secret,
        store_tokens=store_tokens,
        access_token=oauth_dict.get("access_token"),
        refresh_token=oauth_dict.get("refresh_token"),
    )

    return oauth


def oauth_authenticate(code: str):
    """
    Retreives the access and refresh tokens
    from using the code obtained from the first leg
    of the oAuth2 process
    """
    oauth = oauth_from_config(AppConfig())
    oauth.authenticate(code)
