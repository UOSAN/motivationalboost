from typing import Set, Mapping

from .apptoto import Apptoto
from .apptoto_event import ApptotoEvent
from .apptoto_participant import ApptotoParticipant
from .mbconfig import MBConfig
from .message_container import MessageContainer


class RequestHandler:
    def __init__(self, config: MBConfig, survey_output: Mapping[str, str]):
        """
        Create a RequestHandler instance.

        :param MBConfig config: Application configuration
        :param Mapping[str, str] survey_output: Mapping of placeholders to values from survey output
        """
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
