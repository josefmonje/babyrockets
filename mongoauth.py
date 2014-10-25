# handles web and sms auth
class Auth(object):

    def __init__(self, *args, **kwargs):
        # check if database exists/was passed
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        if not self.DB:
            raise NullDatabaseException

    # check if user with email already exists
    def exist(self, email):
        user = self.DB.users.find_one({ 'email': email })
        if user:
            return user
        else:
            return False

    # save new user
    def _new(self, email, password):
        return self.DB.users.save({ 'email': email , 'password': password })

    # check first if user exists before creating
    def create(self, email, password):
        user = self.exist(email):
        if user:
            return False
        else:
            return self._new(email, password)

    # user login returns True or False
    def login(self, email, password):
        user = self.DB.users.find_one({ 'email': email , 'password': password })
        if user:
            return True
        else:
            return False
