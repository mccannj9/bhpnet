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

    def get_message_length(self):
        buff = ""
        while True:
            c = self.client.recv(1).decode("utf-8")
            if c == "|":
                return int(buff)
            else:
                buff += c

    def use_server_terminal_2(self):
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
            except EOFError:
                print("")
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                break


if __name__ == '__main__':
    user = TerminalUser()
    user.setup_client_connection()
    user.use_server_terminal_2()
