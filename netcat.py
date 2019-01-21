#! /usr/bin/env python3

from terminal.client import TerminalUser
from terminal.server import TerminalServer


def main():
    import sys
    import traceback
    import argparse as ap

    desc = "A tool for running commands over a server socket connection"

    parser = ap.ArgumentParser(description=desc)

    parser.add_argument('-l', "--listen", action="store_true")
    parser.add_argument('-c', "--command", action="store_true")
    parser.add_argument('-t', "--target", default="127.0.0.1", type=str)
    parser.add_argument('-p', "--port", default=9999, type=int)

    args = parser.parse_args()

    if args.listen and not(args.command):
        try:
            term = TerminalServer(args.target, args.port)
            term.setup_server()
            term.run_server()
        except KeyboardInterrupt:
            term.close_server()
        except Exception:
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

    elif args.command and not(args.listen):
        user = TerminalUser(args.target, args.port)
        user.setup_client_connection()
        user.use_server_terminal()

    else:
        print(
            "Please specify either --listen OR "
            "--command for your program instance", file=sys.stderr
        )
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    return 0


if __name__ == '__main__':
    main()
