import sys, json
from splitwise import Splitwise
from urlparse import urlparse
import boto3
from boto3.dynamodb.conditions import Key, Attr
import tinyurl
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SplitwiseAccountmanager(object):

    def __init__(self, userId):
        self.sauth = SplitwiseOAuthManager(userId)
        self.userId = userId

    def get_friends(self):
        access_token = self.sauth.get_access_token()
        self.sauth.splitwise_handle.setAccessToken(access_token)
        return self.sauth.splitwise_handle.getFriends()

    def get_current_user(self):
        access_token = self.sauth.get_access_token()
        self.sauth.splitwise_handle.setAccessToken(access_token)
        return self.sauth.splitwise_handle.getCurrentUser()


class SplitwiseOAuthManager(object):
    CONSUMER_KEY = 'fACzGnELB2PJ9yj00KFhamAEXARtq4HNXKkc2649'
    CONSUMER_SECRET = '4JhR47gtvqfB5bKTNPvdtK2yKYeRCDp2JbRyFlnR'

    def __init__(self, userId=None, auth_token=None):
        self.userId = userId
        self.splitwise_handle = Splitwise(SplitwiseOAuthManager.CONSUMER_KEY, SplitwiseOAuthManager.CONSUMER_SECRET)
        self.auth_token = auth_token

    def request_authorized_url(self):
        self.url, self._secret = self.splitwise_handle.getAuthorizeURL()
        logger.info("Received url=%s and secrect=%s" %(self.url, self._secret))
        query_param = urlparse(self.url).query
        if 'oauth_token' in query_param:
            self.auth_token=query_param.split('=')[1]
            session = UserSession(userId=self.userId,
                                  oauth_token=self.auth_token,
                                  secret=self._secret)
            UserSessionManager().persist_user_session(session)

        return tinyurl.create_one(self.url)

    def request_access_token(self, auth_verifier=None):
        mgr = UserSessionManager()
        session = mgr.get_session_from_oauth_token(self.auth_token)
        logger.info("User session %s" %repr(session))

        access_token = self.splitwise_handle.getAccessToken(session.oauth_token,
                                             session.secret,
                                             auth_verifier)
        session.access_token = access_token
        mgr.persist_user_session(session)
        return access_token

    def get_access_token(self):
        mgr = UserSessionManager()
        session = mgr.get_session_from_userid(self.userId)
        result =  session.access_token if session else None
        return result


class UserSession(object):
    def __init__(self, userId, oauth_token, secret, access_token=None, auth_verifier= None):
        self.userId = userId
        self.oauth_token = oauth_token
        self.secret = secret
        self.auth_verifier = auth_verifier
        self.access_token = access_token

    def __repr__(self):
        return "user_id={} , oauth_token={}, secret={}, auth_verifier={}, access_token={}".format(
            self.userId, self.oauth_token, self.secret, self.auth_verifier, self.access_token
        )


class UserSessionManager(object):

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('spliteasy-user-session')

    def persist_user_session(self, user_session):
        logger.info("Creating UserSession for %s" % user_session.userId)
        response = self.table.put_item(Item={
            'user_id': user_session.userId,
            'oauth_token' : user_session.oauth_token,
            'secret' : user_session.secret,
            'access_token': user_session.access_token,
            'auth_verifier': user_session.auth_verifier
        })
        logger.info("persist_user_session response %s" %repr(response))

    def get_session_from_oauth_token(self, oauth_token):
        filter_ex = Key('oauth_token').eq(oauth_token)
        response = self.table.scan(FilterExpression = filter_ex)
        item = response['Items'][0]
        logger.info('Found user session object %s' %repr(item))
        return UserSession(userId=item['user_id'],
                           oauth_token=item['oauth_token'],
                           secret=item['secret'],
                           access_token=item['access_token'])

    def get_session_from_userid(self, userId):
        response = self.table.query(
            KeyConditionExpression=Key('user_id').eq(userId)
        )
        if response['Count'] <= 0:
            return None

        item = response['Items'][0]
        logger.info('Found user session object %s' % repr(item))

        return UserSession(userId=item['user_id'],
                           oauth_token=item['oauth_token'],
                           secret=item['secret'],
                           access_token=item['access_token'])

'''
Test cases
'''
def test_initiate_oauth():
    """
    When user first  authenticates with Splitwise
    :return:
    """
    sauth = SplitwiseOAuthManager('demo-sbi-user-1')
    print sauth.request_authorized_url()


def test_on_callback_from_splitwise(auth_token, auth_verifier):
    """
    Splitwise -> API Gateway -> Lambda Function

    :param auth_token:
    :param auth_verifier:
    :return:
    """
    sauth = SplitwiseOAuthManager(auth_token=auth_token)
    access_token = sauth.request_access_token(auth_verifier)
    print access_token


def test_get_friends():
    """
    Splitwise calls
    :return:
    """
    smgr = SplitwiseAccountmanager(userId='123')
    print smgr.get_friends()

def test_get_current_user():
    smgr = SplitwiseAccountmanager(userId='123')
    print smgr.get_current_user().__dict__


if __name__ == '__main__':
    pass
    #test_initiate_oauth()
    #test_on_callback_from_splitwise('7oIMvWbqZXgwCc0zQAWToA1q7NzAntn7EUeuubaR', 'pE28vR9Pct4kR4G1jvjd')
    #get_friends({u'oauth_token_secret': u'88VUx9FMf85JaB81evq5zMqWSs5zB8wQ773B2lIh',
    #             u'oauth_token': u'3cxfHmS2Kma7wbiwTDL7ix4Th2eXFI5sykCL5qM7'})
    #test_get_current_user()

