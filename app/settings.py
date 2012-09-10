
"""Settings File.
Is possible to configure the Database, the accesso Token Length and the maximum ongoing call."""

__author__ = 'cingusoft'

OAUTH2_ACCESS_TOKEN_LENGTH = 15

DOMAIN_REST_PORT = '8888'
DOMAIN_REST = 'http://localhost:'+DOMAIN_REST_PORT+'/rest'
DATABASE = {
    "name": "clickcall",
    "user": "postgres",
    "password": "nw7a10bt",
    "host": "localhost",
    "port": "5432"
}

MAXIMUM_ONGOING_CALL = 2