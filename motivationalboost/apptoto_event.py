from datetime import datetime
from typing import List

from apptoto_participant import ApptotoParticipant


class ApptotoEvent:
    r"""
    Represents a single event. Messages will be sent at start_time to all participants.
    """
    def __init__(self, calendar: str, title: str, start_time: datetime, end_time: datetime,
                 content: str, participants: List[ApptotoParticipant]):
        self.calendar = calendar
        self.title = title
        self.start_time = start_time.isoformat()
        self.end_time = end_time.isoformat()
        self.content = content
        self.participants = participants
