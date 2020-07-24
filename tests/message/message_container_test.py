import shutil

from motivationalboost.message_container import MessageContainer


class TestMessageContainer:
    def test_constructor_empty_file(self, tmp_path, shared_datadir):
        # Create an empty file in test-controlled path
        template_path = tmp_path / 'templates'
        template_path.mkdir()
        shutil.copyfile((shared_datadir / 'empty.json'), template_path / 'message_template.json')

        message_container = MessageContainer(template_path=template_path)

        assert len(message_container) == 0

    def test_constructor_no_file(self, tmp_path):
        # Test when there is not file in template path
        template_path = tmp_path

        message_container = MessageContainer(template_path=template_path)

        assert len(message_container) == 0

    def test_container_with_messages(self, tmp_path, shared_datadir):
        # Create a valid file in test-controlled path, and verify that the two messages are read
        template_path = tmp_path / 'templates'
        template_path.mkdir()
        shutil.copyfile((shared_datadir / 'valid.json'), template_path / 'message_template.json')

        message_container = MessageContainer(template_path=template_path)
        messages = message_container.get_messages(survey_id='SV_1234')

        assert len(messages) == 2

    def test_container_invalid_survey_id(self, tmp_path, shared_datadir):
        # Create a valid file in test-controlled path, and verify that the two messages are read
        template_path = tmp_path / 'templates'
        template_path.mkdir()
        shutil.copyfile((shared_datadir / 'valid.json'), template_path / 'message_template.json')

        message_container = MessageContainer(template_path=template_path)
        messages = message_container.get_messages(survey_id='invalid_survey_id')

        assert messages is None

    def test_get_placeholders(self, tmp_path, shared_datadir):
        # Create a valid file in test-controlled path, and verify the set of placeholders returned
        template_path = tmp_path / 'templates'
        template_path.mkdir()
        shutil.copyfile((shared_datadir / 'valid.json'), template_path / 'message_template.json')

        message_container = MessageContainer(template_path=template_path)

        placeholders = message_container.get_placeholders(survey_id='SV_1234')
        expected_placeholders = {'QID03', 'QID41', 'QID42', 'QID47', 'QID48', 'QID30', 'QID23'}

        assert len(placeholders) == 7
        assert len(placeholders - expected_placeholders) == 0

    def test_container_with_multiple_groups_of_message_templates(self, tmp_path, shared_datadir):
        # Create a valid file in test-controlled path, and verify that the there are two
        # groups of message templates with different numbers of message templates
        template_path = tmp_path / 'templates'
        template_path.mkdir()
        shutil.copyfile((shared_datadir / 'multiple.json'), template_path / 'message_template.json')

        message_container = MessageContainer(template_path=template_path)
        messages = message_container.get_messages(survey_id='SV_1234')

        assert len(messages) == 2

        messages = message_container.get_messages(survey_id='SV_abcd')

        assert len(messages) == 3
