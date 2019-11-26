import pytest
import requests

from motivationalboost.qualtrics import QualtricsQuery

_api_token = 'test_api_token'
_endpoint = 'https://ca1.qualtrics.com/API/v3'
_response_id = 'test_response_id'
_survey_id = 'test_survey_id'


class TestQualtricsQuery:
    def test_create_response_export_success(self, requests_mock):
        # Arrange
        expected_progress_id = 'test_progress_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses'
        requests_mock.post(url=url,
                           status_code=requests.codes.ok,
                           json={'result': {'progressId': expected_progress_id}})

        # Act
        progress_id = q.create_response_export()

        # Assert
        assert progress_id == expected_progress_id

    def test_create_response_export_invalid_response_format(self, requests_mock):
        # Test behavior when the POST request succeeds, but the returned JSON is not the expected format
        # Arrange
        expected_progress_id = 'test_progress_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses'
        requests_mock.post(url=url,
                           status_code=requests.codes.ok,
                           json={'result': {'unexpected_key': expected_progress_id}})

        # Act
        progress_id = q.create_response_export()

        # Assert
        assert progress_id is None

    def test_create_response_export_failure(self, requests_mock):
        # Arrange
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses'
        requests_mock.post(url=url,
                           status_code=requests.codes.server_error)

        # Act
        progress_id = q.create_response_export()

        # Assert
        assert progress_id is None

    def test_get_response_export_progress_success(self, requests_mock):
        # Arrange
        export_progress_id = 'test_export_progress_id'
        expected_file_id = 'test_file_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses/{export_progress_id}'
        requests_mock.get(url=url,
                          status_code=requests.codes.ok,
                          json={'result': {'status': 'complete', 'fileId': expected_file_id}})

        # Act
        file_id = q.get_response_export_progress(export_progress_id)

        # Assert
        assert expected_file_id == file_id

    def test_get_response_export_progress_success_with_retries(self, requests_mock):
        # Arrange
        export_progress_id = 'test_export_progress_id'
        expected_file_id = 'test_file_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses/{export_progress_id}'
        requests_mock.get(url=url,
                          response_list=[{'json': {'result': {'status': 'inProgress'}}, 'status_code': 200},
                                         {'json': {'result': {'status': 'complete', 'fileId': expected_file_id}}, 'status_code': 200}])

        # Act
        file_id = q.get_response_export_progress(export_progress_id)

        # Assert
        assert expected_file_id == file_id

    def test_get_response_export_progress_failure(self, requests_mock):
        # Arrange
        export_progress_id = 'test_export_progress_id'
        expected_file_id = 'test_file_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses/{export_progress_id}'
        requests_mock.get(url=url,
                          status_code=requests.codes.bad_request,
                          json={'result': {'status': 'inProgress'}})

        # Act
        file_id = q.get_response_export_progress(export_progress_id, max_retries=1)

        # Assert
        assert file_id is None

    def test_get_response_export_file_success(self, requests_mock):
        # Arrange
        file_id = 'test_file_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses/{file_id}/file'
        requests_mock.get(url=url, status_code=requests.codes.ok, json={'a': 'b'})

        # Act
        survey_responses = q.get_response_export_file(file_id)

        # Assert
        assert survey_responses == {'a': 'b'}

    def test_get_response_export_file_failure(self, requests_mock):
        # Arrange
        file_id = 'test_file_id'
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/export-responses/{file_id}/file'
        requests_mock.get(url=url, status_code=requests.codes.bad_request)

        # Assert
        with pytest.raises(ValueError):
            # Act
            q.get_response_export_file(file_id)

    def test_get_survey_definition_success(self, requests_mock):
        # Arrange
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/survey-definitions/{_survey_id}'
        requests_mock.get(url=url, status_code=requests.codes.ok, json={'a': 'b'})

        # Act
        survey_responses = q.get_survey_definition()

        # Assert
        assert survey_responses == {'a': 'b'}

    def test_get_survey_definition_failure(self, requests_mock):
        # Arrange
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/survey-definitions/{_survey_id}'
        requests_mock.get(url=url, status_code=requests.codes.bad_request)

        # Assert
        with pytest.raises(ValueError):
            # Act
            q.get_survey_definition()

    def test_get_survey_response_success(self, requests_mock):
        # Arrange
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/responses/{_response_id}'
        requests_mock.get(url=url, status_code=requests.codes.ok, json={'a': 'b'})

        # Act
        survey_response = q.get_survey_response(_response_id)

        # Assert
        assert survey_response == {'a': 'b'}

    def test_get_survey_response_failure(self, requests_mock):
        # Arrange
        q = QualtricsQuery(api_token=_api_token, survey_id=_survey_id)
        url = f'{_endpoint}/surveys/{_survey_id}/responses/{_response_id}'
        requests_mock.get(url=url, status_code=requests.codes.bad_request)

        # Assert
        with pytest.raises(ValueError):
            # Act
            q.get_survey_response(_response_id)
