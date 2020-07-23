from datetime import datetime, date

import pytest
from dateutil import tz

from motivationalboost.message import Message


def get_expected_date(start_date_str: str) -> date:
    temp_date = datetime.strptime(start_date_str, '%m-%d-%Y')
    return date(temp_date.year, temp_date.month, temp_date.day)


class TestMessage:
    def test_get_placeholders_empty_string(self):
        # Verify an empty string has no placeholders
        content = ''

        m = Message(content=content, schedule='', start_date='', start_time='', title='')

        assert len(m.get_placeholders()) == 0

    def test_get_placeholders_valid_template_string(self):
        # Verify a valid template string has placeholders
        # https://docs.python.org/3/library/string.html#template-strings
        content = 'Test ${template} string'

        m = Message(content=content, schedule='', start_date='', start_time='', title='')

        assert len(m.get_placeholders()) == 1

    def test_get_content(self):
        content = 'Test ${PH01} string ${PH02}'
        placeholders = {'PH01': 'failure', 'PH02': 'cheese'}

        m = Message(content=content, schedule='', start_date='', start_time='', title='')
        m.set_placeholders(placeholders=placeholders)

        actual = m.get_content()

        assert actual == 'Test failure string cheese'
        # Verify that title is an empty string because it has no placeholders
        assert m.get_title() == ''

    def test_get_title(self):
        title = 'Test ${PH01} string ${PH02}'
        placeholders = {'PH01': 'failure', 'PH02': 'cheese'}

        m = Message(content='', schedule='', start_date='', start_time='', title=title)
        m.set_placeholders(placeholders=placeholders)

        actual = m.get_title()

        assert actual == 'Test failure string cheese'

        # Verify that content is an empty string because it has no placeholders
        assert m.get_content() == ''

    def test_get_message_time_relative_time_hours(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = '-2h'
        placeholders = {'PH01': '07-25-2020', 'PH02': '1pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Expected time is two hours before start_time, because of the relative offset from schedule
        temp = get_expected_date(placeholders['PH01'])
        expected = datetime(year=temp.year, month=temp.month, day=temp.day, hour=11, minute=0,
                            tzinfo=tz.gettz('America/Los_Angeles'))

        assert m.get_message_time() == expected

    def test_get_message_time_relative_time_days(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = '-1d'
        placeholders = {'PH01': '07-25-2020', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Expected time is one day before start_time, because of the relative offset from schedule
        temp = get_expected_date(placeholders['PH01'])
        expected = datetime(year=temp.year, month=temp.month, day=temp.day - 1, hour=16, minute=30,
                            tzinfo=tz.gettz('America/Los_Angeles'))

        assert m.get_message_time() == expected

    def test_get_message_time_now(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = 'now'
        placeholders = {'PH01': '07-25-2020', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Verify that message_time is essentially now.
        expected = datetime.now(tz=tz.gettz('America/Los_Angeles'))

        assert (m.get_message_time() - expected).microseconds < 1000

    def test_get_message_time_missing_schedule(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = ''
        placeholders = {'PH01': '07-25-2020', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Verify that message_time is essentially now.
        expected = datetime.now(tz=tz.gettz('America/Los_Angeles'))
        assert (m.get_message_time() - expected).microseconds < 1000

    @pytest.mark.parametrize('start_date_str', ['01-02-2017', '03-04-2018', '05-06-2019', '07-08-2020', '09-10-2021',
                                                '11-12-2022', '12-31-2023'])
    def test_get_message_time(self, start_date_str):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = '-2h'
        placeholders = {'PH01': start_date_str, 'PH02': '1pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Expected time is two hours before start_time, because of the relative offset from schedule
        temp = get_expected_date(placeholders['PH01'])
        expected = datetime(year=temp.year, month=temp.month, day=temp.day, hour=11, minute=0,
                            tzinfo=tz.gettz('America/Los_Angeles'))

        assert m.get_message_time() == expected

    def test_get_message_time_invalid_date_string(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = '-2h'
        placeholders = {'PH01': 'Invalid date string', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Verify ValueError exception is raised when input date string is invalid.
        with pytest.raises(ValueError):
            m.get_message_time()
