from splitwise_main.util import *
from splitwise_main.expense_manager import SplitwiseAccountmanager

help_message = "Hello ! I am SplitSmartBot.\nI am here to help you manage and split expenses with friends.\n You can ask me any of the following.\n1. create expense group.\n2. Add friend to expense group.\n3. Show groups.\n4. Show friends. \n5. Get all pending expenses. \n6. Show expenses with friend Bob. \n7. Show expenses for group VegasTrip. \n\nWhat do you want to do today ? "

def intent_help(intent):

    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': help_message})


def process_intent(intent):
    return intent_help(intent=intent)
