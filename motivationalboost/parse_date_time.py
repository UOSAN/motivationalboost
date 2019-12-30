from datetime import datetime

import dateutil


def parse_datetime_string(datetime_string: str) -> datetime:
    """
    Parse date time strings with or without minutes, with format:
    '%m-%d-%Y %I:%M%p' (i.e., '08-04-2019 2:30pm') or
    '%m-%d-%Y %I%p' (i.e., '08-04-2019 2pm')
    """
    tz = dateutil.tz.gettz('America/Los_Angeles')
    try:
        temp = datetime.strptime(datetime_string, '%m-%d-%Y %I:%M%p')
        return temp.replace(tzinfo=tz)
    except ValueError:
        temp = datetime.strptime(datetime_string, '%m-%d-%Y %I%p')
        return temp.replace(tzinfo=tz)
