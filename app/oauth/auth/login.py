
"""Module with Login Handler."""

import urllib
import tornado.web
from core.exceptions import ObjectDoesNotExist
from core.http.handler import BaseOAuthHandler
from app.models import User

__author__ = 'cingusoft'



class LoginHandler(BaseOAuthHandler):
    """This Hanlder start the login process.
    is supported the GET and the POST method."""
    def get(self):
        """This is the login web page.
        In this Test is not active the web user interface, in a production solution this will be the HTML page that show the
        login access.
        if the used is logged in, this page redirect automatically to the Grant Handler.
        If the user is nto logged, the page return a Statis Code 200 and a JSON string with basic informations.
        For an automatized Test process, the returned JSON string is usefoult to take all the parameter ant send a POST to login the User-Agent.
        To Log the User-Agent will be send a POST to the same URL with username and password parameters."""
        client_id = self.get_argument("client_id")
        response_type = self.get_argument("response_type")
        redirect_uri = self.get_argument("redirect_uri")
        scope = self.get_argument("scope")

        user = self.get_current_user()
        if user is not None:
            #the user is loggedin, we need to move to redirect to the grant page
            self.redirect(("/auth/grant?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s")%(client_id,
                                                                                                  response_type,
                                                                                                  urllib.quote_plus(redirect_uri),
                                                                                                  scope))
        else:
            message = {
                'client_id':client_id,
                'response_type':response_type,
                'redirect_uri':redirect_uri,
                'scope':scope,
                'message':"login"
            }
            self.write_result(message)

    def post(self):
        """This is the POST to start the login process.
        all the parameters are Mandatory
        if the login is succesfull the page redirect to the Grant page.
        Is necesarry to add username and password parameters to the POST body.
        the redirect is with a status code 303.
        if the username and the password are not correct, the page raise a 403 error."""
        client_id = self.get_argument("client_id")
        response_type = self.get_argument("response_type")
        redirect_uri = self.get_argument("redirect_uri")
        scope = self.get_argument("scope")
        username = self.get_argument("username")
        password = self.get_argument("password")

        #if one of the values is not passed we raise an 400 error with a string error
        #make the login process
        try:
            user = User()
            ret = user.authenticate(username,password)
            #the user is authenticated, send a secure_cookie and redirect to the grant page
            self.set_secure_cookie("clkcallagent",username)
            self.redirect(("/auth/grant?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s")%(
                                                                                            client_id,
                                                                                            response_type,
                                                                                            urllib.quote_plus(redirect_uri),
                                                                                            scope),
                                                                                            status=303)
        except ObjectDoesNotExist, e:
            raise tornado.web.HTTPError(403,"username and password not correspond to any user")