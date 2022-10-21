#!/usr/bin/python3

import select
import socket
import socketserver

DEFAULT_BUFFER_SIZE = 4096


def SocketFactory(family: socket.AddressFamily, address):
    # returns a callable that instantiates and connects a socket when called
    def init_socket():
        sock = socket.socket(family)
        sock.connect(address)
        return sock

    return init_socket


def ProxyStreamRequestHandlerFactory(
    socket_factory: callable, buffer_size: int = DEFAULT_BUFFER_SIZE
):
    # instantiates a stream / TCP proxy handler with the address set up
    # socketserver.BaseServer instances take a class and doesn't pass any args to __init__,
    # so we need to use a factory for this
    class ProxyStreamRequestHandler(socketserver.BaseRequestHandler):
        def setup(self):
            self.forward = socket_factory()

        def handle(self):
            # create bidirectional associations between (request, forward)
            dest_map = {
                self.request: self.forward,
                self.forward: self.request,
            }

            # the function will block as long as the sockets are connected
            # socketserver.TCPServer shuts down the request socket once this method returns
            while self.process_connection(dest_map):
                pass

        def process_connection(self, dest_map):
            # returns false if the connection was terminated
            readable, writable, exceptioned = select.select(dest_map.keys(), [], [])
            for sock in readable:
                buffer = sock.recv(buffer_size)
                if buffer:
                    dest_map[sock].sendall(buffer)
                else:
                    return False
            return True

        def finish(self):
            self.forward.shutdown(socket.SHUT_RDWR)

    return ProxyStreamRequestHandler
