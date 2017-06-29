from splitwise_main.expense_manager import SplitwiseAccountmanager
from splitwise_main.util import *

def try_ex(func):
    try:
        return func()
    except KeyError:
        return None


def process_add_user_request(intent):
    first_name = try_ex(lambda: intent['currentIntent']['slots']['FirstName'])
    last_name = try_ex(lambda: intent['currentIntent']['slots']['LastName'])
    email = try_ex(lambda: intent['currentIntent']['slots']['Email'])
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    if first_name and last_name and email and group_name:
        smgr = SplitwiseAccountmanager(userId=intent['userId'])
        group_id = smgr.get_group_id(group_name)
        smgr.add_user_to_group(first_name, last_name, email, group_id)
        return "Added {} {} to group {}".format(first_name, last_name, group_name)


def process_create_group(intent):
    logger.info("Intent Req:{}".format(intent))
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    logger.info("Group Name {}".format(group_name))
    source = intent['invocationSource']
    logger.info("Source {}".format(source))
    if group_name is not None:
        smgr = SplitwiseAccountmanager(userId=intent['userId'])
        smgr.create_group(group_name)
        return "created group name : {}".format(group_name)


def intent_add_user_to_group(intent):
    # Check if logged In
    if intent['invocationSource'] == 'DialogCodeHook':
        slots = get_slots(intent)
        if intent['currentIntent']['confirmationStatus'] == 'Denied':
            return close(intent['sessionAttributes'], 'Failed',
                         {'contentType': 'PlainText',
                          'content': 'Sorry unable to proceed with your request'})

        token, attem = is_logged_in(intent['userId'], intent)
        if not token:
            if attem > 3:
                intent['sessionAttributes']['login_attempts'] = 0
                logger.info('Login attempts exceeded. Fail request')
                return close(intent['sessionAttributes'], 'Failed',
                             {'contentType': 'PlainText',
                              'content': 'Number of login attempts exceeded. Please check your splitwise credentials'})

            logger.info('Token is not present. Now asking for login confirmation with %s' % intent)
            return confirm_intent(intent['sessionAttributes'],
                                  intent['currentIntent']['name'],
                                  get_slots(intent),
                                  initiate_oauth(intent['userId']))
        else:
            # Do other validation yourself or delegate other validations to BOT
            return delegate(intent['sessionAttributes'], get_slots(intent))

    fulfilment_result = process_add_user_request(intent)
    logger.info("Add user fullfil result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})

def intent_create_group(intent):
    # Check if logged In
    logger.info('Intent {}'.format(intent))
    if intent['invocationSource'] == 'DialogCodeHook':
        slots = get_slots(intent)
        if intent['currentIntent']['confirmationStatus'] == 'Denied':
            return close(intent['sessionAttributes'], 'Failed',
                         {'contentType': 'PlainText',
                          'content': 'Sorry unable to proceed with your request'})

        token, attem = is_logged_in(intent['userId'], intent)
        if not token:
            if attem > 3:
                intent['sessionAttributes']['login_attempts'] = 0
                logger.info('Login attempts exceeded. Fail request')
                return close(intent['sessionAttributes'], 'Failed',
                             {'contentType': 'PlainText',
                              'content': 'Number of login attempts exceeded. Please check your splitwise credentials'})

            logger.info('Token is not present. Now asking for login confirmation with %s' % intent)
            return confirm_intent(intent['sessionAttributes'],
                                  intent['currentIntent']['name'],
                                  get_slots(intent),
                                  initiate_oauth(intent['userId']))
        else:
            # Do other validation yourself or delegate other validations to BOT
            return delegate(intent['sessionAttributes'], get_slots(intent))

    fulfilment_result = process_create_group(intent)
    logger.info("Create group fullfil result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def process_user_intent(intent):
    return intent_add_user_to_group(intent=intent)


def process_group_intent(intent):
    return intent_create_group(intent=intent)
