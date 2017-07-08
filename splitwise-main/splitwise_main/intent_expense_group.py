from expense_manager import SplitwiseAccountmanager
from util import *


def try_ex(func):
    try:
        return func()
    except KeyError:
        return None


def ask_to_add_friend(friend):
    return "Friend {} does exist in your list, please add friend".format(friend)


def ask_to_create_group(group_name):
    return "Group {} does not exist, please create expense group".format(group_name)


def get_group_id(smgr, group_name):
    groups = smgr.get_groups()
    for group in groups:
        if group.getName() == group_name:
            return group.getId()


def get_friend_id(smgr, friend_name):
    friends = smgr.get_friends()
    for friend in friends:
        print friend.getId(), friend.getFirstName(), friend.getLastName(), friend.getEmail()
        if friend_name == friend.getFirstName():
            return friend.getId()


def add_user_request(intent):
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    first_name = try_ex(lambda: intent['currentIntent']['slots']['FirstName'])
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    if first_name and group_name:
        friend_id = get_friend_id(smgr, first_name)
        logger.info('Friend Id {}'.format(friend_id))
        if friend_id is None:
            return ask_to_add_friend(first_name)
        group_id = get_group_id(smgr, group_name)
        logger.info('Group Id {}'.format(group_id))
        if group_id is None:
            return ask_to_create_group(group_name)
        smgr.add_user_to_group(friend_id, group_id)
        return "Added {} to group {}".format(first_name, group_name)


def add_friend_request(intent):
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    first_name = try_ex(lambda: intent['currentIntent']['slots']['FirstName'])
    last_name = try_ex(lambda: intent['currentIntent']['slots']['LastName'])
    email = try_ex(lambda: intent['currentIntent']['slots']['Email'])
    if first_name and email:
        friend = dict(user_first_name=first_name, user_email=email)
        if last_name is not None:
            friend.update(dict(user_last_name=last_name))
        smgr.add_friend(friend)
        return "Added friend {} {}".format(first_name, last_name)


def create_group_request(intent):
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    if group_name is not None:
        smgr = SplitwiseAccountmanager(userId=intent['userId'])
        smgr.create_group(group_name)
        return "created group name : {}".format(group_name)
    return "Group {} can not be created".format(group_name)


def list_groups_request(intent):
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    groups = smgr.get_groups()
    group_name = ""
    for group in groups:
        group_name = group_name + group.getName() + ', '+' \n '

    return "Expense Group Name are : {}".format(group_name)


def get_users_in_group(intent):
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    groups = smgr.get_groups()
    user = ''
    group_exist = False
    for group in groups:
        if group.getName() == group_name:
            group_exist = True
            members = group.getMembers()
            for m in members:
                user = user + m.getFirstName()
                if m.getLastName() is not None: user = user + ' ' + m.getLastName()
                user = user + ', \n'

    if user and group_exist:
        return 'Friends in this group are : \n{}'.format(user)
    elif not group_exist:
        return 'No group exist with name {}, Please create group'.format(group_name)
    else:
        return 'There are no friends added to this group, please add friends to this group'


def intent_create_group(intent):
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

    fulfilment_result = create_group_request(intent)
    logger.info("Create group fulfill result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


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

    fulfilment_result = add_user_request(intent)
    logger.info("Add user fulfill result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def intent_list_groups(intent):
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

    fulfilment_result = list_groups_request(intent)
    logger.info("Add user fulfill result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def intent_get_users_in_group(intent):
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

    fulfilment_result = get_users_in_group(intent)
    logger.info("Add user fulfill result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def intent_add_friend(intent):
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

    fulfilment_result = add_friend_request(intent)
    logger.info("Add user fulfill result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def process_user_intent(intent):
    return intent_add_user_to_group(intent=intent)


def process_group_intent(intent):
    return intent_create_group(intent=intent)


def process_list_groups(intent):
    return intent_list_groups(intent=intent)


def process_get_users_in_group(intent):
    return intent_get_users_in_group(intent)


def process_add_friend(intent):
    return intent_add_friend(intent)
