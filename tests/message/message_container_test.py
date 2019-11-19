import shutil
from src.motivationalboost.message_container import MessageContainer


class TestMessageContainer:
    def test_constructor_empty_file(self, tmp_path, shared_datadir):
        # Create an empty file in test-controlled path
        template_path = tmp_path / 'templates'
        template_path.mkdir()
        shutil.copyfile((shared_datadir / 'empty.json'), template_path / 'module1_template.json')

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
        shutil.copyfile((shared_datadir / 'valid.json'), template_path / 'module1_template.json')

        message_container = MessageContainer(template_path=template_path)

        assert len(message_container) == 2
