from __future__ import print_function
from splitwise_oauth.callback import SplitwiseCallbackHandler
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def respond_html(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'text/html',
        },
    }


def handler(event, context):
    logging.debug("Processing splitwise callback event V2." + json.dumps(event, indent=2))
    response = SplitwiseCallbackHandler(event, context).process_event()
    return respond(None, res=response)


def lambda_handler(event, context):
    logging.debug("Processing splitwise callback event V2." + json.dumps(event, indent=2))
    response = SplitwiseCallbackHandler(event, context).process_event_html()
    return respond_html(None, res=response)
