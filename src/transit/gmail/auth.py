import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError


class Auth:
    """Auth handles the OAuth authentication logic of a client
    in order to grant access to the Gmail API.
    """
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose',
    ]

    def __init__(self, credentials_file_path, token_file_path):
        """Constructor.

        Args:
            credentials_file_path (str): Path to the credentials file.
            token_file_path (str): Path to the token file. 
        """
        self._credentials_file_path = credentials_file_path
        self._token_file_path = token_file_path

    def get_creds(self):
        """Gets the credentials of a given client. If no token.json file exists,
        a prompt will be displayed with the steps on how to generate it. A link
        will be displayed which will prompt a user to sign in, grant scopes, a paste
        an activation code in the terminal. This will automatically generate the token.json
        file.

        Returns:
            google.oauth2.credentials.Credentials: The credentials of the client.
        """
        creds = None
        if os.path.exists(self._token_file_path):
            creds = Credentials.from_authorized_user_file(
                self._token_file_path, self.SCOPES
            )

        if creds:
            try:
                if not creds.valid and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                return creds
            except RefreshError:
                pass

        flow = InstalledAppFlow.from_client_secrets_file(
            self._credentials_file_path, scopes=self.SCOPES
        )
        # prompt the user to grant access to passeri
        creds = flow.run_console()
        with open(self._token_file_path, 'w') as token:
            token.write(creds.to_json())

        return creds
