""" Handles the call back request from Box OAuth2.0
---
This is a simple HTTP server that listens for a request from Box OAuth2.0.
picking up the code and csrf_token from the query string.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import webbrowser
from app.box_oauth import oauth_authenticate
from app.config import AppConfig

CSRF_TOKEN_ORIG = ""


class CallbackServer(BaseHTTPRequestHandler):
    """
    Creates a mini http request handler to handle a single callback request"""

    def do_GET(self):
        """
        Gets the redirect call back from Box OAuth2.0
        capturing the code and csrf_token from the query string
        and calls for the completion of the OAuth2.0 process.
        """
        self.send_response(200)
        self.end_headers()

        # self.send_header("Content-type", "text/html")
        # self.end_headers()
        # self.wfile.write(
        #     bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8")
        # )
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))

        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        print(params)
        code = " ".join(params.get("code")) if params.get("code") else None
        state = " ".join(params.get("state")) if params.get("state") else None
        error = " ".join(params.get("error")) if params.get("error") else None
        error_description = (
            " ".join(params.get("error_description"))
            if params.get("error_description")
            else None
        )
        # TODO implement proper logging
        print(f"code: {code}")
        print(f"state: {state}")
        print(f"error: {error}")
        print(f"error_description: {error_description}")

        assert state == CSRF_TOKEN_ORIG
        oauth_authenticate(code, state)


def callback_handle_request(config: AppConfig, csrf_token: str):
    """
    Handles the call back request from Box OAuth2.0
    Creates a simple HTTP server that listens for a request from Box OAuth2.0.
    """
    global CSRF_TOKEN_ORIG
    CSRF_TOKEN_ORIG = csrf_token

    web_server = HTTPServer(
        (config.callback_hostname, config.callback_port), CallbackServer
    )

    print(
        f"Server started http://{config.callback_hostname}:{config.callback_port}"  # noqa: E501
    )

    try:
        web_server.handle_request()
    finally:
        web_server.server_close()

    print("Server stopped.")


def open_browser(auth_url: str):
    """
    Opens a browser to the auth_url
    """
    webbrowser.open(auth_url)
