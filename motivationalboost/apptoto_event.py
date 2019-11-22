from typing import List
from apptoto_participant import ApptotoParticipant


class ApptotoEvent:
    r"""
    Represents a single event. Messages will be sent at start_time to all participants.
    """
    def __init__(self, calendar: str, title: str, start_time: str, end_time: str,
                 content: str, participants: List[ApptotoParticipant]):
        self.calendar = calendar
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.content = content
        self.participants = participants
