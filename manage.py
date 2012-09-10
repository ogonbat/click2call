from app.oauth.auth.grant import GrantHandler
from app.oauth.auth.login import LoginHandler
from app.oauth.auth.logout import LogOutHandler
from app.oauth.auth.token import TokenHandler
from app.oauth.client.auth import AuthHandler
from app.oauth.client.call import CallHandler
from app.oauth.client.test import TestHandler
import tornado.web
import tornado.ioloop
import tornado.httpserver

__author__ = 'cingusoft'


handlers = [
    (r"/oauth/auth", AuthHandler),
    (r"/auth/login", LoginHandler),
    (r"/auth/logout", LogOutHandler),
    (r"/auth/grant", GrantHandler),
    (r"/oauth/token", TokenHandler),
    (r"/test", TestHandler), #we use this to read the code on redirection after the grant process
    #REST URI
    (r"/rest/call", CallHandler),


]

application = tornado.web.Application(handlers,cookie_secret="bdc1bc52787034900979109ec3a1760b",xsrf_cookies=False,login_url="/auth/login")


def main():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()