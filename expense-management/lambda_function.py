import logging
#logger = logging.getLogger(__name__)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler('hello.log')
#logger.addHandler(handler)

from splitwise import Splitwise

Splitwise.setDebug(True)


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


def delegate(session_attributes, slots):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
    return response


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def get_accesstoken():
    CONSUMER_KEY = 'fACzGnELB2PJ9yj00KFhamAEXARtq4HNXKkc2649'
    CONSUMER_SECRET = '4JhR47gtvqfB5bKTNPvdtK2yKYeRCDp2JbRyFlnR'

    sobj = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)

    sobj.setAccessToken({'oauth_token_secret': '9uXKc94Om04RPQMlm1Kwh8MHOajHER2SFSwAfMSU',
                         'oauth_token': 'Sx4QMQikmdWAzc55Aem39KyhrjuQXJcph0u9dInY'})

    return sobj


def create_group(name):
    sboj = get_accesstoken()
    sboj.createGroup(name)
    # returning success
    return "created group name : {}".format(name)


def get_group():
    sboj = get_accesstoken()
    groups = sboj.getGroups()
    for g in groups:
        logger.info("Group Name {}, Group Id {}".format(g.id, g.getName()))
        logger.info(g.getName())


def add_user_to_group(first_name, last_name, email, group_id, group_name):
    sboj = get_accesstoken()
    response = sboj.addUserToGroup(first_name, last_name, email, group_id)
    logger.info(response)
    return "Added {} {} to group {}".format(first_name, last_name, group_name)


def get_group_id(group_name):
    sboj = get_accesstoken()
    groups = sboj.getGroups()
    for g in groups:
        logger.info("Group Id {}, Group Name {}".format(g.id, g.getName()))
        if g.getName() == group_name:
            return g.id


def intent_create_group(intent_request):
    logger.info("Intent Req:{}".format(intent_request))
    group_name = try_ex(lambda: intent_request['currentIntent']['slots']['GroupName'])
    logger.info("Group Name {}".format(group_name))
    source = intent_request['invocationSource']
    logger.info("Source {}".format(source))
    if source == 'FulfillmentCodeHook':
        if group_name is not None:
            # Fulfill request
            fulfilment_result = create_group(group_name)
            return close(intent_request['sessionAttributes'], 'Fulfilled',
                         {'contentType': 'PlainText',
                          'content': fulfilment_result})


def intent_add_user(intent_request):
    logger.info("Intent Req:{}".format(intent_request))
    first_name = try_ex(lambda: intent_request['currentIntent']['slots']['FirstName'])
    last_name = try_ex(lambda: intent_request['currentIntent']['slots']['LastName'])
    email = try_ex(lambda: intent_request['currentIntent']['slots']['Email'])
    group_name = try_ex(lambda: intent_request['currentIntent']['slots']['GroupName'])
    logger.info('First Name {} Last Name {} Email {}'.format(first_name, last_name, email))
    source = intent_request['invocationSource']
    logger.info("Source {}".format(source))

    if source == 'FulfillmentCodeHook':
        if first_name and last_name and email and group_name:
            group_id = get_group_id(group_name)
            # Fulfill request
            fulfilment_result = add_user_to_group(first_name, last_name, email, group_id, group_name)
            return close(intent_request['sessionAttributes'], 'Fulfilled',
                         {'contentType': 'PlainText',
                          'content': fulfilment_result})


def process_intent(intent_request):
    logger.info(
        'User={}, Intent={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    if intent_request['currentIntent']['name'] == 'createExpenseGroup':
        return intent_create_group(intent_request)
    elif intent_request['currentIntent']['name'] == 'addUserToGroup':
        return intent_add_user(intent_request)


def lambda_handler(event, context):
    logger.info("Start processing BOT request")
    return process_intent(event)

"""if __name__ == '__main__':
    event = {
       "currentIntent":{
          "slots":{
             "GroupName":"Japan",
             "Email":"rangaresandeep@gmail.com",
             "FirstName":"Sandeep",
             "LastName":"Rangare"
          },
          "name":"addUserToGroup",
          "confirmationStatus":"None"
       },
       "bot":{
          "alias":"None",
          "version":"$LATEST",
          "name":"expenseManagement"
       },
       "userId":"v2wuy8i0p8yom7oum7kvrivq2ph0m7i6",
       "inputTranscript":"Japan",
       "invocationSource":"FulfillmentCodeHook",
       "outputDialogMode":"Text",
       "messageVersion":"1.0",
       "sessionAttributes":"None"
    }
    lambda_handler(event, "")"""