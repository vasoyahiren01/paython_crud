ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_STATUS = (100, 200, 201, 202, 300, 301, 302, 400, 401, 402, 500, 501, 502, 503)

OK = 1000
DB_ERR = 1001
LOGIN_FAIL = 1002
SERVER_ERR = 1003
AUTH_FAIL = 1004
NO_TOKEN = 1005
NO_USER = 1006
USER_EXISTS = 1007
PARAM_ERR = 1008
FILE_ILLEGAL = 1009
VALUE_ERROR = 1010
NO_DATA = 1011
DB_ERROR = 1012
REQ_REPEAT = 1013

# redis cache configuration
REDIS_DB = 15
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PWD = ''

REDIS_DB2 = 0
REDIS_HOST2 = '127.0.0.1'
REDIS_PORT2 = 6379
REDIS_PWD2 = 'XXX'
REDIS_URL_REQUEST = 'redis://:%s@%s:%s/%s' % (REDIS_PWD2, REDIS_HOST2, REDIS_PORT2, REDIS_DB2)
