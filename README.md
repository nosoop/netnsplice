# netnsplice

A cross-platform tool to relay / proxy data across TCP sockets.
Like a daemonized `socat` of sorts.

## Configuration

Create a TOML file.  Example below demonstrating the tool's features:

```toml
[[proxies]]
# service will listen on this socket for incoming connections
listen.host = '127.0.16.5'
listen.port = 50007

# service will pass data between incoming connections and this socket
forward.host = '127.0.16.5'
forward.port = 8080

[[proxies]]
# it can also listen on / forward to a Unix stream (TCP) socket
# the listening socket can have its ownership and access permissions set
listen.path = '/var/run/service.sock'
listen.group = 'www-data'
listen.chmod = 0o600

# the forwarded socket may also be inside a network namespace (if on Linux)
# if you'd like to, you will need to run the application as a user that is capable of setns
# you will also need to install as 'netnsplice[netns]' (with the 'netns' extra)
forward.host = '127.0.0.1'
forward.port = 8080
forward.nspath = '/var/run/netns/isolated'
```

Run `netnsplice config.toml`, substituting `config.toml` with the path of your file.

## License

Provided under [MIT No Attribution](https://spdx.org/licenses/MIT-0.html).  Use the code as
you'd like.

However, do note that the `python-netns` package that is optionally used is licensed under
GPLv3.
