import logging
from datetime import datetime

import requests
from dateutil import tz

from motivationalboost.apptoto import Apptoto
from motivationalboost.apptoto_event import ApptotoEvent

_endpoint = 'https://api.apptoto.com/v1'
_api_token = 'test_api_token'
_user = 'test_user'


class TestApptoto:
    def test_post_events_success(self, requests_mock, caplog):
        with caplog.at_level(logging.INFO):
            # Arrange
            a = Apptoto(api_token=_api_token, user=_user)
            url = f'{_endpoint}/events'
            now = datetime.now(tz=tz.gettz('America/Los_Angeles'))
            events = [ApptotoEvent(calendar='', title='', start_time=now, end_time=now, content='', participants=[])]
            requests_mock.post(url=url,
                               status_code=requests.codes.ok)

            # Act
            post = a.post_events(events)

            # Assert
            assert post
            assert 'Posted events to apptoto' in caplog.text

    def test_post_events_failure(self, requests_mock, caplog):
        with caplog.at_level(logging.INFO):
            # Verify log output in the case of failing to post events.
            # Arrange
            a = Apptoto(api_token=_api_token, user=_user)
            url = f'{_endpoint}/events'
            now = datetime.now(tz=tz.gettz('America/Los_Angeles'))
            events = [ApptotoEvent(calendar='', title='', start_time=now, end_time=now, content='', participants=[])]
            content = b'binary content'
            requests_mock.post(url=url,
                               status_code=requests.codes.bad_request,
                               content=content)

            # Act
            post = a.post_events(events)

            # Assert
            assert not post
            assert 'Failed to post' in caplog.text and str(content) in caplog.text
