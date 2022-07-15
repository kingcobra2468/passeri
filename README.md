# Passeri
A simple RESTful microservice that converts Youtube videos to MP3s. Automatically
populates each MP3 with cover, title, and other metadata.

## Gmail Integration
Due to recent changes with Gmail's API, it is necessary to create a Google
Cloud project is order to access the Gmail API. For the account that will be
used as the sender account, the following steps need to be followed.
1. Setup a new Google Cloud project.
2. Enable the Gmail API for the project.
3. Create new credentials under OAuth 2.0 Client IDs.
4. Once created, download the file. The path to the file will need to be
   referenced to by [**PASSERI_CRED_FILE_PATH**](#config).

### Token Generation
If no token file currently exists, one will be created at the path
**PASSERI_TOKEN_FILE_PATH** the first time the program is run. A prompt will
be displayed with instructions on how to allow Passeri to use the selected Gmail
account as the sender account.

## Config
By copying `env.template` into `/src` as `.env` (e.g. `cp env.template src/.env`),
the following config options can then be set:
- **PASSERI_CRED_FILE_PATH=** the path to the Google project OAuth 2.0 Client IDs
    credentials file.
- **PASSERI_TOKEN_FILE_PATH=** the path to the Google API `token.json` file.
- **PASSERI_DOWNLOAD_PATH=** the directory where mp3s will be temporary stored during
    ID3 metadata entry.
- **PASSERI_PORT=** the port address of Passeri.

## Installation
To install and run Passeri, follow the following steps:
1. Ensure that Python3.7+ is installed.
2. Follow the Google Cloud project creation [steps](#gmail-integration).
3. Follow the configuration [steps](#config).
4. Install dependencies with `pip3 install -r requirements.txt`.
5. Navigate into `src/` and run Passeri with `python3 main.py`.

### Docker
1. Build Passeri image with `docker build -t passeri:1.0 .` .
2. Setup the `.env` file as described in the [config](#configuration) section. Note that
   the paths for **PASSERI_CRED_FILE_PATH** and **PASSERI_TOKEN_FILE_PATH** will be
   relative to the filesystem instead of the docker image. As such, the paths should be
   relative to the expose volume `/passeri/config`. 
3. Launch Passeri. An example execution, assuming **PASSERI_PORT** is set to `8088`, and
   the token and client secret current directory, would be:
  ```bash
  docker run --env-file .env -p 8088:8088 -v $PWD:/passeri/config  passeri:1.0