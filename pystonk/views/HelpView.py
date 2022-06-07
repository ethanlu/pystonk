from pystonk.commands import CommandHelp
from pystonk.views import View

from typing import Dict, List

import random


class HelpView(View):
    def __init__(self, help: List[CommandHelp]):
        super().__init__()

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
            },
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
            usage_text = h.command
            required_text = []
            optional_text = []

            if len(h.required_parameters) > 0:
                usage_text += ' {' + '} {'.join([action.dest for action in h.required_parameters]) + '}'
                required_text = [f"`{action.dest}:{action.type.__name__}` - {action.help}" for action in h.required_parameters]
            if len(h.optional_parameters) > 0:
                usage_text += ' [' + '] ['.join([', '.join(action.option_strings) for action in h.optional_parameters]) + ']'
                optional_text = [f"`{', '.join(action.option_strings)}` - {action.help}" for action in h.optional_parameters]

            response += [
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{h.name}* \n{h.description} \n\n" +
                                f"Usage: \n\t\t `{usage_text}` \n\n" +
                                f"Required Parameters: \n\t\t" + "\n\t\t".join(required_text) + "\n\n" +
                                f"Optional Parameters: \n\t\t" + "\n\t\t".join(optional_text) + "\n\n"
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
