from abc import ABC, abstractmethod
from prettytable import PrettyTable
from typing import List, Dict


class View(ABC):
    SLACK_PAGINATE_CHAR_LIMIT = 2600
    SLACK_OK_EMOJI = (':ro-yup:', ':ro-thumbsup:', ':perfect:', ':meme-yiss:')
    SLACK_FAIL_EMOJI = (':ro-hmm:', ':ro-sob:', ':ro-omg:', ':ro-oops:', ':ro-pff:', ':ro-sorry:', ':ro-sweat:', ':ro-question:', ':ro-exclamation:', ':think-3d:', ':where:', ':poop-animated:', ':blob_think:')
    CHART_WIDTH = 600
    CHART_HEIGHT = 400
    CHAR_PIXEL_RATIO = 2

    def __init__(self):
        self._verbose = False

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        self._verbose = verbose
        return self

    def paginate(self, table: PrettyTable, row_size: int = None) -> List[Dict]:
        # paginate by specified row size or calculate based on table dimensions
        row_size = row_size or (self.SLACK_PAGINATE_CHAR_LIMIT // len(table.get_string(start=0, end=1).split("\n")[0]))
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{table.get_string(start=i, end=(i + row_size))}```"
                }
            }
            for i in range(0, len(table.rows), row_size)
        ]

    @abstractmethod
    def show_text(self) -> str:
        """
        show results as text only when slack cannot show results as block kit elements
        :return: results as a string
        """
        pass

    @abstractmethod
    def show(self) -> List[Dict]:
        """
        show results as slack block kit (https://api.slack.com/reference/block-kit/blocks)
        :return: results as a list of dictionaries representing slack block kit elements
        """
        pass