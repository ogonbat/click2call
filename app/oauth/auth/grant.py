
"""Grant Module Handler."""

import tornado.web
from core.exceptions import ObjectDoesNotExist
from core.http.handler import BaseOAuthHandler
from app.models import Client, Grant

__author__ = 'cingusoft'



class GrantHandler(BaseOAuthHandler):
    """GET and POST are permitted.
    This handler grant the Client Application.
    In all the methods is checked the redirect_uri and the client_id sended.
    In Error case the Handler return 403 error with a String body description.
    The redirection process in with 303 to avoid the redirect problem after a POST."""
    @tornado.web.authenticated
    def get(self):
        """This is the form where the user accept or denied the access to the Application Client.
        In this test the form is not returned."""
        client_id = self.get_argument("client_id")
        response_type = self.get_argument("response_type")
        redirect_uri = self.get_argument("redirect_uri")
        scope = self.get_argument("scope")
        try:
            #check if the client exist
            client = Client()
            exist = client.get(client_id=client_id)
            if exist['redirect_uri'] != redirect_uri:
                #have an error, return a 403
                raise tornado.web.HTTPError(403,"redirect uri problem")
        except ObjectDoesNotExist, e:
            raise tornado.web.HTTPError(403,"the client id not correspond to any Client")
        try:
            grant = Grant()
            grant.is_already_authorized(client_id,self.get_current_user())
            grant.update(client_id,self.get_current_user())

            #redirect to the redirect_uri field
            if response_type == "code":
                #redirect to the redirect_url and send the code
                #the user-agent will be contact /oauth/token to take the token and the refresh token
                self.redirect((redirect_uri+"?code=%s")%(grant.code))
            else:
                self.redirect((redirect_uri+"#access_token=%s&token_type=Bearer&expires_in=%s")%(grant.token,3600))
        except ObjectDoesNotExist, e:
            message = {
                'message': 'grant'
            }
            self.write_result(message)

    @tornado.web.authenticated
    def post(self):
        """POST action to authorize the Client Application.
        To authorize will be send a POST with 'grant' parameter set to true, to deny 'parameter' set to false."""
        grant = self.get_argument("grant")
        client_id = self.get_argument("client_id")
        response_type = self.get_argument("response_type")
        redirect_uri = self.get_argument("redirect_uri")
        scope = self.get_argument("scope")
        # the client send correct paramenters, we need to check if the client id exist and we
        # create the relation between the user-agent and the client
        if grant == "true":
            try:
                #check if the client exist
                client = Client()
                exist = client.get(client_id=client_id)
                if exist['redirect_uri'] != redirect_uri:
                    #have an error, return a 403
                    raise tornado.web.HTTPError(403,"redirect uri problem")
            except ObjectDoesNotExist, e:
                raise tornado.web.HTTPError(403,"the client id not correspond to any Client")

            grant = Grant()
            try:
                #we accept the grant for the user
                grant.is_already_authorized(client_id,self.get_current_user())
                grant.update(client_id,self.get_current_user())
            except ObjectDoesNotExist, e:
                grant.add(client_id,self.get_current_user())
                #redirect to the redirect_uri field
            if response_type == "code":
                #redirect to the redirect_url and send the code
                #the user-agent will be contact /oauth/token to take the token and the refresh token
                self.redirect((redirect_uri+"?code=%s")%(grant.code),status=303)
            else:
                self.redirect((redirect_uri+"#access_token=%s&token_type=Bearer&expires_in=%s")%(grant.token,3600),status=303)
        else:
            #this is the case the user don't grant the application
            #we redirect with an error code
            self.redirect((redirect_uri+"?code=%s")%("access_denied"),statuc=303)

