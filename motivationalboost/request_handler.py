from typing import Set, Mapping

from mbconfig import MBConfig
from qualtrics import QualtricsQuery
from apptoto import Apptoto
from apptoto_event import ApptotoEvent
from apptoto_participant import ApptotoParticipant
from message_container import MessageContainer

VALUES = 'values'
LABELS = 'labels'
PARTICIPANT_NAME = 'QID3'
PARTICIPANT_EMAIL = ''
PARTICIPANT_PHONE = 'QID1'


def get_placeholder_value_mapping(response, placeholders: Set[str]) -> Mapping[str, str]:
    # Consider only finished survey responses
    values = response[VALUES]
    mapping = {}
    if values['finished'] == 1:
        # Get a mapping of each placeholder in the messages to the values from the survey
        for p in placeholders:
            mapping[p] = values[p]

    return mapping


class RequestHandler:
    def __init__(self, config: MBConfig, response_id: str = None):
        self._config = config
        self._response_id = response_id

    def handle_request(self):
        q = QualtricsQuery(survey_id=self._config.survey_id,
                           api_token=self._config.qualtrics_api_token)
        response = q.get_survey_response(response_id=self._response_id)

        # Create Apptoto context
        apptoto = Apptoto(api_token=self._config.apptoto_api_token, user=self._config.apptoto_user)
        message_templates = MessageContainer()
        placeholder_values = get_placeholder_value_mapping(response, message_templates.get_placeholders())
        part = ApptotoParticipant(name=response[VALUES][PARTICIPANT_NAME], email='', phone=response[VALUES][PARTICIPANT_PHONE])

        for message in message_templates.get_messages():
            # set the placeholders
            message.set_placeholders(placeholder_values)
            # Create an Apptoto event from it
            ee = ApptotoEvent(calendar='', title=message.get_title(), start_time=message.get_message_time(),
                              end_time=message.get_message_time(), content=message.get_content(),
                              participants=[part])
            apptoto.post_events([ee])

