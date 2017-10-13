from twilio.rest import Client


class TwilioHelper:
    """
    Twilio Helper contains utility methods for dealing with Twilio methods.

    """
    account_sid = "AC60ad78981ca7f9e3029ad32215132ca2"
    auth_token = "eb358a991cae3f6befc173f4d3853555"

    def __init__(self):
        self.client = Client(self.account_sid, self.auth_token)

    def message(self, text, code):
        """
        send meesage
        """
        message = self.client.messages.create(
            to="+923214170605",
            from_="+18336000981",
            body="Hello from Python! - {}".format(code))

        return message
