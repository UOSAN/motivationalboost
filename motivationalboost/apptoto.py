from typing import List

import jsonpickle
import requests
from requests.auth import HTTPBasicAuth

from .apptoto_event import ApptotoEvent


class Apptoto:
    def __init__(self, api_token: str, user: str):
        self._endpoint = 'https://api.apptoto.com/v1'
        self._api_token = api_token
        self._user = user
        self._headers = {'Content-Type': 'application/json'}
        self._timeout = 5

    def post_events(self, events: List[ApptotoEvent]):
        r"""
        Post events to the /v1/events API to create events that will send messages to all participants.
        :param events: 
        """
        url = f'{self._endpoint}/events'
        request_data = jsonpickle.encode({'events': events, 'prevent_calendar_creation': True}, unpicklable=False)
        r = requests.post(url=url,
                          data=request_data,
                          headers=self._headers,
                          timeout=self._timeout,
                          auth=HTTPBasicAuth(username=self._user, password=self._api_token))

        if r.status_code == requests.codes.ok:
            print('Posted events to Apptoto')
