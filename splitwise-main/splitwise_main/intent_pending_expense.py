from splitwise_main.util import get_slots, prompt_for_login, delegate, confirm_intent, close, logger
from splitwise_main.expense_manager import SplitwiseAccountmanager

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
        val = prompt_for_login(intent)
        if val:
            logger.info("OAuth Initiation...")
            return val
        else:
            # Do other validation yourself or delegate other validations to BOT
            return delegate(intent['sessionAttributes'], get_slots(intent) )

    # Fulfill request
    fulfilment_result = calculate_pending_expenses(intent['userId'])
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def process_intent(intent):
    return intent_pending_expenses(intent=intent)
