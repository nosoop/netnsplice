#!/usr/bin/python3

import argparse
import pathlib
import shutil
import socket
import socketserver
import threading
import time
import tomli

from .config import AppConfig, ProxyConfig
from .proxy import ProxyStreamRequestHandlerFactory, SocketFactory
from .netns import NamespacedSocketFactory

unix_avail = hasattr(socket, "AF_UNIX")


class AutoRequestQueueMixIn:
    # disable the default maximum of 5 (!!) connections for socketserver to use more sane defaults
    def server_activate(self):
        self.socket.listen()


class InternalThreadingTCPServer(AutoRequestQueueMixIn, socketserver.ThreadingTCPServer):
    pass


if hasattr(socket, "AF_UNIX"):

    class InternalThreadingUnixStreamServer(
        AutoRequestQueueMixIn, socketserver.ThreadingUnixStreamServer
    ):
        pass


def create_server(proxy: ProxyConfig):
    socketfactory = SocketFactory(proxy.forward.family, proxy.forward.address)
    if proxy.forward.family == socket.AF_INET and proxy.forward.nspath:
        socketfactory = NamespacedSocketFactory(
            proxy.forward.family, proxy.forward.address, proxy.forward.nspath
        )

    handler = ProxyStreamRequestHandlerFactory(socketfactory)

    if unix_avail and proxy.listen.family == socket.AF_UNIX:
        proxy.listen.path.unlink(missing_ok=True)
        server = InternalThreadingUnixStreamServer(proxy.listen.address, handler)

        if proxy.listen.owner or proxy.listen.group:
            shutil.chown(proxy.listen.address, proxy.listen.owner, proxy.listen.group)
        if proxy.listen.chmod is not None:
            proxy.listen.path.chmod(proxy.listen.chmod)
        return server
    return InternalThreadingTCPServer(proxy.listen.address, handler)


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
