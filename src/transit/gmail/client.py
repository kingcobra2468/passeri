from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import base64
import mimetypes

from googleapiclient.discovery import build

from transit.gmail.auth import Auth


class GmailClient:
    """GmailClient serves as a client to interact with Gmail through
    the official Google Gmail API.
    """
    MAX_EMAIL_BODY_MB = 25

    def __init__(self, credentials_file_path, token_file_path):
        """Constructor.

        Args:
            credentials_file_path (str): Path to the credentials file.
            token_file_path (str): Path to the token file. 
        """
        self._client = None
        self._auth_client = Auth(credentials_file_path, token_file_path)
        self._setup()

    def _setup(self):
        """Sets up a Gmail client with the client credentials.
        """
        self._client = build(
            'gmail', 'v1', credentials=self._auth_client.get_creds())

    def send_files(self, recipient, *files):
        """Sends files to a given recipients. In the case where the total
        number of files exceeds the Gmail max body size(25Mb), the emails
        be partitioned into smaller emails. Files with sizes over the max
        body size will not be sent.

        Args:
            recipient (str): The recipient email to which to send the files.
            files (str): The paths to the file attachments.
        """
        num_files = len(files)
        if not num_files:
            return

        partition_start_idx = 0
        partition_end_idx = 0
        files = [(file, self._get_file_size(file)) for file in files]
        current_size = 0
        files.sort(key=lambda file: file[1])
        if self.MAX_EMAIL_BODY_MB < files[0][1]:
            return

        # partition the sendoff of emails to avoid going over the max email
        # body size
        while partition_end_idx < num_files:
            if self.MAX_EMAIL_BODY_MB < files[partition_end_idx][1]:
                return

            current_size += files[partition_end_idx][1]
            # check if the current set of files exceeds the max body size
            if current_size < self.MAX_EMAIL_BODY_MB:
                partition_end_idx += 1
                if partition_end_idx + 1 < num_files:
                    continue
            else:
                partition_end_idx -= 1

            self._send_email(
                recipient,
                [
                    file[0]
                    for file in files[partition_start_idx: partition_end_idx + 1]
                ],
            )

            partition_start_idx = partition_end_idx + 1
            partition_end_idx = partition_start_idx
            current_size = 0

    def _send_email(self, recipient, files):
        """Sends files to a given recipients.

        Args:
            recipient (str): The recipient email to which to send the files.
            files (str): The paths to the file attachments.
        """
        message = MIMEMultipart()
        message['To'] = recipient
        message['Subject'] = 'Passeri Mp3s'
        for file in list(files):
            type_subtype, _ = mimetypes.guess_type(file)
            maintype, subtype = type_subtype.split('/')
            with open(file, 'rb') as fp:
                contents = fp.read()

            part = MIMEBase(maintype, subtype)
            part.set_payload(contents)
            filename = file.split('/')[-1].encode('utf-8').decode('utf-8')

            encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment', filename=filename)
            message.attach(part)

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        self._client.users().messages().send(userId='me', body=create_message).execute()

    def _get_file_size(self, file):
        """Gets the size of a given file.

        Args:
            file (str): The path to the file.

        Returns:
            int: The size of the file in Mb.
        """
        return os.path.getsize(file) / (1024 * 1024)
