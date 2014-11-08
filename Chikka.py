import os
import re
import requests

# add local_settings.py to .gitignore
# variables in local_settings optional, it won't be uploaded
try:
    from local_settings import CLIENT_ID, SECRET_KEY, SHORTCODE, REQUEST_COST
except ImportError:
    CLIENT_ID = None
    SECRET_KEY = None
    SHORTCODE = None

API_URL = 'https://post.chikka.com/smsapi/request'

SUN_PREFIXES = [
    '63922',
    '63923',
    '63925',
    '63932',
    '63933',
    '63934',
    '63942',
    '63943',
]

# send and receive messages using the Chikka API
class Chikka(object):

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        for v in args:
            setattr(self, v)

    def send(self, mobile_number, message, **kwargs):
        payload = self._prepare_payload()

        # if passed, store user for later use
        if kwargs.has_key('user'):
            user = kwargs.get('user')

        # check and validate mobile number
        if not mobile_number:
            raise NullMobileNumberException
        else:
            mobile_number = str(mobile_number)
 
        # e.g. 9991234567
        if len(mobile_number) is 10:
            mobile_number = '%s%s' % ('63', mobile_number)
 
        # e.g. 09991234567
        if len(mobile_number) is 11 and mobile_number.startswith('0'):
            mobile_number = '%s%s' % ('63', mobile_number[1:])
 
        # e.g. 639991234567
        if not re.match('^63[0-9]{10}', mobile_number):
            raise InvalidMobileNumberException

        payload['mobile_number'] = mobile_number

        # if request_id was passed it means message was received
        # determines message_type, adds other required payload
        if kwargs.get('request_id'):
            payload['request_id'] = kwargs.get('request_id')

        # also check if request_cost was passed to this method
        # if not, use default request_cost
        if kwargs.get('request_cost'):
            payload['request_cost'] = kwargs.get('request_cost', REQUEST_COST)

        # override request_cost if SUN, which can only be P2.00
        if mobile_number[0:5] in SUN_PREFIXES:
            payload['request_cost'] = 'P2.00'

            payload['message_type'] = 'REPLY'
        else:
            payload['message_type'] = 'SEND'

        # message_id can be passed to track messages sent
        # if message_id does not exist, generate a random message id
        payload['message_id'] = kwargs.get('message_id', os.urandom(16).encode('hex'))

        payload['message'] = message

        self.response = requests.post(API_URL, data=payload)

        # return user value
        if kwargs.has_key('user'):
            payload['user'] = user

        return payload


    def _prepare_payload(self):
        # check if other required fields exists
        client_id = getattr(self, 'client_id', CLIENT_ID)
        if not client_id:
            raise NullClientIDException

        secret_key = getattr(self, 'secret_key', SECRET_KEY)
        if not secret_key:
            raise NullSecretKeyException

        shortcode = getattr(self, 'shortcode', SHORTCODE)
        if not shortcode:
            raise NullShortCodeException

        payload = {
            'client_id': client_id,
            'secret_key': secret_key,
            'shortcode': shortcode,
        }

        return payload


class NullMobileNumberException(Exception):
    pass

class NullMessageException(Exception):
    pass

class InvalidMobileNumberException(Exception):
    pass

class NullClientIDException(Exception):
    pass

class NullSecretKeyException(Exception):
    pass

class NullShortCodeException(Exception):
    pass

class NullRequestCostException(Exception):
    pass
