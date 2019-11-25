import re
from datetime import datetime, timedelta
from dateutil import tz
from string import Template
from typing import List, Mapping

from parse_date_time import parse_datetime_string


class Message:
    def __init__(self, content: str, schedule: str, start_date: str, start_time: str, title: str):
        self._content_template = Template(content)
        self._schedule_template = schedule
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
        if self._schedule_template == '' or self._schedule_template == 'now':
            # TODO: Perhaps delay the "now" response by a few minutes to make sure it can get scheduled and sent
            return datetime.now(tz=tz.gettz('America/Los_Angeles'))
        else:
            start_date_time = f'{self._start_date_template.substitute(self._placeholders)} ' \
                              f'{self._start_time_template.substitute(self._placeholders)}'
            start = parse_datetime_string(start_date_time)

            if self._schedule_template.endswith('h'):
                start = start + timedelta(hours=int(self._schedule_template[:-1]))

            return start
