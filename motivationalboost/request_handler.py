from typing import Set, Mapping

from .apptoto import Apptoto
from .apptoto_event import ApptotoEvent
from .apptoto_participant import ApptotoParticipant
from .mbconfig import MBConfig
from .message_container import MessageContainer

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
    def __init__(self, config: MBConfig, survey_output: Mapping[str, str]):
        self._config = config
        self._survey_output = survey_output

    def handle_request(self):
        # Create Apptoto context
        apptoto = Apptoto(api_token=self._config.get_apptoto_api_token(), user=self._config.get_apptoto_user())
        message_templates = MessageContainer()
        part = ApptotoParticipant(name=self._survey_output.get('name'), phone=self._survey_output.get('phone'))

        events = []
        for message in message_templates.get_messages():
            # set the placeholders
            message.set_placeholders(self._survey_output)
            # Create an Apptoto event from it
            events.append(ApptotoEvent(calendar=self._config.get_apptoto_calendar(), title=message.get_title(),
                                       start_time=message.get_message_time(), end_time=message.get_message_time(),
                                       content=message.get_content(), participants=[part]))
        if len(events) > 0:
            apptoto.post_events(events)
