import requests
from time import sleep
from typing import Optional


class QualtricsQuery():
    def __init__(self, survey_id: str, api_token: str):
        self._endpoint = 'https://ca1.qualtrics.com/API/v3'
        self._headers = {'X-API-TOKEN': api_token}
        self._timeout = 5
        self._survey_id = survey_id

    def qualtrics_create_response_export(self) -> Optional[str]:
        """
        Create a survey export from Qualtrics
        :return: A progress identifier
        """
        url = f'{self._endpoint}/surveys/{self._survey_id}/export-responses'
        request_data = {'format': 'json', 'compress': 'false'}
        r = requests.post(url=url, json=request_data, headers=self._headers, timeout=self._timeout)
        export_progress_id = None
        if r.status_code == requests.codes.ok:
            export_progress_id = r.json()['result']['progressId']
        return export_progress_id

    def qualtrics_get_response_export_progress(self, export_progress_id: Optional[str]) -> Optional[str]:
        """
        Get the fileId of the survey export, by repeatedly querying for progress until the status is complete
        :param export_progress_id: A progress identifier
        :return: A file identifier
        """
        if not export_progress_id:
            raise ValueError('Invalid export progressId')

        url = f'{self._endpoint}/surveys/{self._survey_id}/export-responses/{export_progress_id}'
        r = requests.get(url=url, headers=self._headers, timeout=self._timeout)
        max_count = 10
        count = 0
        while r.status_code == requests.codes.ok and r.json()['result']['status'] != 'complete' and count < max_count:
            sleep(1)
            r = requests.get(url=url, headers=self._headers)
            count += 1

        file_id = None
        if r.status_code == requests.codes.ok and r.json()['result']['status'] == 'complete':
            file_id = r.json()['result']['fileId']

        return file_id

    def qualtrics_get_response_export_file(self, file_id: str):
        """
        Get the exported survey results
        :param file_id: File identifier of the exported survey
        :return: A string in JSON format containing all survey responses
        """
        # No type hints on the return value of qualtrics_get_response_export_file because it is a big blob of JSON.
        if not file_id:
            raise ValueError('Invalid fileId. Did response export complete correctly?')

        url = f'{self._endpoint}/surveys/{self._survey_id}/export-responses/{file_id}/file'
        r = requests.get(url=url, headers=self._headers, timeout=self._timeout)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            raise ValueError('Could not get JSON response of surveys')