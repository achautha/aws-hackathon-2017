from splitwise_main.util import *
from splitwise_main.expense_manager import SplitwiseAccountmanager

def calc_pending_expenses_for_friend(userId, friend):
    smgr = SplitwiseAccountmanager(userId=userId)
    friends = smgr.get_friends()
    if not friends:
        return "Sorry ! You don't seem have any friends in this account ! Why don't you invite them."
    frnd = None
    for f in friends:
        if f.first_name.upper() == friend.upper():
	    
            frnd =  f
            break

    if not frnd:
        return "Sorry ! {} is not in your friends list".format(friend)

    to_friend = []
    from_friend = []
    for balance in frnd.balances:
        if float(balance.amount) < 0:
            to_friend.append("{} {}".format(balance.currency_code ,abs(float(balance.amount))))
        elif float(balance.amount) > 0:
            from_friend.append("{} {}".format(balance.currency_code ,abs(float(balance.amount))))

    frnd_exp = None
    if not to_friend:
        frnd_exp = "You owe {} nothing. ".format(friend)
    else:
        frnd_exp = "You owe {} {}. ".format(friend, ",".join(to_friend))

    your_exp= None
    if not from_friend:
        your_exp = "{} owes you nothing. ".format(friend)
    else:
        your_exp = "{} owes you {}. ".format(friend, ",".join(from_friend))

    return "{}\n\n{}".format(frnd_exp, your_exp)
    	
def calculate_pending_expenses_for_group(userId, group):
    smgr = SplitwiseAccountmanager(userId=userId)
    group_exp = []
    mygroup = smgr.get_group(group)
    if not mygroup:
	return "Sorry ! group {} does not exist in your account".format(group)

    for debt in mygroup.simplified_debts:
        group_exp.append("{} owes {} {} {}. ".format(smgr.get_user(debt.fromUser).first_name, smgr.get_user(debt.toUser).first_name,
                                        debt.currency_code, debt.amount))
    if not group_exp:
        return "Sorry ! No expenses created in this group"

    return "Here is your expense report for group {}:\n\n{}".format(group, ",\n".join(group_exp))

def fulfil_request(userId, slots):
    if slots.get('friendOrGroup', None):
        if slots['friendOrGroup'].lower() == 'friend':
	   logger.info("calculating for friend %s" %slots['entityName'])
	   return calc_pending_expenses_for_friend(userId, slots['entityName'])
        if slots['friendOrGroup'].lower() == 'group':
	   logger.info("calculating for group %s" %slots['entityName'])
	   return calculate_pending_expenses_for_group(userId, slots['entityName'])
    else:
	return calculate_pending_expenses(userId)

def calculate_pending_expenses(userId):
    smgr = SplitwiseAccountmanager(userId=userId)
    friends = smgr.get_friends()
    if not friends:
        return "Sorry! You Don't seem to  have any friends in your account. Invite some friends and have fun!"

    you_owe = []
    friends_owe = []
    for f in friends:
        for balance in f.balances:
            if float(balance.amount) < 0:
                you_owe.append("{} {} {}".format(f.first_name, balance.currency_code ,abs(float(balance.amount))))
	    elif float(balance.amount) > 0:
	        friends_owe.append("{} {} {}".format(f.first_name, balance.currency_code ,abs(float(balance.amount))))	
 
    frnd_exp = None
    if not you_owe:
        frnd_exp = "You owe nothing."
    else:
        frnd_exp = "You owe: \n{}".format(",\n".join(you_owe))

    your_exp= None
    if not friends_owe:
        your_exp = "Friends owe you nothing."
    else:
        your_exp = "Friends owe you:\n{} ".format( ",\n".join(friends_owe))

    return "Here is your pending expense report: \n{}\n   \n{}\n".format(frnd_exp, your_exp)

def intent_pending_expenses(intent):
    # Check if logged In
    if intent['invocationSource'] == 'DialogCodeHook':
        slots = get_slots(intent)
        if intent['currentIntent']['confirmationStatus'] == 'Denied':
	    return close(intent['sessionAttributes'], 'Failed',
		         {'contentType': 'PlainText',
                  	  'content': 'Sorry ! We can not process your request without authorization.'})   
		 
	token, attem = is_logged_in(intent['userId'], intent)
	if not token:
	    if attem > 3:
		intent['sessionAttributes']['login_attempts'] = 0
            	logger.info('Login attempts exceeded. Fail request')
	    	return close(intent['sessionAttributes'], 'Failed',
		         {'contentType': 'PlainText',
                  	  'content': 'Oops ! Number of login attempts exceeded. Please check your SplitWise credentials'})   
			
            logger.info('Token is not present. Now asking for login confirmation with %s' % intent)
            return confirm_intent(intent['sessionAttributes'],
                              intent['currentIntent']['name'],
                              get_slots(intent),
                              initiate_oauth(intent['userId']))
        else:
            # Do other validation yourself or delegate other validations to BOT
            return delegate(intent['sessionAttributes'], get_slots(intent) )

    # Fulfill request
    fulfilment_result = fulfil_request(intent['userId'], get_slots(intent))
    return close(intent['sessionAttributes'], 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': fulfilment_result})


def process_intent(intent):
    return intent_pending_expenses(intent=intent)
