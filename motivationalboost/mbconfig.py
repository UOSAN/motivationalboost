import json
import os


class MBConfig:
    """
    Class to read configuration for motivational boost from the environment
    """
    def __init__(self, qualtrics_api_token: str = None, apptoto_api_token: str = None,
                 apptoto_user: str = None, survey_id: str = None):
        if qualtrics_api_token and apptoto_api_token and apptoto_user and survey_id:
            self.qualtrics_api_token = qualtrics_api_token
            self.apptoto_api_token = apptoto_api_token
            self.apptoto_user = apptoto_user
            self.survey_id = survey_id
        else:
            with open(os.path.join('instance', 'config.json')) as f:
                configuration = json.load(f)
                self.qualtrics_api_token = configuration['qualtrics_api_token']
                self.apptoto_api_token = configuration['apptoto_api_token']
                self.apptoto_user = configuration['apptoto_user']
                self.survey_id = configuration['survey_id']
