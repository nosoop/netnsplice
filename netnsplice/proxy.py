#!/usr/bin/python3

import concurrent.futures
import socket
import socketserver

DEFAULT_BUFFER_SIZE = 4096


def _socket_forward(src_sock: socket.socket, dst_sock: socket.socket, buffer_size: int):
    # passes the data from src_sock to dst_sock
    # the caller is responsible for cleaning up the sockets after this function returns
    while True:
        buffer = src_sock.recv(buffer_size)
        if buffer:
            dst_sock.sendall(buffer)
        else:
            break


def ProxyStreamRequestHandlerFactory(
    family: socket.AddressFamily, address, buffer_size: int = DEFAULT_BUFFER_SIZE
):
    # instantiates a stream / TCP proxy handler with the address set up
    # socketserver.BaseServer instances take a class and doesn't pass any args to __init__,
    # so we need to use a factory for this
    class ProxyStreamRequestHandler(socketserver.BaseRequestHandler):
        def setup(self):
            self.forward = socket.socket(family)
            self.forward.connect(address)

        def handle(self):
            # create bidirectional connections between (request, forward)
            # surely there's a way to do this in one function...

            # the executor will block until both connections have finished
            # socketserver.TCPServer shuts down the request socket once this method returns
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(_socket_forward, self.request, self.forward, buffer_size)
                executor.submit(_socket_forward, self.forward, self.request, buffer_size)

        def finish(self):
            self.forward.shutdown(socket.SHUT_RDWR)

    return ProxyStreamRequestHandler
