import json
import logging
from pathlib import Path
from typing import List, Set

from .message import Message


class MessageContainer:
    def __init__(self, template_path: Path = Path.cwd() / 'templates'):
        self._container = []
        try:
            with open(str(template_path / 'module1_template.json')) as f:
                template_string = json.load(f)
                for m in template_string['messages']:
                    message = Message(m['content'], m['schedule'], m['start_date'], m['start_time'], m['title'])
                    self._container.append(message)
        except (FileNotFoundError, KeyError):
            # Explicitly ignore FileNotFoundErrors and create an empty container.
            # Explicitly ignore KeyErrors, and create an empty container.
            logging.getLogger().info(f'Unable to load message templates from directory: {str(template_path)}')

    def __len__(self):
        return len(self._container)

    def get_messages(self) -> List[Message]:
        return self._container

    def get_placeholders(self) -> Set[str]:
        """
        Get all the placeholders in all the messages
        :return: a set of the placeholder strings
        """
        placeholders = set()
        for m in self._container:
            placeholders = placeholders | set(m.get_placeholders())

        return placeholders
