FROM haproxytech/haproxy-alpine:2.3.9

LABEL maintainer="u1234x1234@gmail.com"
ENV USERNAME torpool

RUN apk update && \
    apk add --no-cache tor bash python3 privoxy procps py3-pip && \
    pip install jinja2 && \
    rm -rf /var/cache/apk/*

RUN adduser -D $USERNAME

RUN mkdir -p /var/lib/tor/
RUN mkdir -p /var/run/tor/
RUN chown ${USERNAME}:${USERNAME} -R /var/lib/
RUN chown ${USERNAME}:${USERNAME} -R /var/run/
RUN chown ${USERNAME}:${USERNAME} -R /etc/privoxy

COPY start.py ./
COPY haproxy.conf /etc/haproxy.conf
RUN chown ${USERNAME}:${USERNAME} -R /etc/haproxy.conf

USER ${USERNAME}
ENTRYPOINT [ "python3", "start.py"]
