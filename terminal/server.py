#! /usr/bin/env python3

import socket
import queue
import select
import subprocess


class TerminalServer(object):

    def __init__(self, target, port):
        self.prompt = "<BHP:#> $ ".encode("utf-8")
        self.target = target
        self.port = port
        self.max_connections = 5

    def setup_server(self):
        self.server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.server.setblocking(0)
        self.server.bind((self.target, self.port))
        self.server.listen(self.max_connections)

        self.inputs = [self.server]
        self.outputs = []
        self.msg_queues = {}

    def run_server(self):
        print(
            f"[*] Starting server on {self.target}:{self.port}"
        )
        while self.inputs:
            _read, _write, _except = select.select(
                self.inputs, self.outputs, self.inputs
            )
            for sock in _read:
                if sock is self.server:
                    client_socket, addr = self.server.accept()
                    print(
                        f"[*] Accepted connection from: {addr[0]}:{addr[1]}"
                    )
                    client_socket.setblocking(0)
                    self.inputs.append(client_socket)
                    self.msg_queues[client_socket] = queue.Queue()
                    prompt_length = f"{len(self.prompt)}|".encode("utf-8")
                    client_socket.send(prompt_length + self.prompt)
                else:
                    fail = self.client_handle(sock)
                    if fail:
                        _except.append(sock)

            for sock in _write:
                try:
                    next_msg = self.msg_queues[sock].get_nowait()
                except queue.Empty:
                    self.outputs.remove(sock)
                    continue
                sock.send(next_msg)

            for sock in _except:
                self.inputs.remove(sock)
                if sock in self.outputs:
                    self.outputs.remove(sock)
                sock.close()
                del self.msg_queues[sock]

    def client_handle(self, client_socket):
        cmd_buff = ""
        while "\n" not in cmd_buff:
            data = client_socket.recv(1024).decode("utf-8")
            if data == "x404x":
                ip, port = client_socket.getpeername()
                print(
                    f"[*] Client connection closed: {ip}:{port}"
                )
                return client_socket
            else:
                cmd_buff += data

        cmd_buff = cmd_buff.rstrip()
        cmd_output = self.run_command(cmd_buff) + self.prompt
        msg_length = f"{len(cmd_output)}|".encode("utf-8")
        print(f"{cmd_buff} {len(cmd_output)}")
        cmd_output = msg_length + cmd_output
        self.msg_queues[client_socket].put(cmd_output)
        if client_socket not in self.outputs:
            self.outputs.append(client_socket)
        return None

    def close_server(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print(f"\n[*] Shutdown server at {self.target}:{self.port}")

    def run_command(self, cmd):
        try:
            output = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=True
            )
        except Exception as err:
            output = f"{cmd} failed to execute.\n".encode("utf-8")

        return output


def main():
    import sys
    import traceback

    try:
        term = TerminalServer("127.0.0.1", 9998)
        term.setup_server()
        term.run_server()
    except KeyboardInterrupt:
        term.close_server()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == '__main__':
    main()
