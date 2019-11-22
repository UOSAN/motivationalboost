import pytest
import requests


_api_token = 'test_api_token'
_endpoint = 'https://ca1.qualtrics.com/API/v3'
_response_id = 'test_response_id'
_survey_id = 'test_survey_id'


def test_event_subscriber_bad_data(app):
    with app.app_context():
        client = app.test_client()
        response = client.post('/response', data={'a': 'b'})
        assert response.status == '200 OK'


def test_event_subscriber_invalid_response_id(app, requests_mock):
    # Arrange. Mock the underlying call to qualtrics to throw ValueError because response_id is not valid
    url = f'{_endpoint}/surveys/{_survey_id}/responses/{_response_id}'
    requests_mock.get(url=url, status_code=requests.codes.bad_request)

    with app.app_context():
        client = app.test_client()
        # Assert
        with pytest.raises(ValueError):
            # Act
            client.post('/response', data={'ResponseID': _response_id})
