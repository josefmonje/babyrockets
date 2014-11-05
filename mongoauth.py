# handles web and sms auth
class Auth(object):

    def __init__(self, *args, **kwargs):
        # check if database exists/was passed
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        for v in args:
            setattr(self, v)

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
    def _new(self, email, mobile_number, password, first_name, last_name, designation, hospital):
        return self.DB.users.save({
            'email': email,
            'mobile_number': mobile_number,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'designation': designation,
            'hospital': hospital
        })

    # check first if user exists before creating
    def create(self, email, mobile_number, password, first_name, last_name, designation, hospital):
        user = self.exist(email)
        if user:
            return False
        else:
            return self._new(email, mobile_number, password, first_name, last_name, designation, hospital)

    # user login returns True or False
    def login(self, email, password):
        user = self.DB.users.find_one({ 'email': email , 'password': password })
        if user:
            return True
        else:
            return False

    def show_user(self, email):
        return self.DB.users.find_one({ 'email': email }, {'password': 0 })

    def show_users(self, hospital):
        return list(self.DB.users.find({ 'hospital': hospital}, {'password': 0 }))

    def show_hospitals(self):
        return list(self.DB.hospitals.find())

