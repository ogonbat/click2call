import json
import unittest
import urllib
from tornado.testing import AsyncHTTPTestCase
import manage

__author__ = 'cingusoft'


class Skype_Test(AsyncHTTPTestCase):

    def get_app(self):
        return manage.application


    def get_http_port(self):
        return 8888

    def test_oauth(self):
        headers = {"Accept":"application/json"}

        response = self.fetch(
            '/oauth/auth?client_id=123456&response_type=code&redirect_uri=http://localhost&scope=call',
            method='GET',
            headers=headers,
            follow_redirects=True
        )
        self.assertEqual(response.code,200)
        loginData = json.loads(response.body)
        self.assertEqual(loginData['message'],"login")

        #Login Test
        loginData['username'] = "testuser"
        loginData['password'] = "testpassword"

        response = self.fetch(
            '/auth/login',
            method='POST',
            body=urllib.urlencode(loginData),
            headers=headers,

            follow_redirects=True
        )
        self.assertEqual(response.code,200)
        grantData = json.loads(response.body)
        self.assertEqual(grantData['message'],"grant")

        grantData['grant'] = "true"
        response = self.fetch(
            '/auth/grant',
            method='GET',
            #body=urllib.urlencode(grantData),
            headers=headers,
            follow_redirects=True
        )
        self.assertEqual(response.code,200)

if __name__ == '__main__':
    unittest.main()