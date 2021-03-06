import json
import logging
import os


class MBConfig:
    def __init__(self, path: str = None):
        """
        Create an MBConfig instance to read application configuration.

        :param str path: Path to configuration
        """
        logging.getLogger().info(f' Configuration path is: {path}')
        self._config_path = path
        self._apptoto_api_token = None
        self._apptoto_calendar = None
        self._apptoto_user = None

    def _read_config(self):
        if self._config_path:
            with open(os.path.join(self._config_path, 'config.json')) as f:
                configuration = json.load(f)
                self._apptoto_api_token = configuration['apptoto_api_token']
                self._apptoto_calendar = configuration['apptoto_calendar']
                self._apptoto_user = configuration['apptoto_user']

    def get_apptoto_api_token(self):
        if self._apptoto_api_token is None:
            self._read_config()
        return self._apptoto_api_token

    def get_apptoto_calendar(self):
        if self._apptoto_calendar is None:
            self._read_config()
        return self._apptoto_calendar

    def get_apptoto_user(self):
        if self._apptoto_user is None:
            self._read_config()
        return self._apptoto_user
