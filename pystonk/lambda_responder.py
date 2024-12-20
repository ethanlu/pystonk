from pystonk import logger
from pystonk.slack_app import mention, slash_command


def start(event, context):
    logger.debug(event)
    logger.debug(context)

    match event['f']:
        case 'slash_command': slash_command(event['p'])
        case 'mention': mention(event['p'])
