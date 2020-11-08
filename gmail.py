import smtplib
import config

def get_sms_address(number, carrier):
    if carrier == 'verizon':
        return '%s@vtext.com' % number
    elif carrier == 'att':
        return '%s@txt.att.net' % number
    else:
        raise NotImplementedError(
            'get_sms_address received unsupported carrier: %s' % carrier
        )

class Gmail(object):
    def __init__(self, gmail_address, gmail_pw):
        self.gmail_address = gmail_address
        self.gmail_pw = gmail_pw

    def send(self, recipient, subject, body):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.gmail_address, self.gmail_pw)
        body = self._getbody(recipient, subject, body)
        try:
            server.sendmail(self.gmail_address, recipient, body)
        except:
            print("Failed to send email to %s" % recipient)
        server.quit()

    def _getbody(self, recipient, subject, body):
        return '\r\n'.join([
            'To: %s' % recipient,
            'From: %s' % self.gmail_address,
            'Subject: %s' % subject,
            '',
            body
        ])