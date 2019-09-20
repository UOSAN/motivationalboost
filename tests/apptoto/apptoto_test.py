import requests
from apptoto import Apptoto
from apptoto_event import ApptotoEvent

_endpoint = 'https://api.apptoto.com/v1'
_api_token = 'test_api_token'
_user = 'test_user'


class TestApptoto:
    def test_post_events_success(self, requests_mock, capsys):
        # Arrange
        a = Apptoto(api_token=_api_token, user=_user)
        url = f'{_endpoint}/events'
        events = [ApptotoEvent(calendar='', title='', start_time='', end_time='', content='', participants=[])]
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
        events = [ApptotoEvent(calendar='', title='', start_time='', end_time='', content='', participants=[])]
        requests_mock.post(url=url,
                           status_code=requests.codes.bad_request)

        # Act
        a.post_events(events)

        # Assert
        captured = capsys.readouterr()
        assert captured.out == ''