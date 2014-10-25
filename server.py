from tornado.ioloop import IOLoop
from tornado.web import Application, url

from handlers import ErrorHandler, HomeHandler, MessageHandler, \
                     ChikkaMessageHandler, ChikkaNotificationHandler

try:
    from local_settings import COOKIE_SERCRET, DB
except ImportError:
    COOKIE_SERCRET = 'default_cookie_secret'
    DB = None

import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('server')

handlers = [
    (r'/', HomeHandler, dict(database=DB)),
    (r'/messages', MessageHandler, dict(database=DB)),
    (r'/ChikkaMessageReceiver/', ChikkaMessageHandler, dict(database=DB)),
    (r'/ChikkaNotificationReceiver/', ChikkaNotificationHandler, dict(database=DB)),
]

#Some standard settings
settings = {
    'debug' : True,
    'autoreload' : True,
    'template_path' : 'templates',
    'static_path' : 'static',
    'static_url_prefix' : '/static/',
    'default_handler_class' : ErrorHandler,
    'login_url' : '/login',
    'cookie_secret' : COOKIE_SERCRET,
    'xsrf_cookies' : False,
}


app = Application(handlers, **settings)

if __name__ == '__main__':
    print("Let the Awesome begin")
    app.listen(8000)
    IOLoop.instance().start()
