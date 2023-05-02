"""main.py"""

from boxsdk import Client

from box_oauth import oauth_from_previous
from oaut_callback import callback_handle_request, open_browser
from config import AppConfig


conf = AppConfig()


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """
    oauth = oauth_from_previous()

    # do we need to authorize the app?
    if not oauth.access_token:
        auth_url, csrf_token = oauth.get_authorization_url(conf.redirect_uri)
        open_browser(auth_url)
        callback_handle_request(conf, csrf_token)

    oauth = oauth_from_previous()

    oauth.refresh(oauth.access_token)
    client = Client(oauth)
    user = client.user().get()
    print(f"Hello, {user.name}")

    print("Root folder items:")
    print("------------------")
    items = client.folder("0").get_items()
    for item in items:
        print(f"Type: {item.type} ID: {item.id} Name: {item.name}")


if __name__ == "__main__":
    main()
