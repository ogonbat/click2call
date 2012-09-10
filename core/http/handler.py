
""" Module for Generic Hanlders.
In this module have all the handlers used during the Autorizathion, Authentication and the REST Call processes."""


import json
import time
import tornado.web
import tornado.escape
from app.models import Grant
from core.exceptions import ObjectDoesNotExist
from core.utils import General

__author__ = 'cingusoft'


class BaseHandler(tornado.web.RequestHandler):
    """Base Class for all the Handlers."""
    def initialize(self):
        """Method called before the flush().
        Preconfigure the Server Header and check the Accept Header."""
        self.set_header("Server","Skype ClickToCall Server")
        general = General()
        self._rest_accepted = general.getHeadersAccepted(self.request.headers)

    def write_result(self,object,objname=None):
        """Write to the buffer the object paramenter
        with the global attribute self._rest_accept check if the Client Accept XML or JSON."""
        if self._rest_accepted == "xml":
            return self.__write_xml(object,objname)
        return self.__write_json(object)


    def __write_xml(self,object,objname=None):
        """Used during the XML String generation."""
        self.set_header("Content-Type","text/xml;application/xml")
        self._write_buffer.append(self.__getXML_dict(object,objname))

    def __write_json(self,object):
        """method used during the JSON string generation."""
        self.set_header("Content-Type","application/json")
        self._write_buffer.append(json.dumps(object,indent=4))

    def __getXML(self,object,objname=None):
        """return the XML formatted string.
        Accept List or Dictionary."""
        xmlString = ""
        if object == None:
            return ""
        if not objname:
            objname = "clicktocall"
        adapt={
            dict: self.__getXML_dict,
            list: self.__getXML_list,
            tuple: self.__getXML_list,
            }
        if adapt.has_key(object.__class__):
            return adapt[object.__class__](object, objname)
        else:
            xmlString = "<%(n)s>%(o)s</%(n)s>"%{'n':objname,'o':str(object)}
        return xmlString

    def __getXML_dict(self,indict, objname=None):
        """method used to parse the dictionary for the XML String Generation."""
        h = "<%s>"%objname
        for k, v in indict.items():
            h += self.__getXML(v, k)
        h += "</%s>"%objname
        return h

    def __getXML_list(self,inlist, objname=None):
        """method used to parse the list for the XML String Generation."""
        h = ""
        for i in inlist:
            h += self.__getXML(i, objname)
        return h

class BaseOAuthHandler(BaseHandler):
    """Handler used during the Authentication/Authorization Process."""
    def get_current_user(self):
        """Check if the User-Agent is logged and decript the secret cookie.
        The value returned is the client username, the cookie is crypted with an hashtag."""
        user_json = self.get_secure_cookie("clkcallagent")
        if user_json:
            return user_json
        else:
            return None

class RestHandler(BaseHandler):
    """Hanlder used during the Rest Calls."""
    _grant_token = None

    def initialize(self):
        """Method that override the initialize BaseHandler method."""
        self.set_header("Server","Skype ClickToCall Server")
        general = General()
        self._rest_accepted = general.getHeadersAccepted(self.request.headers)


    def prepare(self):
        """Override the prepare RequestHandler method.
        Check if the Client send correct token and if the token need refresh.
        Support the Authorization Header check or the GET access_token.
        if the Client don't send a Token or the token is incorrect this method flush a 403 HTTP Error."""

        token = None
        #frst we check if the authentication token is send by the Autorization header
        if 'Authorization' in self.request.headers:
            auth_header = self.request.headers['Authorization']
            #the authentication token is send like Bearer <token>
            #we need to split the string and obtain the token
            header_parts = auth_header.split(' ')
            token = header_parts[1]
        elif self.get_argument('access_token'):
            token = self.get_argument('access_token')
        else:
            raise tornado.web.HTTPError(403,"not authorized, no token send")

        #check if the token is correct
        try:
            grant = Grant()
            results = grant.get(token=token)
        except ObjectDoesNotExist, e:
            raise tornado.web.HTTPError(403,"invalid authorization token incorrect")
        #check the refresh
        time_remain = grant.is_token_expired(token)
        if int(time_remain['expiration']) < 0:
            raise tornado.web.HTTPError(403,"token expired")
        self._grant_token = token