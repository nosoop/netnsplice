# netnsplice

> [!NOTE]
> This project has been archived.  While it still probably all works just fine, I've opted to
> migrate my Linux services to use `systemd-socket-proxyd`.

A cross-platform tool to relay / proxy data across TCP sockets.
Like `rinetd` or a daemonized `socat` of sorts.

## Installation

Package is currently only provided in the git repository:

```
# cutting edge
pip install "git+https://github.com/nosoop/netnsplice#egg=netnsplice"

# with network namespace support
pip install "git+https://github.com/nosoop/netnsplice#egg=netnsplice[netns]"
```

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
listen.path = '/var/run/service.sock'

# the listening socket can have its ownership and access permissions set
# if not running as root, the user will need CAP_CHOWN and CAP_FOWNER capabilites respectively
listen.group = 'www-data'
listen.chmod = 0o600

forward.host = '127.0.0.1'
forward.port = 8080

# the forwarded socket may also be inside a network namespace (if on Linux)
# if not running as root, the user will need CAP_SYS_ADMIN capabilities to use setns
# you will also need to install as 'netnsplice[netns]' (with the 'netns' extra)
forward.nspath = '/var/run/netns/isolated'
```

Run `netnsplice config.toml`, substituting `config.toml` with the path of your file.

## License

Provided under [MIT No Attribution](https://spdx.org/licenses/MIT-0.html).  Use the code as
you'd like.

However, do note that the `python-netns` package that is optionally used is licensed under
GPLv3.
