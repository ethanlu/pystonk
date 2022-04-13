from pystonk.utils.LoggerMixin import LoggerMixin


class API(LoggerMixin):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError(f"Invalid API Key : {api_key}")
        self._api_key = api_key