import re
from string import Template
from typing import List


class Message:
    def __init__(self, content: str, schedule: str, start_date: str, start_time: str, title: str):
        self._content_template = Template(content)
        self._schedule_template = schedule
        self._start_date_template = Template(start_date)
        self._start_time_template = Template(start_time)
        self._title_template = Template(title)

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

    def get_content(self) -> str:
        """Return the substituted template content string"""
        pass

    def get_title(self) -> str:
        """Return the substituted template title string"""
        pass

    def get_start_date_time(self) -> str:
        """Return the substituted date time string"""
        pass
