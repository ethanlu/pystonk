from argparse import ArgumentError, ArgumentParser, Action
from typing import List

class CustomArgParser(ArgumentParser):
    def error(self, message: str):
        """
        TODO : this method will no longer be needed once following bug is resolved:
            https://bugs.python.org/issue41255
        :param message:
        :return:
        """
        if not self.exit_on_error:
            raise ArgumentError(None, message)
        return ArgumentParser.error(self, message)

    def get_positional_actions(self) -> List[Action]:
        return self._get_positional_actions()

    def get_optional_actions(self) -> List[Action]:
        return self._get_optional_actions()
