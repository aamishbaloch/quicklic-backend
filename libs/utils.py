from random import randint
from datetime import datetime, timedelta
import pytz

from quicklic_backend import settings


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


def get_datetime_now_by_date():
    date_str = str(datetime.now().date())
    datetime_str = "{} {}".format(date_str, "00:00:00")
    unaware_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return pytz.timezone(settings.TIME_ZONE).localize(unaware_date)

def get_datetime_from_date_string(datetime_str):
    datetime_str = "{} {}".format(datetime_str, "00:00:00")
    unaware_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return pytz.timezone(settings.TIME_ZONE).localize(unaware_date)


def get_start_datetime_from_date_string(datetime_str):
    datetime_str = "{} {}".format(datetime_str, "00:00:00")
    unaware_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return pytz.timezone(settings.TIME_ZONE).localize(unaware_date)


def get_end_datetime_from_date_string(datetime_str):
    datetime_str = "{} {}".format(datetime_str, "23:59:59")
    unaware_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return pytz.timezone(settings.TIME_ZONE).localize(unaware_date)


def get_datetime_range_from_date_string(datetime_str):
    datetime_start_str = "{} {}".format(datetime_str, "00:00:00")
    datetime_end_str = "{} {}".format(datetime_str, "23:59:59")
    unaware_start_date = datetime.strptime(datetime_start_str, "%Y-%m-%d %H:%M:%S")
    unaware_end_date = datetime.strptime(datetime_end_str, "%Y-%m-%d %H:%M:%S")
    return pytz.timezone(settings.TIME_ZONE).localize(unaware_start_date), pytz.utc.localize(unaware_end_date),


def get_date_from_date_string(date_str):
    datetime_str = "{} {}".format(date_str, "00:00:00")
    unaware_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    pytz.timezone(settings.TIME_ZONE).localize(unaware_date)
    return unaware_date.date()


def get_time_from_string(time_str):
    unaware_time = datetime.strptime(time_str, '%H:%M').time()
    return pytz.timezone(settings.TIME_ZONE).localize(unaware_time)


def get_interval_between_time(start, end, length, date):
    intervals = []
    start = datetime.combine(get_date_from_date_string(date), start)
    end = datetime.combine(get_date_from_date_string(date), end)

    while start < end:
        end_time = (start + timedelta(minutes=length))
        end_time = (end_time - timedelta(seconds=1))
        interval = {
            "start": start,
            "end": end_time,
            "available": True
        }
        start = (end_time + timedelta(seconds=1))
        intervals.append(interval)

    return intervals


