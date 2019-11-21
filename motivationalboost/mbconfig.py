import json


class MBConfig:
    """
    Class to read configuration for motivational boost from the environment
    """
    def __init__(self):
        with open('config.json') as f:
            configuration = json.load(f)
            self.qualtrics_api_token = configuration['qualtrics_api_token']
            self.apptoto_api_token = configuration['apptoto_api_token']
            self.apptoto_user = configuration['apptoto_user']
            self.survey_id = configuration['survey_id']
