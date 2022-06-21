from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from pathlib import Path
import os
import base64
import mimetypes

from googleapiclient.discovery import build

from gmail.auth import Auth


class GmailClient:
    MAX_EMAIL_BODY_MB = 25

    def __init__(self, credentials_file_path, token_file_path):
        self._client = None
        self._auth_client = Auth(credentials_file_path, token_file_path)
        self._setup()

    def _setup(self):
        self._client = build(
            'gmail', 'v1', credentials=self._auth_client.get_creds())

    def send_files(self, recipient, *files):
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

        while partition_end_idx < num_files:
            if self.MAX_EMAIL_BODY_MB < files[partition_end_idx][1]:
                return

            current_size += files[partition_end_idx][1]
            if current_size < self.MAX_EMAIL_BODY_MB:
                partition_end_idx += 1
                if partition_end_idx + 1 < num_files:
                    continue
            else:
                partition_end_idx -= 1

            self._send_email(
                recipient, [file[0]
                            for file in files[partition_start_idx: partition_end_idx + 1]]
            )

            partition_start_idx = partition_end_idx + 1
            partition_end_idx = partition_start_idx
            current_size = 0

    def _send_email(self, recipient, files):
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
            filename = file.split("/")[-1].encode('utf-8').decode('utf-8')

            encode_base64(part)
            part.add_header(
                'Content-Disposition', 'attachment', filename=filename
            )
            message.attach(part)

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        self._client.users().messages().send(userId='me', body=create_message).execute()

    def _get_file_size(self, file_name):
        return os.path.getsize(file_name) / (1024 * 1024)
