import pytest
from motivationalboost.flask_app import create_app
from motivationalboost.mbconfig import MBConfig


@pytest.fixture
def app():
    mbconfig = MBConfig(path=None)
    mbconfig.qualtrics_api_token = 'test_api_token'
    mbconfig.survey_id = 'test_survey_id'
    mbconfig.apptoto_user = 'test_apptoto_user'
    mbconfig.apptoto_api_token = 'test_api_token'

    app = create_app({
        'TESTING': True,
        'MBCONFIG': mbconfig
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
