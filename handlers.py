import json

from bson import json_util

from tornado.web import RequestHandler, authenticated

from mongologger import Logger

from Chikka import Chikka, API_URL

class BaseHandler(RequestHandler):

    def initialize(self, database):
        self.logger = Logger(DB=database)
        self.chikka = Chikka(DB=database)

    def get_current_user(self):
        return self.get_secure_cookie('user')
        # self.clear_cookie("user")

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '.')


class ErrorHandler(BaseHandler):
    def get(self):
        self.write('Something went wrong, sorry.')


class HomeHandler(BaseHandler):
    def get(self):
        user = self.current_user
        self.render('index.html')
        # self.write("Hello, %s" % user)


class ChikkaMessageHandler(BaseHandler):

    def post(self, data):
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


class MessageHandler(BaseHandler):

    def get(self):
        category = self.get_argument('category')
        if category == 'sent':
            data = self.logger.show_outgoing()
        elif category == 'received':
            data = self.logger.show_incoming()
        elif category == 'other':
            data = self.logger.show_others()
        else:
            data = [{'status':'Which messages would you like to see?'}]

        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(data, default=json_util.default))

    def post(self):
        data = json.loads(self.request.body)
        mobile_number = data['mobile_number']
        message = data['message']

        payload = {}

        try:
            request_id = data['request_id']
        except KeyError:
            request_id = None
        
        if request_id:
            payload['request_id'] = request_id

        try:
            request_cost = data['request_cost']
        except KeyError:
            request_cost = None

        if request_cost:
            payload['request_cost'] = request_cost

        if payload:
            data = self.chikka.send(mobile_number, message, **payload)
        else:
            data = self.chikka.send(mobile_number, message)

        self.logger.log(data)


class NullDatabaseException(Exception):
    pass
