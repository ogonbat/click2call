
"""Module for the test redirect page"""

from core.http.handler import BaseOAuthHandler

__author__ = 'cingusoft'


class TestHandler(BaseOAuthHandler):
    """This handler have a get method that return the code or the token after the redirect form grant or token page."""
    def get(self):
        """GET method that return the Code or the Token send by the Grant or the Token page.
        The returned value is a json string."""
        code = self.get_argument("code",None)

        access_token = self.get_argument("access_token",None)
        token_expire = self.get_argument("expires_in",None)
        if code is not None:
            message = {
                'code': code
            }
            self.write_result(message)
        else:
            message = {
                'token': access_token,
                'expire': token_expire
            }
            self.write_result(message)
