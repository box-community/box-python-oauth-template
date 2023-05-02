"""main.py"""

from config import AppConfig
from box_oauth import get_oauth, open_browser


conf = AppConfig()

hostName = "127.0.0.1"
serverPort = 5000


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8")
        )
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


def main():
    oauth = get_oauth(conf)
    auth_url, csrf_token = oauth.get_authorization_url(conf.redirect_uri)
    # print(auth_url)
    # print(csrf_token)
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    open_browser(auth_url)

    try:
        webServer.handle_request()

    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    main()
