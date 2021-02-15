from motivationalboost.request_handler import RequestHandler
from motivationalboost.mbconfig import MBConfig
from motivationalboost.message_container import MessageContainer
from motivationalboost.message import Message


import unittest.mock as mock


class TestRequestHandler:
    def test_request_handler_no_messages(self):
        with mock.patch('motivationalboost.mbconfig.MBConfig.get_apptoto_api_token', return_value=''), \
             mock.patch('motivationalboost.mbconfig.MBConfig.get_apptoto_user', return_value=''), \
             mock.patch('motivationalboost.message_container.MessageContainer.get_messages', return_value=None),\
             mock.patch('motivationalboost.apptoto.Apptoto.post_events') as mock_post:
            config = MBConfig()
            survey_output = {'Q43': 'some text'}
            handler = RequestHandler(config=config, survey_output=survey_output)

            handler.handle_request()

            assert not mock_post.called

    def test_request_handler_invalid_placeholders_messages(self):
        messages = [Message(content='${invalid}', schedule='now', start_date='{invalid}', start_time='*-2h',
                            title='test title')]
        with mock.patch('motivationalboost.mbconfig.MBConfig.get_apptoto_api_token', return_value=''), \
             mock.patch('motivationalboost.mbconfig.MBConfig.get_apptoto_user', return_value=''), \
             mock.patch('motivationalboost.message_container.MessageContainer.get_messages', return_value=messages),\
             mock.patch('motivationalboost.apptoto.Apptoto.post_events') as mock_post:
            config = MBConfig()
            survey_output = {'Q43': 'some text'}
            handler = RequestHandler(config=config, survey_output=survey_output)

            handler.handle_request()

            assert not mock_post.called

    def test_request_handler_success(self):
        messages = [Message(content='${Q43}', schedule='now', start_date='07-27-2020', start_time='*-2h',
                            title='test title')]
        with mock.patch('motivationalboost.mbconfig.MBConfig.get_apptoto_api_token', return_value=''), \
             mock.patch('motivationalboost.mbconfig.MBConfig.get_apptoto_user', return_value=''), \
             mock.patch('motivationalboost.message_container.MessageContainer.get_messages', return_value=messages),\
             mock.patch('motivationalboost.apptoto.Apptoto.post_events') as mock_post:
            config = MBConfig()
            survey_output = {'Q43': 'some text'}
            handler = RequestHandler(config=config, survey_output=survey_output)

            handler.handle_request()

            assert mock_post.called
