#! /usr/bin/env python3

import socket
import threading
import subprocess


class TerminalServer(object):

    def __init__(self):
        self.prompt = "<BHP:#> $ ".encode("utf-8")
        self.target = "127.0.0.1"
        self.port = 9998
        self.max_connections = 5

    def setup_server(self):
        self.server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self.server.bind((self.target, self.port))
        self.server.listen(self.max_connections)

    def run_server(self):
        print(
            f"[*] Starting server on {self.target}:{self.port}"
        )
        while True:
            client_socket, addr = self.server.accept()
            client_thread = threading.Thread(
                target=self.client_handle, args=(client_socket,)
            )
            client_thread.start()

    def client_handle(self, client_socket):
        client_socket.send(self.prompt)
        while True:
            self.cmd_buff = ""

            while "\n" not in self.cmd_buff:
                data = client_socket.recv(1024)
                self.cmd_buff += data.decode("utf-8")

            self.cmd_buff = self.cmd_buff.rstrip()
            print(self.cmd_buff)
            cmd_output = self.run_command()
            print(f"Length of buff to be sent {len(cmd_output)}")

            try:
                client_socket.send(cmd_output)
            except TypeError:
                client_socket.send(cmd_output.encode("utf-8"))

            client_socket.send(self.prompt)

    def run_command(self):
        try:
            output = subprocess.check_output(
                self.cmd_buff, stderr=subprocess.STDOUT, shell=True
            )
        except Exception as err:
            output = f"{self.cmd_buff} failed to execute.\r\n"

        return output


if __name__ == '__main__':
    term = TerminalServer()
    term.setup_server()
    term.run_server()
