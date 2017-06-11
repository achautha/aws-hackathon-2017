from splitwise_main.intent_pending_expense import process_intent as pending_ex
import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


intent_map ={
    'PendingExpenses' : pending_ex,
}


def lambda_handler(event, context):
    logger.info('Start processing event=%s' %str(event))
    intent_name = event['currentIntent']['name']
    logger.info('Current user={} participating in intent={}'.format(event['userId'], intent_name))

    # execute function based on intent name
    resp = intent_map[intent_name](event)
    logger.info('Returning response : %s' %resp)
    return resp


