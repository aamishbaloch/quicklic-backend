from random import randint
from datetime import datetime
import pytz


def str2bool(value):
    """
    convert string to bool
    """
    if value:
        return value.lower() in ("true",)
    else:
        return False


def get_verification_code():
    return randint(100000, 999999)


def get_qid_code():
    return randint(1000, 9999)


def get_datetime_from_date_string(datetime_str):
    datetime_str = "{} {}".format(datetime_str, "00:00:00")
    unaware_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return pytz.utc.localize(unaware_date)


def get_time_from_string(time_str):
    unaware_time = datetime.strptime(time_str, '%H:%M').time()
    return pytz.utc.localize(unaware_time)


