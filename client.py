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
        self.address = self.client.getsockname()

    def get_message_length(self):
        buff = ""
        while True:
            c = self.client.recv(1).decode("utf-8")
            if c == "|":
                return int(buff)
            else:
                buff += c

    def use_server_terminal(self):
        exit_code = "x404x".encode("utf-8")
        exit_msg = f":{self.address[0]}:{self.address[1]}".encode("utf-8")
        exit_msg = exit_code + exit_msg

        while True:
            msg_length = self.get_message_length()
            data = self.client.recv(msg_length)
            print(data.decode("utf-8"), end="")
            try:
                buff = input("")
                buff += "\n"
                self.history.append(buff)
                buff = buff.encode("utf-8")
                self.client.send(buff)
            except (EOFError, KeyboardInterrupt):
                print("")
                self.client.send(exit_msg)
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                break
        return 0


if __name__ == '__main__':
    user = TerminalUser()
    user.setup_client_connection()
    user.use_server_terminal()
