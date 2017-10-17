from random import randint
from datetime import datetime


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


def get_datetime_from_date_string(datetime_str):
    datetime_str = "{} {}".format(datetime_str, "00:00:00")
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


def get_time_from_string(time_str):
    return datetime.strptime(time_str, '%H:%M').time()


