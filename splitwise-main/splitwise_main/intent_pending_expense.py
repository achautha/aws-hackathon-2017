from splitwise_main.expense_manager import SplitwiseAccountmanager
from splitwise_main.util import *


def calculate_pending_expenses(userId):
    smgr = SplitwiseAccountmanager(userId=userId)
    friends = smgr.get_friends()
    if not friends:
        return "You Don't have any friends. Create an expense group and invite friends."

    pending_exp = []
    for f in friends:
        for balance in f.balances:
            if float(balance.amount) < 0:
                pending_exp.append("{}={}".format(f.first_name, abs(float(balance.amount))))

    if not pending_exp:
        return "You don't owe anything"

    result = "You owe " + ", ".join(pending_exp)
    return result


def intent_pending_expenses(intent):
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

    # Fulfill request
    fulfilment_result = calculate_pending_expenses(intent['userId'])
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def process_intent(intent):
    return intent_pending_expenses(intent=intent)
