FROM python:3.7

ARG passeri_port
ARG passeri_cred_file_path
ARG passeri_token_file_path
ARG passer_download_path=/tmp

ENV PASSERI_CRED_FILE_PATH=${passeri_cred_file_path}
ENV PASSERI_TOKEN_FILE_PATH=${passeri_token_file_path}
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