""" Handles the call back request from Box OAuth2.0
---
This is a simple HTTP server that listens for a request from Box OAuth2.0.
picking up the code and csrf_token from the query string.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from app.config import AppConfig


class CallbackServer(BaseHTTPRequestHandler):
    """
    Creates a mini http request handler to handle a single callback request"""

    def do_GET(self):
        """
        Gets the redirect call back from Box OAuth2.0
        capturing the code and csrf_token from the query string
        and calls for the completion of the OAuth2.0 process.
        """
        self.send_response(201)

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
        print(params["code"][0])
        print(params["state"][0])


def callback_handle_request(config: AppConfig):
    """
    Handles the call back request from Box OAuth2.0
    Creates a simple HTTP server that listens for a request from Box OAuth2.0.
    """
    web_server = HTTPServer(
        (config.callback_hostname, config.callback_port), CallbackServer
    )
    print(f"Server started http://{config.callback_hostname}:{config.callback_port}")

    try:
        web_server.handle_request()
    finally:
        web_server.server_close()

    print("Server stopped.")
