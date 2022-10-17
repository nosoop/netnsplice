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

# multiple [[proxies]] sections can be specified
```
