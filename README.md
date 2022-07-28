# Passeri
A simple RESTful microservice that converts Youtube videos to MP3s. Automatically
populates each MP3 with cover, title, and other metadata.

## Gmail Integration
Due to recent changes with Gmail's API, it is no longer possible to use a Gmail
account's email + password for email automation. However, once an app
password is created, one can use the email + app password to automatically send
emails. To do so, follow these steps:
1. Navigate to https://myaccount.google.com/. Ensure that 2FA is enabled
   for the account(this step is critical).
2. Then, click Security on the left. 
3. Scroll down to the "Signing in to Google" card.
4. Click App passwords.
5. Enter your password again.
6. Select app (Mail) and device (whatever you want).
7. Generate. Now, it is possible to automatically send emails with this
   account. Set this generated password to **PASSERI_EMAIL_PASSWORD**.

## Config
By copying `env.template` into `/src` as `.env` (e.g. `cp env.template src/.env`),
the following config options can then be set:
- **PASSERI_EMAIL_ADDRESS=** the email address of the email account.
- **PASSERI_EMAIL_PASSWORD=** the password of the email account.
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