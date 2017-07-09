from splitwise_main.util import *
from splitwise_main.expense_manager import SplitwiseAccountmanager

help_message = "Hello ! I am SplitSmartBot.\nI am here to help you manage and split expenses with friends.\n You can ask me any of the following."

operations = [ 
 "Create a new expense group.", 
 "Add <friend> to <GroupName>.", 
 "Create a new expenses in the <GroupName>",
 "Show all groups.",
 "Show friends in a <GroupName>.",
 "Get all pending expenses.", 
 "Show expenses with friend <NameOfFriend>.",
 "Show expenses for group <GroupName>."
]

greetings="What do you want to do today ?"

def intent_help(intent):
    newoper = []
    for i, ele in enumerate(operations):
	newoper.append("{}. {}".format(i+1, ele))

    oper_str = "\n".join(newoper)
    final_message = "{}\n{}\n\n\n{}".format(help_message, oper_str, greetings)	  
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': final_message})


def process_intent(intent):
    return intent_help(intent=intent)
