import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class Auth:

    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose',
    ]

    def __init__(self, credentials_file_path, token_file_path):
        self._credentials_file_path = credentials_file_path
        self._token_file_path = token_file_path

    def get_creds(self):
        creds = None
        if os.path.exists(self._token_file_path):
            creds = Credentials.from_authorized_user_file(
                self._token_file_path, self.SCOPES
            )

        if creds:
            if not creds.valid and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds

        flow = InstalledAppFlow.from_client_secrets_file(
            self._credentials_file_path, scopes=self.SCOPES
        )
        creds = flow.run_console()
        with open(self._token_file_path, 'w') as token:
            token.write(creds.to_json())

        return creds
