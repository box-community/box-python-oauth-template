"""
Handles the box client object creation
orchestrates the authentication process
"""

from boxsdk import Client
from app.box_oauth import oauth_from_previous
from app.config import AppConfig
from app.oaut_callback import callback_handle_request, open_browser


def get_client(config: AppConfig) -> Client:
    """Returns a boxsdk Client object"""
    oauth = oauth_from_previous()

    # do we need to authorize the app?
    if not oauth.access_token:
        auth_url, csrf_token = oauth.get_authorization_url(config.redirect_uri)
        open_browser(auth_url)
        callback_handle_request(config, csrf_token)

    oauth = oauth_from_previous()

    if not oauth.access_token:
        raise RuntimeError("Unable to authenticate")

    oauth.refresh(oauth.access_token)

    return Client(oauth)
