from src.motivationalboost.message import Message


class TestMessage:
    def test_get_placeholders_empty_string(self):
        # Verify an empty string has no placeholders
        content = ''

        m = Message(content=content, schedule='', start_date='', start_time='', title='')

        assert len(m.get_placeholders()) == 0

    def test_get_placeholders_valid_template_string(self):
        # Verify a valid template string has placeholders
        # https://docs.python.org/3/library/string.html#template-strings
        content = 'Test ${template} string'

        m = Message(content=content, schedule='', start_date='', start_time='', title='')

        assert len(m.get_placeholders()) == 1
