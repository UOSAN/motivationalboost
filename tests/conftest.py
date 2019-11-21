import pytest
from motivationalboost import create_app
from mbconfig import MBConfig


@pytest.fixture
def app():
    mbconfig = MBConfig(qualtrics_api_token='test_api_token',
                        survey_id='test_survey_id',
                        apptoto_user='test_apptoto_user',
                        apptoto_api_token='test_api_token')

    app = create_app({
        'TESTING': True,
        'MBCONFIG': mbconfig
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
