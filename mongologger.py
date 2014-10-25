from datetime import datetime
import time


# cleans the data and logs it
class Logger(object):

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        # check if database exists/was passed
        if not self.DB:
            raise NullDatabaseException

    # clean up messages
    def log(self, message):
        if message['message_type'] is 'outgoing':
            msg = self.get_sent(message['message_id'])
            if message['status'] is 'FAILED':
                # send back if delivery notification says failed
                return msg
            # delivery notification updates the sent message
            for k, v in msg:
                message[k] = v
            del message['message_id']

        del message['client_id']
        del message['secret_key']
        del message['shortcode']

        msg_type = message['message_type']
        del message['message_type']

        message['timestamp'] = int(time.time())
        # save messages in proper database
        if msg_type is 'SEND' or msg_type is 'REPLY' or msg_type is 'outgoing':
            self.DB.outgoing.save(message)
            return 'Accepted'
        elif msg_type is 'incoming':
            self.DB.incoming.save(message)
            return 'Accepted'
        else: #if ever lang
            self.DB.others.save(message)
            return 'Error'

    def get_sent(self, message_id):
        return self.DB.outgoing.find_one({ 'message_id': message_id })

    def get_received(self, message_id):
        return self.DB.incoming.find_one({ 'message_id': message_id })

    def show_outgoing(self):
        return list(self.DB.outgoing.find())

    def show_incoming(self):
        return list(self.DB.incoming.find())

    def show_others(self):
        return list(self.DB.others.find())


class NullShortCodeException(Exception):
    pass

class NullDatabaseException(Exception):
    pass
