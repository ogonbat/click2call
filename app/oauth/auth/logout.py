
"""Module with the Logout Handler"""

from core.http.handler import BaseOAuthHandler
import tornado.web
__author__ = 'cingusoft'

class LogOutHandler(BaseOAuthHandler):
    """Logout Handler"""
    @tornado.web.authenticated
    def get(self):
        """The Logout process in handled with a GET Method.
        The logout delete the secret cookie.
        If all work well the logout return a 200 status code and a message in JSON format."""
        self.clear_all_cookies()
        message = {
            'message':"logout complete"
        }
        self.write_result(message)