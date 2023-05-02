""" check if the oAuth is working"""

from app.config import AppConfig
from app.box_oauth import get_oauth, open_browser
from app.oaut_callback import callback_handle_request


def test_oauth_configurations():
    """check if the oAuth configurations exist as expected"""
    conf = AppConfig()

    assert conf.client_id is not None
    assert conf.client_secret is not None
    assert conf.redirect_uri is not None


def test_get_oauth_object():
    """check if the authorization url is generated as expected"""
    conf = AppConfig()

    oauth = get_oauth(conf)

    assert oauth is not None
    assert oauth.api_config.BASE_API_URL is not None
    assert oauth.api_config.OAUTH2_API_URL is not None
    assert oauth.api_config.OAUTH2_AUTHORIZE_URL is not None
    assert oauth.api_config.UPLOAD_URL is not None

    auth_url, csrf_token = oauth.get_authorization_url(conf.redirect_uri)

    assert auth_url is not None
    assert csrf_token is not None


def test_open_browser():
    """check if the authorization url is generated as expected"""
    conf = AppConfig()

    oauth = get_oauth(conf)

    assert oauth is not None
    assert oauth.api_config.BASE_API_URL is not None
    assert oauth.api_config.OAUTH2_API_URL is not None
    assert oauth.api_config.OAUTH2_AUTHORIZE_URL is not None
    assert oauth.api_config.UPLOAD_URL is not None

    auth_url, csrf_token = oauth.get_authorization_url(conf.redirect_uri)

    assert auth_url is not None
    assert csrf_token is not None

    open_browser(auth_url)

    callback_handle_request(conf)
