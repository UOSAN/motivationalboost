from datetime import datetime

import requests
from dateutil import tz

from motivationalboost.apptoto import Apptoto
from motivationalboost.apptoto_event import ApptotoEvent

_endpoint = 'https://api.apptoto.com/v1'
_api_token = 'test_api_token'
_user = 'test_user'


class TestApptoto:
    def test_post_events_success(self, requests_mock, capsys):
        # Arrange
        a = Apptoto(api_token=_api_token, user=_user)
        url = f'{_endpoint}/events'
        now = datetime.now(tz=tz.gettz('America/Los_Angeles'))
        events = [ApptotoEvent(calendar='', title='', start_time=now, end_time=now, content='', participants=[])]
        requests_mock.post(url=url,
                           status_code=requests.codes.ok)

        # Act
        a.post_events(events)

        # Assert
        captured = capsys.readouterr()
        assert captured.out == 'Posted events to Apptoto\n'

    def test_post_events_failure(self, requests_mock, capsys):
        # Verify no output in the case of failing to post events.
        # Arrange
        a = Apptoto(api_token=_api_token, user=_user)
        url = f'{_endpoint}/events'
        now = datetime.now(tz=tz.gettz('America/Los_Angeles'))
        events = [ApptotoEvent(calendar='', title='', start_time=now, end_time=now, content='', participants=[])]
        requests_mock.post(url=url,
                           status_code=requests.codes.bad_request)

        # Act
        a.post_events(events)

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ''
