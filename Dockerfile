FROM alpine:3.9.2

LABEL maintainer="u1234x1234@gmail.com"
ENV MULTITOR_VERSION="v1.3.0"
ENV USERNAME multitor

RUN apk update && apk add --no-cache tor bash haproxy privoxy procps

# Creating stubs for hpts, polipo as it is required by multitor but not used further
RUN touch /usr/local/bin/hpts && \
    touch /usr/local/bin/polipo && \
    chmod +x /usr/local/bin/hpts && \
    chmod +x /usr/local/bin/polipo

RUN	wget -O multitor.zip "https://github.com/trimstray/multitor/archive/$MULTITOR_VERSION.zip" && \
    unzip multitor.zip && \
    rm multitor.zip && \
    cd multitor* && \
    sed -i '/EUID\ is\ not\ equal\ 0/{n;s/.*//}' /multitor-1.3.0/src/__init__ && \
    sed -i 's/EUID is not equal 0.*/Running as non root user"/' /multitor-1.3.0/src/__init__ && \
    sed -i 's/sudo\ -u\ "$user_name"//' /multitor-1.3.0/src/__init__ && \
    sed -i 's/sudo\ -u\ "$_arg_uname"//' /multitor-1.3.0/lib/CreateTorProcess && \
    sed -i 's/sudo//' /multitor-1.3.0/src/__init__ && \
    ./setup.sh install && \
    sed -i s/127.0.0.1:16379/0.0.0.0:16379/g templates/haproxy-template.cfg

WORKDIR /multitor/
EXPOSE	16379

RUN adduser -D $USERNAME

RUN chown multitor:multitor -R /var/lib/
RUN chown multitor:multitor -R /etc/privoxy

COPY start.sh ./

USER $USERNAME
ENTRYPOINT [ "/multitor/start.sh" ]
