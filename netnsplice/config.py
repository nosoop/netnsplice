#!/usr/bin/python3

import pydantic
import socket


class NetSocketConfig(pydantic.BaseModel):
    host: str
    port: int

    @property
    def address(self):
        return (self.host, self.port)

    @property
    def family(self) -> socket.AddressFamily:
        return socket.AF_INET


class ProxyConfig(pydantic.BaseModel):
    listen: NetSocketConfig
    forward: NetSocketConfig


class AppConfig(pydantic.BaseModel):
    proxies: list[ProxyConfig]
