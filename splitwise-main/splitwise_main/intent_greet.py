from splitwise_main.util import *
from splitwise_main.expense_manager import SplitwiseAccountmanager

help_message = "Hello ! I am SplitSmartBot.\nI am here to help you manage and split expenses with friends.\nYou can ask me any of the following."

operations = [ 
 "Show all friends",
 "I want to Invite friend [FirstName]",
 "Show all my groups",
 "I want to create a new group [GroupName]", 
 "Show friends in [GroupName]",
 "Can you add [FirstName] to [GroupName].", 
 "I paid [amount] for [purpose]",
 "Show my balance", 
 "Show balance with friend [FirstName].",
 "Get balance for group [GroupName]."
]

greetings="What do you want to do today ?"

def intent_help(intent):
    newoper = []
    for i, ele in enumerate(operations):
	newoper.append("{}. {}".format(i+1, ele))

    oper_str = "\n\n".join(newoper)
    final_message = "{}\n{}\n\n\n{}".format(help_message, oper_str, greetings)	  
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': final_message})


def process_intent(intent):
    return intent_help(intent=intent)
