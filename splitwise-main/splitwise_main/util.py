import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from splitwise_main.expense_manager import SplitwiseOAuthManager


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }

def initiate_oauth(userId):
    sauth = SplitwiseOAuthManager(userId)
    auth_url = sauth.request_authorized_url()
    oauth_msg = {'contentType': 'PlainText',
                 'content': "I can't access your splitwise account yet. \r "
                            "Please authorize me using this url {}\r\r\r "
                            "Have you finished login? ".format(auth_url)}
    return oauth_msg

def get_token_from_db(userId):
    logger.info('Getting token from db for user %s' %userId)
    sauth = SplitwiseOAuthManager(userId)
    return sauth.get_access_token()


def is_logged_in(userid, intent):
    # here goto dynamodb to see if token is present
    token = None
    if intent['sessionAttributes']:
        logger.info("session attrs are not empty")
        token = intent['sessionAttributes'].get('access_token', None)
        if not token:
            token = get_token_from_db(userid)
            intent['sessionAttributes']['access_token'] = str(token)
    else:
        logger.info("session attrs are empty")
        token = get_token_from_db(userid)
        intent['sessionAttributes'] = { 'access_token' : str(token) }

    return token


def prompt_for_login(intent):
    if not is_logged_in(intent['userId'], intent):
        logger.info('Token is not present. Now asking for login confirmation with %s' % intent)
        return confirm_intent(intent['sessionAttributes'],
                              intent['currentIntent']['name'],
                              get_slots(intent),
                              initiate_oauth(intent['userId']))
    return None

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

