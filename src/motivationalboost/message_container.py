import json
from typing import List
from message import Message
import os


class MessageContainer:
    def __init__(self, template_path: os.PathLike = os.getcwd()):
        self._container = []
        try:
            with open(template_path / 'module1_template.json') as f:
                template_string = json.load(f)
                for m in template_string['messages']:
                    message = Message(m['content'], m['schedule'], m['start_date'], m['start_time'], m['title'])
                    self._container.append(message)
        except (FileNotFoundError, KeyError):
            # Explicitly ignore FileNotFoundErrors and create an empty container
            # Explicitly ignore KeyErrors, and do not create a Message object.
            pass

    def __len__(self):
        return len(self._container)

    def get_messages(self) -> List[Message]:
        return self._container
