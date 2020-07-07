import math
from frappe.utils.data import today, date_diff


def calculate_age(dob):
    return math.floor(
        date_diff(today(), dob) / 365
    )


def format_timedelta(timedelta, strformat):
    """
    Format [datetime.timedelta] to [str].
    Source: https://stackoverflow.com/questions/538666/format-timedelta-to-string
    :param timedelta:
    :param strformat:
    :return:
    """
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return strformat.format(hours=hours, minutes=minutes, seconds=seconds)


def timedelta_to_default_format(timedelta):
    return format_timedelta(timedelta, '{hours:02}:{minutes:02}')
