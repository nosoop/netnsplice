#!/usr/bin/python3

import argparse
import pathlib
import socket
import socketserver
import threading
import time
import tomli

from .config import AppConfig
from .proxy import ProxyStreamRequestHandlerFactory, SocketFactory


def main():
    parser = argparse.ArgumentParser(description="Proxies data between addresses")
    parser.add_argument("config", type=pathlib.Path)

    args = parser.parse_args()

    config = AppConfig.parse_obj(tomli.loads(args.config.read_text()))

    servers = []
    for proxy in config.proxies:
        socketfactory = SocketFactory(proxy.forward.family, proxy.forward.address)
        handler = ProxyStreamRequestHandlerFactory(socketfactory)
        server = socketserver.ThreadingTCPServer(proxy.listen.address, handler)

        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        servers.append(server)

    # allow clean interrupts
    try:
        while True:
            time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        pass

    # shutdown listeners
    for server in servers:
        server.shutdown()


if __name__ == "__main__":
    main()
