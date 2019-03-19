FROM python:2.7-alpine

LABEL maintainer="u1234x1234@gmail.com"
ENV USERNAME multitor

RUN apk update && apk add --no-cache tor bash haproxy privoxy procps

COPY start.py ./

RUN adduser -D $USERNAME

RUN mkdir -p /var/lib/tor/
RUN mkdir -p /var/run/tor/
RUN chown ${USERNAME}:${USERNAME} -R /var/lib/
RUN chown ${USERNAME}:${USERNAME} -R /var/run/

USER ${USERNAME}

ENTRYPOINT [ "python", "start.py"]
