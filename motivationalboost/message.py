import re
from datetime import datetime, timedelta
from string import Template
from typing import List, Mapping

from dateutil import tz, relativedelta

from .parse_date_time import parse_datetime_string

day_to_delta = {'Monday': relativedelta.MO,
                'Tuesday': relativedelta.TU,
                'Wednesday': relativedelta.WE,
                'Thursday': relativedelta.TH,
                'Friday': relativedelta.FR,
                'Saturday': relativedelta.SA,
                'Sunday': relativedelta.SU}


class Message:
    def __init__(self, content: str, schedule: str, start_date: str, start_time: str, title: str):
        self._content_template = Template(content)
        self._schedule = schedule
        self._start_date_template = Template(start_date)
        self._start_time_template = Template(start_time)
        self._title_template = Template(title)
        self._placeholders = None

    def get_placeholders(self) -> List[str]:
        """Return a set of all the placeholders in the message"""
        # Copied the pattern for string templates from CPython:
        # https://github.com/python/cpython/blob/master/Lib/string.py#L78
        delimiter = re.escape('$')
        bid = r'(?a:[_a-z][_a-z0-9]*)'
        pattern = fr"""
                {delimiter}(?:
                      {{(?P<braced>{bid})}}   # delimiter and a braced identifier
                    )
        """
        p = re.compile(pattern, re.IGNORECASE | re.VERBOSE)
        return p.findall(self._content_template.template)

    def set_placeholders(self, placeholders: Mapping[str, str]):
        self._placeholders = placeholders

    def get_content(self) -> str:
        """Return the substituted template content string"""
        return self._content_template.substitute(self._placeholders)

    def get_title(self) -> str:
        """Return the substituted template title string"""
        return self._title_template.substitute(self._placeholders)

    def get_message_time(self) -> datetime:
        """
        Get the date time that the message should be sent
        :return: a datetime in the 'America/Los_Angeles' timezone
        """
        if self._schedule == '' or self._schedule == 'now':
            return datetime.now(tz=tz.gettz('America/Los_Angeles')) + timedelta(minutes=2)
        else:
            # The text in the start_date_template placeholder is actually the next weekday,
            # so get the today's day, and then find the next weekday, then add the time for
            # the reminder, modify per the schedule provided, then return the correct datetime.

            # If start_day is the same as today, then calculate a time next week.
            start_day = self._start_date_template.substitute(self._placeholders)

            delta = day_to_delta.get(start_day, None)
            today = datetime.now(tz=tz.gettz('America/Los_Angeles')).date().today()

            if delta:
                start_date = today + relativedelta.relativedelta(days=1, weekday=delta)
            else:
                start_date = today

            sss = start_date.strftime('%m-%d-%Y')
            start_date_time = f'{sss} ' \
                              f'{self._start_time_template.substitute(self._placeholders)}'
            start = parse_datetime_string(start_date_time)

            if self._schedule.endswith('h'):
                start = start + timedelta(hours=int(self._schedule[:-1]))
            elif self._schedule.endswith('d'):
                start = start + timedelta(days=int(self._schedule[:-1]))

            return start
