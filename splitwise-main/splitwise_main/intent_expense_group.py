from expense_manager import SplitwiseAccountmanager
from util import *


def try_ex(func):
    try:
        return func()
    except KeyError:
        return None


def ask_to_add_friend(friend):
    return "Oops ! Friend {} does exist in your list, please add friend".format(friend)


def ask_to_create_group(group_name):
    return "Oops ! Group {} does not exist, please create expense group".format(group_name)


def get_group_id(smgr, group_name):
    groups = smgr.get_groups()
    for group in groups:
        if group.getName().lower() == group_name.lower():
            return group.getId()


def get_friend_id(smgr, friend_name):
    friends = smgr.get_friends()
    for friend in friends:
        print friend.getId(), friend.getFirstName(), friend.getLastName(), friend.getEmail()
        if friend_name.lower() == friend.getFirstName().lower():
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
        return "Successfully Added {} to group {}".format(first_name, group_name)


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
        return "Successfully invited friend {} {}".format(first_name, last_name)


def create_group_request(intent):
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    if group_name is not None:
        smgr = SplitwiseAccountmanager(userId=intent['userId'])
        smgr.create_group(group_name)
        return "Successfully created group name : {} ! Now you can invite friends and add them here".format(group_name)
    return "Sorry! Group {} can not be created".format(group_name)


def list_groups_request(intent):
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    groups = smgr.get_groups()
    group_name = ""
    for group in groups:
        group_name = group_name + group.getName() + ', '+' \n '

    return "You have following groups in your account:\n {}".format(group_name)


def get_users_in_group(intent):
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    groups = smgr.get_groups()
    user = ''
    group_exist = False
    for group in groups:
        if group.getName().lower() == group_name.lower():
            group_exist = True
            members = group.getMembers()
            for m in members:
                user = user + m.getFirstName()
                if m.getLastName() is not None: user = user + ' ' + m.getLastName()
                user = user + '\n'

    if user and group_exist:
        return 'Friends in this group are : \n{}'.format(user)
    elif not group_exist:
        return 'Sorry ! No group exist with name {}, Please create group'.format(group_name)
    else:
        return 'Sorry ! There are no friends added to this group, please add friends to this group'


def create_expense_group(intent):
    logger.info('Create Expense :%s' % intent)
    group_name = try_ex(lambda: intent['currentIntent']['slots']['GroupName'])
    expense_dec = try_ex(lambda: intent['currentIntent']['slots']['ExpenseDescription'])
    expense_cost = try_ex(lambda: intent['currentIntent']['slots']['ExpenseCost'])
    if group_name and expense_cost and expense_cost:
        cost = float(expense_cost)
        smgr = SplitwiseAccountmanager(userId=intent['userId'])
        groups = smgr.get_groups()
        expense = smgr.get_expense_obj()
        current_user = smgr.get_current_user()
        my_id = current_user.getId()
        expense.setCost(cost)
        expense.setDescription(expense_dec)
        expense.setPayment(False)

        group_exist = False

        for group in groups:
            if group.getName().lower() == group_name.lower():
                group_exist = True
                group_id = group.getId()
                expense.setGroupId(group_id)
                members = group.getMembers()
                total_members = float(len(members))
                owe_share = float("{0:.2f}".format(cost/total_members))
                users = []
                # There is always atleast one group member
                for member in members:
                    user = smgr.get_expense_user()
                    user.setId(member.getId())
                    if my_id == member.getId():
                        my_owe_share = cost - owe_share * (total_members - 1)
                        user.setOwedShare(str(my_owe_share))
                        user.setPaidShare(str(cost))
                    else:
                        user.setOwedShare(str(owe_share))
                        user.setPaidShare(str(0))

                    users.append(user)

                expense.setUsers(users)

        if group_exist:
            expense = smgr.create_expense(expense)
            # parse the expense object to see if any error exist
            return 'Added your expense amount {} in group {}.'.format(expense_cost, group_name)
        else:
            return 'Oops! Group {} does not exist in your account. Why dont you create a anew group'.format(group_name)


def get_friends(intent):
    smgr = SplitwiseAccountmanager(userId=intent['userId'])
    friends = smgr.get_friends()
    friend_list = ''
    for friend in friends:
        friend_list = friend_list + friend.getFirstName()
        if friend.getLastName() is not None:
            friend_list = friend_list + ' ' + friend.getLastName()
        friend_list = friend_list + '\n'

    if friend_list:
        return 'Your friends \n{}'.format(friend_list)
    else:
        return 'Looks like you have not invited any friends yet, please invite friend'

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

def intent_create_expense(intent):
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

    fulfilment_result = create_expense_group(intent)
    logger.info("Add user fulfill result {}".format(fulfilment_result))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def intent_get_friends(intent):
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

    fulfilment_result = get_friends(intent)
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

def process_create_expense(intent):
    return intent_create_expense(intent)

def process_get_friends(intent):
    return intent_get_friends(intent)
