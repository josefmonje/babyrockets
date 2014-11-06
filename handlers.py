from tornado.web import RequestHandler, authenticated

import json
import bson
from bson import json_util

from mongoauth import Auth
from mongologger import Logger
from Chikka import Chikka


class BaseHandler(RequestHandler):
    def initialize(self, database):
        self.auth = Auth(DB=database)
        self.logger = Logger(DB=database)
        self.chikka = Chikka()

    def get_current_user(self):
        user = self.get_secure_cookie('user')
        return user

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '.')


class IndexHandler(BaseHandler):
    def get(self):
        user = self.current_user
        if user:
            self.redirect('/main/')
        else:
            self.render('index.html')


class ErrorHandler(BaseHandler):
    def get(self):
        self.redirect('/')


class LogoutHandler(ErrorHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')


class LoginHandler(BaseHandler):
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = self.auth.login(email, password)
        if user:
            self.set_secure_cookie('user', email)
            self.redirect('/main/')
        else:
            self.render('index.html')


class UserHandler(BaseHandler):
    def get(self):
        msg = self.get_argument('msg', '')
        self.render('profile.html', msg=msg)

    def post(self):
        email = self.get_argument('email')
        mobile_number = self.get_argument('mobile_number')
        password = self.get_argument('password')
        password2 = self.get_argument('password2')
        first_name = self.get_argument('first_name')
        last_name = self.get_argument('last_name')
        designation = self.get_argument('designation')
        hospital = self.get_argument('hospital')
        if password == password2:
            user = self.auth.create(email, mobile_number, password, first_name, last_name, designation, hospital)
            self.set_secure_cookie('user', email)
            self.redirect('/main/')
        else:
            msg = 'Please check your account details'
            self.render('profile.html', msg=msg)



class MainHandler(BaseHandler):
    @authenticated
    def get(self):
        user = self.current_user
        self.render('main.html')


class ChikkaMessageHandler(BaseHandler):
    def post(self):
        data = json.loads(self.request.body)
        log = logger.log(data)
        # insert app logic here
        return log


class ChikkaNotificationHandler(BaseHandler):
    def post(self, message):
        # if the message is received back, send again.
        if log != 'Accepted' or log != 'Error':
            message = logger.get_sent(message['message_id'])
            chikka.send(message['mobile_number'], message['message'])
            return 'Accepted'
        else:
            return log


class APIHandler(BaseHandler):
    def get(self):
        q = self.get_argument('q', 'received')
        user = self.get_argument('user', '')

        if q == 'hospitals':
            data = self.auth.show_hospitals()
        elif q == 'contacts':
            data = self.auth.show_user(user)
            hospital = data['hospital']
            data = self.auth.show_users(hospital)
        elif q == 'received':
            data = self.logger.show_incoming(user)
        elif q == 'sent':
            data = self.logger.show_outgoing(user)
        elif q == 'user':
            data = self.auth.show_user(user)
        elif q == 'other':
            data = self.logger.show_others(user)
        else:
            data = 'Something went wrong...'

        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(data, default=bson.json_util.default))

    def post(self):
        data = json.loads(self.request.body)
        mobile_number = data['mobile_number']
        message = data['message']
        user = data['user']
        payload = {
            'user': user
        }

        if 'request_id' in data.keys():
            payload['request_id'] = data['request_id']

        if 'request_cost' in data.keys():
            payload['request_cost'] = data['request_cost']

        data = self.chikka.send(mobile_number, message, **payload)

        self.logger.log(data)


class NullDatabaseException(Exception):
    pass
