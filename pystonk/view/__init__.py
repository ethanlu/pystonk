from abc import ABC, abstractmethod
from typing import List


class View(ABC):
    SLACK_BLOCK_LIMIT = 35
    SLACK_OK_EMOJI = (':ro-yup:', ':ro-thumbsup:', ':perfect:', ':meme-yiss:')
    SLACK_FAIL_EMOJI = (':ro-hmm:', ':ro-sob:', ':ro-omg:', ':ro-oops:', ':ro-pff:', ':ro-sorry:', ':ro-sweat:', ':ro-question:', ':ro-exclamation:', ':think-3d:', ':where:', ':poop-animated:', ':blob_think:')
    CHART_WIDTH = 600
    CHART_HEIGHT = 400
    CHAR_PIXEL_RATIO = 2

    def __init__(self):
        pass

    @abstractmethod
    def show(self) -> List:
        pass
