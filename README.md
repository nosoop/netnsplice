# netnsplice

A tool to replay / proxy data across sockets.  Like a daemonized `socat` of sorts.

## Configuration

Create a TOML file with the following:

```
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

# the forwarded socket may also be inside a network namespace (if on Linux)
# you will need to run the daemon as a user that is capable of setns
forward.host = '127.0.0.1'
forward.port = 8080
forward.nspath = '/var/run/netns/isolated'
```
