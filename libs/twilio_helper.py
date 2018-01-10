from twilio.rest import Client
from quicklic_backend import settings


class TwilioHelper:
    """
    Twilio Helper contains utility methods for dealing with Twilio methods.

    """
    account_sid = settings.TWILIO_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    def __init__(self):
        self.client = Client(self.account_sid, self.auth_token)

    def message(self, phone, body):
        """
        send meesage
        """
        message = self.client.messages.create(
            to=phone,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=body,
        )

        return message
