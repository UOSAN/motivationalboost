import datetime


def parse_datetime_string(datetime_string: str) -> datetime:
    """
    Parse date time strings with or without minutes, with format:
    '%m-%d-%Y %I:%M%p' (i.e., '08-04-2019 2:30pm') or
    '%m-%d-%Y %I%p' (i.e., '08-04-2019 2pm')
    """
    try:
        return datetime.datetime.strptime(datetime_string, '%m-%d-%Y %I:%M%p')
    except ValueError:
        return datetime.datetime.strptime(datetime_string, '%m-%d-%Y %I%p')

