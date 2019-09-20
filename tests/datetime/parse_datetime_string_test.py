import datetime
from parse_date_time import parse_datetime_string


class TestParseDateTime:
    def test_lowercase_am_pm(self):
        datetime_string = '08-04-2019 2:30pm'
        expected_datetime = datetime.datetime(2019, 8, 4, hour=14, minute=30)
        assert expected_datetime == parse_datetime_string(datetime_string)

    def test_uppercase_am_pm(self):
        datetime_string = '08-04-2019 2:30AM'
        expected_datetime = datetime.datetime(2019, 8, 4, hour=2, minute=30)
        assert expected_datetime == parse_datetime_string(datetime_string)

    def test_with_minutes(self):
        datetime_string = '08-04-2019 2:30pm'
        expected_datetime = datetime.datetime(2019, 8, 4, hour=14, minute=30)
        assert expected_datetime == parse_datetime_string(datetime_string)

    def test_without_minutes(self):
        datetime_string = '08-04-2019 2pm'
        expected_datetime = datetime.datetime(2019, 8, 4, hour=14)
        assert expected_datetime == parse_datetime_string(datetime_string)
