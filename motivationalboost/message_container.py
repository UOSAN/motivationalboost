import json
import logging
from pathlib import Path
from typing import List, Set, Optional

from .message import Message


class MessageContainer:
    def __init__(self, template_path: Path = Path.cwd() / 'templates'):
        """
        Create a MessageContainer instance.

        :param Path template_path: Path to message templates
        """
        self._container = {}
        try:
            with open(str(template_path / 'message_template.json')) as f:
                template_string = json.load(f)
                for survey_id, message_templates in template_string.items():
                    messages = [Message(m['content'], m['schedule'], m['start_date'], m['start_time'], m['title'])
                                for m in message_templates]
                    self._container[survey_id] = messages
        except (FileNotFoundError, KeyError):
            # Explicitly ignore FileNotFoundErrors and create an empty container.
            # Explicitly ignore KeyErrors, and create an empty container.
            logging.getLogger().info(f'Unable to load message templates from directory: {str(template_path)}')

    def __len__(self):
        return len(self._container)

    def get_messages(self, survey_id: str) -> Optional[List[Message]]:
        return self._container.get(survey_id)

    def get_placeholders(self, survey_id: str) -> Set[str]:
        """
        Get all the placeholders in all the messages.
        :return: a set of the placeholder strings
        """
        placeholders = set()
        for m in self._container[survey_id]:
            placeholders = placeholders | set(m.get_placeholders())

        return placeholders
