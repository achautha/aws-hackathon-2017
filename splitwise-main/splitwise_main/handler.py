from splitwise_main.intent_pending_expense import process_intent as pending_ex
from splitwise_main.intent_greet import process_intent as greet
from splitwise_main.intent_expense_group import process_group_intent as expense_group
from splitwise_main.intent_expense_group import process_user_intent as add_user_to_group
from splitwise_main.intent_expense_group import process_list_groups as list_groups
from splitwise_main.intent_expense_group import process_get_users_in_group as get_user_in_group
from splitwise_main.intent_expense_group import process_add_friend as add_friend
from splitwise_main.intent_expense_group import process_create_expense as create_ex

import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

intent_map ={
    'PendingExpenses': pending_ex,
    'createExpense': create_ex,
    'createExpenseGroup': expense_group,
    'addUserToGroup': add_user_to_group,
    'showGroups': list_groups,
    'showFriendsInGroup': get_user_in_group,
    'addFriend': add_friend,
    'SplitSmartHelp': greet,
}


def lambda_handler(event, context):
    logger.info('Start processing event=%s' %str(event))
    intent_name = event['currentIntent']['name']
    logger.info('Current user={} participating in intent={}'.format(event['userId'], intent_name))

    # execute function based on intent name
    resp = intent_map[intent_name](event)
    logger.info('Returning response : %s' %resp)
    return resp
