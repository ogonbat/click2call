
"""Token Module Handler."""

import tornado
from core.exceptions import ObjectDoesNotExist
from core.http.handler import BaseOAuthHandler
from app.models import Client

__author__ = 'cingusoft'


class TokenHandler(BaseOAuthHandler):
    """This Handler is used only for the Appllication Flow.
    we use a get to check the code and return the token, and and expire."""

    @tornado.web.authenticated
    def get(self):
        """Get method.
        return the token and the refresh if all the parameters passed are correct."""
        code = self.get_argument("code")
        client_id = self.get_argument("client_id")
        client_secret= self.get_argument("client_secret")
        redirect_uri = self.get_argument("redirect_uri")
        grant_type = self.get_argument("grant_type")

        try:
            client_check = Client()
            exist = client_check.get(client_id=client_id)
            if exist['redirect_uri'] != redirect_uri:
                #have an error, return a 403
                raise tornado.web.HTTPError(403,"redirect uri problem")
            #check the redirect_uri parameter
            token_result = client_check.authenticate(client_id,client_secret,code)

            self.redirect((redirect_uri+"?access_token=%s&expires_in=%s&token_type=Bearer")%(token_result['token'],3600))
        except ObjectDoesNotExist, e:
            raise tornado.web.HTTPError(403)