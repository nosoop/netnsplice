#!/usr/bin/python3

import argparse
import pathlib
import socket
import socketserver
import threading
import time
import tomli

from .config import AppConfig, ProxyConfig
from .proxy import ProxyStreamRequestHandlerFactory, SocketFactory
from .netns import NamespacedSocketFactory

unix_avail = hasattr(socket, "AF_UNIX")


def create_server(proxy: ProxyConfig):
    socketfactory = SocketFactory(proxy.forward.family, proxy.forward.address)
    if proxy.forward.family == socket.AF_INET and proxy.forward.nspath:
        socketfactory = NamespacedSocketFactory(
            proxy.forward.family, proxy.forward.address, proxy.forward.nspath
        )

    handler = ProxyStreamRequestHandlerFactory(socketfactory)

    if unix_avail and proxy.listen.family == socket.AF_UNIX:
        proxy.listen.path.unlink(missing_ok=True)
        return socketserver.ThreadingUnixStreamServer(proxy.listen.address, handler)
    return socketserver.ThreadingTCPServer(proxy.listen.address, handler)


def main():
    parser = argparse.ArgumentParser(description="Proxies data between addresses")
    parser.add_argument("config", type=pathlib.Path)

    args = parser.parse_args()

    config = AppConfig.parse_obj(tomli.loads(args.config.read_text()))

    servers = [create_server(proxy) for proxy in config.proxies]

    for server in servers:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

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
