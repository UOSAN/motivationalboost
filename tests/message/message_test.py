from datetime import datetime
from dateutil import tz

from motivationalboost.message import Message


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

    def test_get_message_time_relative_time(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = '-2h'
        placeholders = {'PH01': '08-04-2019', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Expected time is two hours before start_time, because of the relative offset from schedule
        expected = datetime(year=2019, month=8, day=4, hour=14, minute=30, tzinfo=tz.gettz('America/Los_Angeles'))

        assert m.get_message_time() == expected

    def test_get_message_time_now(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = 'now'
        placeholders = {'PH01': '08-04-2019', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Verify that message_time is essentially now.
        expected = datetime.now(tz=tz.gettz('America/Los_Angeles'))

        assert (m.get_message_time() - expected).microseconds < 1000

    def test_get_message_time_missing_schedule(self):
        start_date = '${PH01}'
        start_time = '${PH02}'
        schedule = ''
        placeholders = {'PH01': '08-04-2019', 'PH02': '4:30pm'}

        m = Message(content='', schedule=schedule, start_date=start_date, start_time=start_time, title='')
        m.set_placeholders(placeholders=placeholders)

        # Verify that message_time is essentially now.
        expected = datetime.now(tz=tz.gettz('America/Los_Angeles'))
        assert (m.get_message_time() - expected).microseconds < 1000
