import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
from splitwise_oauth.expense_manager import SplitwiseOAuthManager

html_response = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>Authorization Status</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<div class="jumbotron text-center">
  <h2>Your Splitwise authorization is successful !</h2>
  <p>Go back to your bot and enjoy</p>
</div>

</body>
</html>"""


class SplitwiseCallbackHandler(object):
    """
    This is an entrypoint for you microservice
    """

    def __init__(self, event, context):
        self.event = event
        self.context = context

    def process_event(self):
        """
        Retrieve auth_token and verifier from request and call AuthManager
        :return:
        """
        query_params = self.event['queryStringParameters']
        sauth = SplitwiseOAuthManager(auth_token=query_params['oauth_token'])
        access_token = sauth.request_access_token(query_params['oauth_verifier'])
        logger.info("Access token obtained %s" % repr(access_token))
        response = {
            'Status': 'SUCCESS',
            'Message': 'Splitwise Authentication is successful. Go back to your bot and enjoy Splitwise !',
            'access_token': access_token
        }
        return response

    def process_event_html(self):
        """
        Retrieve auth_token and verifier from request and call AuthManager
        :return:
        """
        query_params = self.event['queryStringParameters']
        sauth = SplitwiseOAuthManager(auth_token=query_params['oauth_token'])
        access_token = sauth.request_access_token(query_params['oauth_verifier'])
        logger.info("Access token obtained %s" % repr(access_token))
        # response = html_response.replace("##ACCESS##", str(access_token))
        response = html_response
        return response
