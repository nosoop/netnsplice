#!/usr/bin/python3

import pathlib
import pydantic
import socket
import typing


class BaseSocketConfig(pydantic.BaseModel):
    @property
    def address(self):
        raise NotImplementedError

    @property
    def family(self) -> socket.AddressFamily:
        raise NotImplementedError


class UnixSocketConfig(BaseSocketConfig):
    path: pathlib.Path

    @property
    def address(self):
        return str(self.path)

    @property
    def family(self) -> socket.AddressFamily:
        return socket.AF_UNIX


class NetSocketConfig(BaseSocketConfig):
    host: str
    port: int

    @property
    def address(self):
        return (self.host, self.port)

    @property
    def family(self) -> socket.AddressFamily:
        return socket.AF_INET


class ListenUnixSocketConfig(UnixSocketConfig):
    # only the listening socket can have these fields
    owner: typing.Optional[str]
    group: typing.Optional[str]
    chmod: typing.Optional[int]


class ForwardNetSocketConfig(NetSocketConfig):
    # only the socket we are forwarding to can support namespaces at the moment
    nspath: typing.Optional[str]


class ProxyConfig(pydantic.BaseModel):
    listen: typing.Union[NetSocketConfig, ListenUnixSocketConfig]
    forward: typing.Union[ForwardNetSocketConfig, UnixSocketConfig]


class AppConfig(pydantic.BaseModel):
    proxies: list[ProxyConfig]
