""" Application configurations """
import os
from dotenv import load_dotenv


class AppConfig:
    """application configurations"""

    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = os.getenv("REDIRECT_URI")
        self.callback_hostname = os.getenv("CALLBACK_HOSTNAME")
        self.callback_port = int(os.getenv("CALLBACK_PORT"))

    def __repr__(self) -> str:
        return f"AppConfig({self.__dict__})"
