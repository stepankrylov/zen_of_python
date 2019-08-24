import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class PostMan:

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_message(self, message, subject, *args):
        GMAIL_SMTP = "smtp.gmail.com"
        """Send message."""
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(args)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        ms = smtplib.SMTP(GMAIL_SMTP, 587)
        """Identify ourselves to smtp gmail client."""
        ms.ehlo()
        """Secure our email with tls encryption."""
        ms.starttls()
        """Re-identify ourselves as an encrypted connection."""
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, ms, msg.as_string())
        ms.quit()
        """Send end."""

    def recive_message(self, header=None):
        GMAIL_IMAP = "imap.gmail.com"
        """Recieve."""
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        if header is None:
            criterion = '(HEADER Subject "%s")' % 'ALL'
        else:
            criterion = '(HEADER Subject "%s")' % header
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message
        """End recieve."""


if __name__ == "__main__":
    mail = PostMan('login@gmail.com', 'qwerty')
    mail.send_message(
        'Message', 'Subject', 'vasya@email.com', 'petya@email.com'
        )
    mail.recive_message()
