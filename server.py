from tornado.ioloop import IOLoop
from tornado.web import Application, url
from tornado.wsgi import WSGIAdapter
from tornado.httpserver import HTTPServer

from handlers import UserHandler, LoginHandler, LogoutHandler, \
                     IndexHandler, MainHandler, ErrorHandler, \
                     APIHandler, ChikkaMessageHandler, \
                     ChikkaNotificationHandler

try:
    from local_settings import COOKIE_SERCRET, CLIENT, DB
except ImportError:
    COOKIE_SERCRET = 'default_cookie_secret'
    CLIENT = None
    DB = None

import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('server')

handlers = [
    url(r'/', IndexHandler, dict(database=DB), name='index'),           #index.html
    url(r'/main/', MainHandler, dict(database=DB), name='main'),        #home.html
    url(r'/profile', UserHandler, dict(database=DB), name='profile'),   #register.html
    url(r'/login', LoginHandler, dict(database=DB), name='login'),
    url(r'/logout', LogoutHandler, dict(database=DB), name='logout'),
    url(r'/api', APIHandler, dict(database=DB), name='api'),
    (r'/ChikkaMessageReceiver/', ChikkaMessageHandler, dict(database=DB)),
    (r'/ChikkaNotificationReceiver/', ChikkaNotificationHandler, dict(database=DB)),
]


settings = { #Some standard settings
    'debug' : False,
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

wsgi_app = WSGIAdapter(handlers, **settings)


def make_app():
    return app

def main():
    print("It's ALIVE")
    application = make_app()
    #server = HTTPServer(application)
    #server.bind(8000)
    #server.start(0)  # forks one process per cpu
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()