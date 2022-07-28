FROM python:3.7

ARG passeri_port
ARG passeri_email_address
ARG passeri_email_password
ARG passer_download_path=/tmp

ENV PASSERI_EMAIL_ADDRESS=${passeri_email_address}
ENV PASSERI_EMAIL_PASSWORD=${passeri_email_password}
ENV PASSERI_DOWNLOAD_PATH=${passer_download_path}
ENV PASSERI_PORT=${passeri_port}

COPY src/ /opt/passeri/
COPY requirements.txt /tmp

RUN apt-get update -y && apt-get install -y ffmpeg

RUN mkdir -p /passeri/config
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /opt/passeri

VOLUME /passeri/config

ENTRYPOINT ["python3", "main.py"]