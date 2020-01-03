class ApptotoParticipant:
    """
    Represents a single participant on an ApptotoEvent. This participant will receive messages
    via email or phone.
    """
    def __init__(self, name: str, phone: str, email: str = ''):
        self.name = name
        self.phone = phone
        self.email = email
