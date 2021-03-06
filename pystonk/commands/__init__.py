from pystonk.commands.CommandHelp import CommandHelp
from pystonk.utils.LoggerMixin import LoggerMixin
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.ErrorView import ErrorView
from pystonk.views.HelpView import HelpView

from abc import abstractmethod
from argparse import ArgumentError, Namespace, RawDescriptionHelpFormatter
from typing import Type

import re


class Command(LoggerMixin):
    def __init__(self):
        # options available to all commands
        self._common_parser = CustomArgParser(
            add_help=False,
            exit_on_error=False,
            formatter_class=RawDescriptionHelpFormatter
        )
        self._common_parser.add_argument('-v', '--verbose', action='store_true', help='return detailed information')

    @property
    def common_parser(self):
        return self._common_parser

    @property
    @abstractmethod
    def command_regex(self) -> re.Pattern:
        pass

    @property
    @abstractmethod
    def parser(self) -> CustomArgParser:
        pass

    @abstractmethod
    def process(self, args: Namespace) -> Type[View]:
        pass

    def help(self) -> CommandHelp:
        return CommandHelp(self.__class__.__name__, self.parser.description, self.parser.prog, self.parser.get_positional_actions(), self.parser.get_optional_actions())

    def execute(self, s: str) -> Type[View]:
        try:
            self.logger.debug(f"parsing arguments ({s}) for command : {self.__class__.__name__}")
            args = self.parser.parse_args(s.split(' ')[1:])
            self.logger.debug(f"parsed arguments : {args}")

            view = self.process(args)
            view.verbose = args.verbose
        except ArgumentError as e:
            view = HelpView([self.help()], message=e.message)
        except:
            self.logger.exception(f"Unexpected error while processing command...")
            view = ErrorView(f"Unexpected error while processing command...some shit broke! Tell creator to check logs and fix it!")

        return view
