# Passeri
A simple RESTful microservice for downloading Youtube videos as MP3s and
sending them to a recipient via email. Automatically fills cover, title,
and other ID3 metadata of compliant MP3s via Shazam integration.

## Gmail Integration
Due to recent changes with Gmail's API, it is necessary to create a Google
Cloud project is order to access the Gmail API. For the account that will be
used as the sender account, the following steps need to be followed.
1. Setup a new Google Cloud project.
2. Enable the Gmail API for the project.
3. Create new credentials under OAuth 2.0 Client IDs.
4. Once created, download the file. The path to the file will need to be
   referenced to by [**PASSERI_CRED_FILE_PATH**](#config).

## Config
By copying `env.template` into `/src` as `.env` (e.g. `cp env.template src/.env`),
the following config options can then be set:
- **PASSERI_CRED_FILE_PATH=** the path to the Google project OAuth 2.0 Client IDs credentials
    file.
- **PASSERI_TOKEN_FILE_PATH=** the path to the Google API `token.json` file.
- **PASSERI_DOWNLOAD_PATH=** the directory where mp3s will be temporary stored during ID3 metadata
    entry.
- **PASSERI_PORT=** the port address of Passeri.

## Installation
To install and run Passeri, follow the following steps:
1. Ensure that Python3.7+ is installed.
2. Follow the Google Cloud project creation [steps](#gmail-integration).
3. Follow the configuration [steps](#config).
4. Install dependencies with `pip3 install -r requirements.txt`.
5. Navigate into `src/` and run Passeri with `python3 main.py`.