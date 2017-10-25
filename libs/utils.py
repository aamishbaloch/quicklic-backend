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


def get_qid_code():
    return randint(1000, 9999)


def get_datetime_from_date_string(datetime_str):
    datetime_str = "{} {}".format(datetime_str, "00:00:00")
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")



def get_time_from_string(time_str):
    return datetime.strptime(time_str, '%H:%M').time()


def get_split_datetime(datetime_str):
    date_str,time_str = datetime_str.split(' ')
    return date_str, time_str


def get_weekday_from_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").weekday()


def convert_to_datetime(date_str, time):
    datetime_str = date_str + ' ' + time.strftime("%H:%M")
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def convert_to_datetime_from_datetime_string(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

