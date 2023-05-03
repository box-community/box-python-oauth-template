"""main.py"""

import logging
from app.config import AppConfig

from app.box_client import get_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """

    client = get_client(conf)

    user = client.user().get()
    print("==================")
    print(f"Hello, {user.name}")
    print("------------------")
    print("Root folder items:")
    print("------------------")
    items = client.folder("0").get_items()
    for item in items:
        print(f"Type: {item.type} ID: {item.id} Name: {item.name}")
    print("==================")


if __name__ == "__main__":
    main()
