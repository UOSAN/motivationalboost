import requests


_endpoint = 'https://api.apptoto.com/v1/events'
_response_id = 'test_response_id'


def test_event_subscriber_bad_request(app):
    # Verify that 400 Bad Request is returned on a bad request
    with app.app_context():
        client = app.test_client()
        response = client.post('/response', data='some garbage test data', content_type='application/text')
        assert response.status == '400 BAD REQUEST'


def test_event_subscriber_valid_request(app, requests_mock):
    # Arrange. Mock the underlying call to apptoto to succeed
    requests_mock.post(url=_endpoint, status_code=requests.codes.ok)

    with app.app_context():
        client = app.test_client()
        response = client.post('/response', json={'response_id': _response_id})
        assert response.status == '200 OK'
