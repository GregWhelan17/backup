FROM ubuntu:latest
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtimezone && echo $TZ > /etc/timezone
RUN apt-get -y update && apt-get install -y apt-transport-https ca-certificates gnupg curl jq python3 python3-pip python3-venv vim sudo \
    && apt-get upgrade -y
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg \
    && echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list \
    && apt update \
    && apt install kubectl -y
RUN  python3 -m venv .venv && /.venv/bin/pip install google-cloud-storage

RUN mkdir -p /scripts
COPY scripts/* /scripts/
RUN chmod +x /scripts/*
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/entrypoint.sh"]