[![Docker Pulls](https://img.shields.io/docker/cloud/build/u1234x1234/torpool.svg?style=flat-square)](https://hub.docker.com/r/u1234x1234/torpool/)
[![Size](https://images.microbadger.com/badges/image/u1234x1234/torpool.svg)](https://hub.docker.com/r/u1234x1234/torpool/)

# torpool

Containerized pool of multiple Tor instances with load balancing and HTTP proxy.

# Key features

* Multiple [Tor](https://www.torproject.org/) instances with a single endpoint for the end user
* Easy configured (IP rotation, country selection of the exit node, etc)
* Lightweight alpine based Docker image
* HTTP proxy with [Privoxy](https://www.privoxy.org/)
* HTTP/Socks load balancing with [HAProxy](http://www.haproxy.org/)
* Does not using root user inside Docker

```
              +-----------------------------------------------+           
              | Docker                                        |           
              |                                               |           
              |                   +-------+            +----+ |           
              |                   |Privoxy|------------|Tor1| |           
              |                   +-------+        |   +----+ |           
+------+      | +-------+         +-------+        |   +----+ |           
|Client|--------|Haproxy|-------- |Privoxy|--------|---|Tor2| |           
+------+      | +-------+         +-------+        |   +----+ |           
              |     |             +-------+        |   +----+ |           
              |     |             |Privoxy|--------|---|Tor3| |           
              |     |             +-------+        |   +----+ |           
              |     |                              |          |           
              |     |                              |          |           
              |     +------------------------------+          |           
              |                                               |           
              +-----------------------------------------------+           
```

# Usage

Start 5 Tor instances:
```bash
docker run -d -p 9200:9200 -p 9300:9300 u1234x1234/torpool:1.0.0 --Tors=5
```

HTTP proxy is accessible at port 9300:
```bash
curl --proxy localhost:9300 http://ipinfo.io/ip
```

Socks is accessible at port 9200: 
```bash
curl --socks5 localhost:9200 http://ipinfo.io/ip
```

To make Tor instances rotate:
```
docker run -d -p 9200:9200 -p 9300:9300 u1234x1234/torpool:1.0.0 --MaxCircuitDirtiness 30 --NewCircuitPeriod 30
```

Use only US exit nodes:
```
docker run -d -p 9200:9200 -p 9300:9300 u1234x1234/torpool:1.0.0 --ExitNodes {us}
```

[List of available options](https://www.torproject.org/docs/tor-manual.html.en)


# Why

There is a lot of great projects on github, but non of them provides all the options listed above. Some of them:

* https://github.com/trimstray/multitor
* https://github.com/evait-security/docker-multitor
* https://github.com/zet4/alpine-tor
* https://github.com/rdsubhas/docker-tor-privoxy-alpine
* https://github.com/Negashev/docker-haproxy-tor
* https://github.com/marcelmaatkamp/docker-alpine-tor
* https://github.com/mattes/rotating-proxy
* https://github.com/srounet/docker-tor
* https://github.com/dperson/torproxy
* https://github.com/srounet/docker-tor
