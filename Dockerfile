FROM python:3.7

ARG passeri_port
ARG passeri_email_address
ARG passeri_email_password
ARG passeri_download_path=/tmp
ARG passeri_file_cache_size=1000
ARG passeri_mongo_db_host
ARG passeri_mongo_db_port=27017
ARG passeri_request_logging_enabled=0

ENV PASSERI_EMAIL_ADDRESS=${passeri_email_address}
ENV PASSERI_EMAIL_PASSWORD=${passeri_email_password}
ENV PASSERI_DOWNLOAD_PATH=${passeri_download_path}
ENV PASSERI_PORT=${passeri_port}
ENV PASSERI_FILE_CACHE_SIZE=${passeri_file_cache_size}
ENV PASSERI_MONGO_DB_HOST=${passeri_mongo_db_host}
ENV PASSERI_MONGO_DB_PORT=${passeri_mongo_db_port}
ENV PASSERI_REQUEST_LOGGING_ENABLED=${passeri_request_logging_enabled}

COPY src/ /opt/passeri/
COPY requirements.txt /tmp

RUN apt-get update -y && apt-get install -y ffmpeg

RUN mkdir -p /passeri/config
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /opt/passeri

VOLUME /passeri/config

ENTRYPOINT ["python3", "main.py"]