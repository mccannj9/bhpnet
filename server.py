#! /usr/bin/env python3

import socket
import threading
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

        self.server.bind((self.target, self.port))
        self.server.listen(self.max_connections)

    def run_server(self):
        print(
            f"[*] Starting server on {self.target}:{self.port}"
        )
        while True:
            client_socket, addr = self.server.accept()
            print(
                f"[*] Accepted connection from: {addr[0]}:{addr[1]}"
            )
            client_thread = threading.Thread(
                target=self.client_handle, args=(
                    client_socket, addr[0], addr[1]
                )
            )
            client_thread.start()
            # client_thread.join()

    def close_server(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print(f"\n[*] Shutdown server at {self.target}:{self.port}")

    def client_handle(self, client_socket, client_ip, client_port):
        prompt_length = f"{len(self.prompt)}|".encode("utf-8")
        client_socket.send(prompt_length + self.prompt)
        exit_code_received = False

        while True:
            self.cmd_buff = ""

            while "\n" not in self.cmd_buff:
                data = client_socket.recv(1024)
                self.cmd_buff += data.decode("utf-8")
                if self.cmd_buff == "x404x":
                    exit_code_received = True
                    # addr = self.cmd_buff.split(":")
                    print(
                        f"[*] Client connection closed: "
                        f"{client_ip}:{client_port}"
                    )

                    self.cmd_buff
                    break

            if exit_code_received:
                break

            self.cmd_buff = self.cmd_buff.rstrip()
            cmd_output = self.run_command() + self.prompt
            msg_length = f"{len(cmd_output)}|".encode("utf-8")

            print(f"{self.cmd_buff} {len(cmd_output)}")
            cmd_output = msg_length + cmd_output

            try:
                client_socket.send(cmd_output)
            except BrokenPipeError:
                break

        return 0

    def run_command(self):
        try:
            output = subprocess.check_output(
                self.cmd_buff, stderr=subprocess.STDOUT, shell=True
            )
        except Exception as err:
            output = f"{self.cmd_buff} failed to execute.\n".encode("utf-8")

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
