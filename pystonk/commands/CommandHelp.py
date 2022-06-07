from argparse import Action
from typing import List

import re

capital_regex = re.compile(r"[A-Z][^A-Z]*", re.ASCII)


class CommandHelp(object):
    def __init__(self, name: str, description: str, command: str, required_parameters: List[Action], optional_parameters: List[Action]):
        self._name = ' '.join(capital_regex.findall(name)[:-1])
        self._description = description
        self._command = command
        self._required_parameters = required_parameters
        self._optional_parameters = optional_parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def command(self) -> str:
        return self._command

    @property
    def required_parameters(self) -> List[Action]:
        return self._required_parameters

    @property
    def optional_parameters(self) -> List[Action]:
        return self._optional_parameters
