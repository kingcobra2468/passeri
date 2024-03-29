from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import mimetypes
import smtplib
import ssl


class MailClient:
    """A client to interact with SMTP servers.
    """
    MAX_EMAIL_BODY_MB = 25

    def __init__(self, email, password, smtp_server='smtp.gmail.com', smtp_port=465):
        """Constructor.

        Args:
            email (str): The email address of the sender email.
            password (str): The password of the sender email.
            smtp_server (str, optional): The SMTP server host. Defaults to 'smtp.gmail.com'.
            smtp_port (int, optional): The SMTP server port. Defaults to 465.
        """
        self._client = None
        self._email = email
        self._password = password
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port

        self._connect()

    def _connect(self):
        """Connects to the SMTP server.
        """
        ssl_context = ssl.create_default_context()
        self._client = smtplib.SMTP_SSL(
            self._smtp_server, self._smtp_port, context=ssl_context)
        self._client.login(self._email, self._password)

    def send_files(self, recipient, *files):
        """Sends files to the recipients. In the case where the total
        number of files exceeds the Gmail max body size(25Mb), the files
        are partitioned across emails. Files exceeding the max body size
        are ignored.

        Args:
            recipient (str): The recipient email of the files.
            files (str): The file attachment paths.
        """
        num_files = len(files)
        if not num_files:
            return

        partition_start_idx = 0
        partition_end_idx = 0
        current_size = 0
        files = [(file, self._get_file_size(file)) for file in files]

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
        """Sends the files to the recipients.

        Args:
            recipient (str): The recipient email of the files.
            files (str): The file attachment paths.
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

        try:
            self._client.sendmail(self._email, recipient, message.as_string())
        except (smtplib.SMTPServerDisconnected, smtplib.SMTPSenderRefused):
            self._connect()
            self._client.sendmail(self._email, recipient, message.as_string())

    def _get_file_size(self, file):
        """Gets the file size.

        Args:
            file (str): The file attachment path.

        Returns:
            int: The size of the file in Mb.
        """
        return os.path.getsize(file) / (1024 * 1024)
