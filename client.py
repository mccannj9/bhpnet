#! /usr/bin/env python3

import socket


class TerminalUser(object):

    def __init__(self):
        self.target = "127.0.0.1"
        self.port = 9999


if __name__ == '__main__':
    user = TerminalUser()
