import time

# cleans the data and logs it
class Logger(object):

    def __init__(self, *args, **kwargs):
        # check if database exists/was passed
        for v in args:
            setattr(self, v)
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        if not self.DB:
            raise NullDatabaseException

    # clean up messages
    def log(self, message):
        msg_type = message['message_type']

        if msg_type is 'outgoing':
            msg = self.get_sent(message['message_id'])
            # send back if delivery notification says failed
            if msg.has_key('status'):
                if msg['status'] is 'FAILED':
                    return msg
            # delivery notification updates the sent message
            for k, v in msg:
                message[k] = v

        for k in ['client_id','secret_key','shortcode','message_type']:
            if message.has_key(k):
                del message[k]

        message['timestamp'] = int(time.time())

        # save messages in proper database
        if msg_type is 'SEND' or msg_type is 'REPLY' or msg_type is 'outgoing':
            self.DB.outgoing.save(message)
            return 'Accepted'
        else:# msg_type is 'incoming':
            self.DB.incoming.save(message)
            return 'Accepted'
        #else : #if ever lang
        #    self.DB.others.save(message)
        #    return 'Error'

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
