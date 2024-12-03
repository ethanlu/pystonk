from pystonk.commands import CommandHelp
from pystonk.views import View

from typing import Dict, List

import random


class HelpView(View):
    def __init__(self, help: List[CommandHelp], message: str = None):
        super().__init__()

        self._message = message
        self._help = help

    def show_text(self) -> str:
        return "Invalid command"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_FAIL_EMOJI)} \n I didn't understand what you wanted to do..."
                }
            }
        ]

        if self._message:
            response += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{self._message}```"
                    }
                }
            ]

        if len(self._help) == 1:
            response += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Here are the details of the command:"
                    }
                }
            ]
        else:
            response += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Here are the available commands:"
                    }
                }
            ]

        for h in self._help:
            required_usage = ""
            optional_usage = ""
            required_text = []
            optional_text = []

            if len(h.required_parameters) > 0:
                for action in h.required_parameters:
                    required_usage += ' {' + action.dest + '}'
                    required_text.append(f"`{action.dest}:{action.type.__name__}` - {action.help}")
            if len(h.optional_parameters) > 0:
                for action in h.optional_parameters:
                    optional_usage += f"\n\t\t\t\t`[{', '.join(action.option_strings) + (' {choice}' if action.choices else '')}]`"
                    optional_text.append(f"`{', '.join(action.option_strings)}` - {action.help}")

            response += [
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{h.name}* \n{h.description} \n\n" +
                                f"*Usage*: \n\t\t `{h.command}{required_usage}`{optional_usage} \n\n" +
                                f"*Required Parameters*: \n\t\t" + "\n\t\t".join(required_text) + "\n\n" +
                                f"*Optional Parameters*: \n\t\t" + "\n\t\t".join(optional_text) + "\n\n"
                    }
                }
            ]

        response += [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The above command(s) are also available with the `/pystonk` slash-command, but the results will only be visible to you"
                }
            }
        ]

        return response
