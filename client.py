#! /usr/bin/env python3

import socket


class TerminalUser(object):

    def __init__(self):
        self.target = "127.0.0.1"
        self.port = 9998
        self.history = []

    def setup_client_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.target, self.port))
        # data = self.client.recv(4096)
        # print(data.decode("utf-8"))

    def use_server_terminal(self):
        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = self.client.recv(4096)
                response += data.decode("utf-8")

                if recv_len < 4096:
                    print(response, end="")
                    break
            try:
                buff = input("")
                buff += "\n"
                self.history.append(buff)
                buff = buff.encode("utf-8")
                self.client.send(buff)
            except EOFError:
                print("")
                break


if __name__ == '__main__':
    user = TerminalUser()
    user.setup_client_connection()
    user.use_server_terminal()
