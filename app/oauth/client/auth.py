
"""Module for the Authorization Client Handler."""

import urllib
from core.exceptions import ObjectDoesNotExist
from core.http.handler import BaseOAuthHandler
from app.models import  Client
import tornado.web

__author__ = 'cingusoft'



class AuthHandler(BaseOAuthHandler):
    """This is the first handler called during the Authentication/Authorization process."""
    def get(self):
        """This Method check if the Application Client exist, if yes redirect to the login page.
        In Case something goes wrong the Handler return a 400 status code if the Client Id does not exist and 400 if the parameters send are not correct."""
        client_id = self.get_argument("client_id")
        response_type = self.get_argument("response_type")
        redirect_uri = self.get_argument("redirect_uri")
        scope = self.get_argument("scope")

        # before check if the client pass client_id, redirect_url and response_type
        # we accept only token "Implicit Grant Flow"
        # if all is ok we need to check if the client_id and the redirect_uri are correct
        # if not we return a 403 to the client
        if response_type in ("token","code"):
            try:
                client_check = Client()
                exist = client_check.get(client_id=client_id)
                #check the redirect_uri parameter
                if exist['redirect_uri'] != redirect_uri:
                    #have an error, return a 403
                    raise tornado.web.HTTPError(403,"redirect uri problem")
                # redirect to login page
                self.redirect(("/auth/login?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s")%(client_id,
                                                                                                      response_type,
                                                                                                      urllib.quote_plus(redirect_uri),
                                                                                                      scope))
            except ObjectDoesNotExist, e:
                raise tornado.web.HTTPError(403)
        else:
            raise tornado.web.HTTPError(400,"The accepted values for response type are token or code")

