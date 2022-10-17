#!/usr/bin/python3

import argparse
import socket
import socketserver
import threading

from .proxy import ProxyStreamRequestHandlerFactory


def main():
    # this is a temporary setup to avoid having hardcoded args in commit history
    parser = argparse.ArgumentParser(description="Proxies data between addresses")
    parser.add_argument("listen_host")
    parser.add_argument("listen_port", type=int)

    parser.add_argument("forward_host")
    parser.add_argument("forward_port", type=int)

    args = parser.parse_args()

    listen_addr = (args.listen_host, args.listen_port)
    forward_addr = (args.forward_host, args.forward_port)

    handler = ProxyStreamRequestHandlerFactory(socket.AF_INET, forward_addr)
    with socketserver.ThreadingTCPServer(listen_addr, handler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()

        # allow clean interrupts
        try:
            while server_thread.is_alive():
                server_thread.join(0.5)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            server.shutdown()


if __name__ == "__main__":
    main()
