import sys
from django.core import mail
from django.views.debug import ExceptionReporter


def send_manually_exception_email(request, e):
    exc_info = sys.exc_info()
    reporter = ExceptionReporter(request, is_email=True, *exc_info)
    subject = "Django Error Report"
    message = "{}".format(reporter.get_traceback_text)
    mail.mail_admins(
        subject, message, fail_silently=True,
        html_message=reporter.get_traceback_html()
    )


def send_manually_error_email(error_message):
    subject = "Django Error Report"
    message = "{}".format(error_message)
    mail.mail_admins(
        subject, message, fail_silently=True
    )
