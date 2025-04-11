FROM ubuntu:latest
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtimezone && echo $TZ > /etc/timezone
# RUN --mount=type=secret,id=aptconf,target=/etc/apt/auth.conf \
RUN apt-get -y update && apt-get install -y apt-transport-https ca-certificates gnupg curl jq python3 python3-pip python3-request vim python3-google-cloud-storage \
    && apt-get upgrade -y  

COPY entrypoint.sh /entrypoint.sh
# COPY application_default_credentials.json /root/.config/gcloud/application_default_credentials.json

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/entrypoint.sh"]