import datetime
from datetime import timezone as tz

import pytz
from dateutil import parser
from pytz import timezone


# System uses ISO dates and times in UTC internally
default_system_time_zone: tz = tz.utc
date_format = '%Y-%m-%d'

# Some parts, like in mails, user-friendly date formatting is needed
pst_date_format = '%m/%d/%Y %H:%M (%Z)'
default_user_timezone: str = 'UTC'


def date_from_iso8601(date_iso8601: str) -> datetime.date:
    return parser.parse(date_iso8601).date()


def datetime_from_iso8601(datetime_iso8601: str) -> datetime.datetime:
    return parser.parse(datetime_iso8601)


def datetime_to_iso8601_string(date: datetime.date) -> str:
    return date.isoformat()


def date_to_string(date: datetime.date | None) -> str:
    result_string = ''
    if date:
        result_string = date.strftime(date_format)
    return result_string


def datetime_from_timestamp(ts: float) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ts).replace(tzinfo=default_system_time_zone)


def get_datetime_with_time_zone(
        date: datetime.datetime,
        requested_tz: str = default_user_timezone,
        df: str = pst_date_format
) -> str:
    date = date.astimezone(timezone(requested_tz))
    return date.strftime(df)


def datetime_now_tz() -> datetime.datetime:
    return datetime.datetime.now(tz=default_system_time_zone)


def date_now() -> datetime.date:
    return datetime_now_tz().date()


def default_project_timezone() -> tz:
    return default_system_time_zone


def is_valid_datetime(date_string: str, str_format: str) -> bool:
    try:
        datetime.datetime.strptime(date_string, str_format)
        return True
    except ValueError:
        return False


def is_valid_timezone(tz_string: str) -> bool:
    return tz_string in pytz.all_timezones_set
