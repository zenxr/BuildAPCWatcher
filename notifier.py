from datetime import datetime, timezone

from gmail import Gmail, get_sms_address
import config

class Notifier(object):
    def __init__(self):
        self.gmail = Gmail(config.GMAIL_INFO['email'], config.GMAIL_INFO['pw'])
        self.subject = 'New alert from buildapc watcher'
        self.to_emails = config.EMAIL_TO
        self.to_sms = config.SMS_TO

    def alert(self, post):
        print(post['title'])
        self._alert_emails(post)
        self._alert_smses(post)

    def _alert_emails(self, post):
        body = self._build_email_msg_body(post)
        for to_email in self.to_emails:
            self.gmail.send(to_email, self.subject, body)

    def _build_email_msg_body(self, post):
        date = datetime.fromtimestamp(post['created'])
        date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return '\r\n\r\n'.join([
            post['title'],
            post['link'],
            post['reddit_url'],
            str(date),
            post['body']
        ])

    def _alert_smses(self, post):
        body = self._build_sms_msg_body(post)
        for sms in self.to_sms:
            self.gmail.send(get_sms_address(sms, self.to_sms[sms]), self.subject, body)

    def _build_sms_msg_body(self, post):
        date = datetime.fromtimestamp(post['created'])
        date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return '\r\n\r\n'.join([
            post['title'],
            post['link'],
            post['reddit_url'],
            str(date)
        ])

