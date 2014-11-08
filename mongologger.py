import time

# cleans the data and logs it
class Logger(object):

    def __init__(self, *args, **kwargs):
        # check if database exists/was passed
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        for v in args:
            setattr(self, v)

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

        if 'client_id' in message.iterkeys():
            del message['client_id']
        if 'secret_key' in message.iterkeys():
            del message['secret_key']
        if 'shortcode' in message.iterkeys():
            del message['shortcode']

        msg_type = message['message_type']
        del message['message_type']

        message['timestamp'] = int(time.time())
        # save messages in proper database
        if msg_type is 'incoming':
            self.DB.incoming.save(message)
            return 'Accepted'
        elif msg_type == 'SEND' or msg_type == 'REPLY' or msg_type == 'outgoing':
            self.DB.outgoing.save(message)
            return 'Accepted'
        else: #if ever lang
            self.DB.others.save(message)
            return 'Error'

    def get_sent(self, message_id):
        return self.DB.outgoing.find_one({ 'message_id': message_id })

    def get_received(self, message_id):
        return self.DB.incoming.find_one({ 'message_id': message_id })

    def show_outgoing(self, user):
        return list(self.DB.outgoing.find({'user': user }))

    def show_incoming(self, user):
        return list(self.DB.incoming.find({'user': user }))

    def show_others(self):
        return list(self.DB.others.find())


class NullDatabaseException(Exception):
    pass
