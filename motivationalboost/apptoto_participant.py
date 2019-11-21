class ApptotoParticipant:
    r"""
    Represents a single participant on an ApptotoEvent. This participant will receive messages
    via email or phone.
    """
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone
