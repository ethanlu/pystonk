from pystonk.utils.LoggerMixin import LoggerMixin

import requests


class Api(LoggerMixin):
    ACCESS_TOKEN_ENDPOINT = "https://api.schwabapi.com/v1/oauth/token"
    ACCESS_TOKEN = None

    def __init__(self, app_key: str, app_secret: str):
        if not app_key:
            raise ValueError(f"Invalid App Key : {app_key}")
        self._app_key = app_key

        if not app_secret:
            raise ValueError(f"Invalid App Secret : {app_secret}")
        self._app_secret = app_secret

    def _get(self, endpoint: str, **kwargs) -> dict:
        self.logger.debug(f"get endpoint: {endpoint}")
        self.logger.debug(f"get details: {kwargs}")
        response = requests.get(endpoint, **kwargs)
        self.logger.debug(f"get response : {response.status_code}")
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, **kwargs) -> dict:
        self.logger.debug(f"post endpoint: {endpoint}")
        self.logger.debug(f"post details: {kwargs}")
        response = requests.post(endpoint, **kwargs)
        self.logger.debug(f"post response : {response.status_code}")
        response.raise_for_status()
        return response.json()

    def get_access_token(self) -> str:
        if not self.__class__.ACCESS_TOKEN:
            data = self._post(
                self.ACCESS_TOKEN_ENDPOINT,
                data={'grant_type': "client_credentials", 'scope': 'pystonk'},
                auth=(self._app_key, self._app_secret)
            )

            if not data or 'access_token' not in data:
                raise ValueError(f"access token retreival returned successfully, but data was unrecognized : {data}")

            self.__class__.ACCESS_TOKEN = data['access_token']
        return self.__class__.ACCESS_TOKEN
