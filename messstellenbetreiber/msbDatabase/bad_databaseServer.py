import _socket
import sys
import logging
import signal
import http.server
import socketserver
from threading import Thread
import time

class DatabaseConnection:
    def 


class connectionHandler(http.server.SimpleHTTPRequestHandler):
    """handle a single connection to the server"""

    log = logging.getLogger()
    db: DatabaseConnection

    def __init__(self, request: _RequestType, client_address: _RetAddress, server: BaseServer, *, directory: str | None = None) -> None:
        self.db = DatabaseConnection()
        super().__init__(request, client_address, server, directory=directory)

    def write_headers(self) -> None:
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8")
        )
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


class serverConnector:
    log = logging.getLogger()
    connection: socketserver.TCPServer
    serve_thread: Thread

    def __init__(
        self,
        hostname="localhost",
        port=18732,
    ):
        """initiate and start the connection"""
        # can only connect to ipv4
        # my home only supports ipv4
        self.connection = socketserver.TCPServer((hostname, port), connectionHandler)
        self.log.info(f"Started server on: {hostname}:{port}")
        serve_thread = Thread(target=self.connection.serve_forever)
        serve_thread.start()

    def stop_server(self):
        logging.debug("Shutting down server")
        self.connection.shutdown()
        logging.debug("Shut down server")


class MyServer:
    connection: serverConnector

    def __init__(self) -> None:
        # add log-file
        logging.basicConfig(
            filename="http_api.log",
            encoding="utf-8",
            level=logging.DEBUG,
        )
        # add console-log
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stderr))
        self.connection = serverConnector("localhost", 3000)

    def stop_server(self):
        self.connection.stop_server()


global_server_reference: MyServer = None


def signal_handler(sig, frame):
    logging.debug("You pressed Ctrl+C!")
    if global_server_reference == None:
        logging.warning("server was not initialized?")
    else:
        global_server_reference.stop_server()
    sys.exit(0)


def __main__():
    # add strg c handler
    signal.signal(signal.SIGINT, signal_handler)
    global global_server_reference
    global_server_reference = MyServer()
    # this thread needs to do something, else the stopping doesn't work
    while True:
        time.sleep(0.5)


# check if arguments declare a json file
if __name__ == "__main__":
    __main__()
