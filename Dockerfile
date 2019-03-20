FROM python:3.6-alpine

LABEL maintainer="u1234x1234@gmail.com"
ENV USERNAME multitor

RUN apk update && apk add --no-cache tor bash haproxy privoxy procps

RUN adduser -D $USERNAME

RUN mkdir -p /var/lib/tor/
RUN mkdir -p /var/run/tor/
RUN chown ${USERNAME}:${USERNAME} -R /var/lib/
RUN chown ${USERNAME}:${USERNAME} -R /var/run/

RUN chown ${USERNAME}:${USERNAME} -R /etc/privoxy

COPY start.py ./
COPY haproxy.conf /etc/haproxy.conf

USER ${USERNAME}
ENTRYPOINT [ "python", "start.py"]
