#! /usr/bin/env python3

import socket
import threading


class TerminalServer(object):

    def __init__(self):
        self.prompt = "<BHP:#> $ "
        self.target = "127.0.0.1"
        self.port = 9999
        self.max_connections = 5

    def setup_server(self):
        self.server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self.server.bind((self.target, self.port))
        self.server.listen(self.max_connections)

    def run_server(self):
        while True:
            client_socket, addr = self.server.accept()
            client_thread = threading.Thread(
                target=self.client_handle, args=(client_socket,)
            )
            client_thread.start()

    def client_handle(self, client_socket):
            client_socket.send(self.prompt.encode("utf-8"))

if __name__ == '__main__':
    term = TerminalServer()
