#!/usr/bin/python3

import socket

try:
    import netns as netns_module
except ImportError:
    pass


def NamespacedSocketFactory(family: socket.AddressFamily, address, nspath):
    # returns a callable that instantiates and connects a socket when called
    def init_socket():
        if netns_module:
            sock = netns_module.socket(nspath, family)
            sock.connect(address)
            return sock
        else:
            raise NotImplementedError

    return init_socket
